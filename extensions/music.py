import discord
import logging

from discord import app_commands
from discord.ext import commands

import data
import player
import subsonic
import ui

from discodrome import DiscodromeClient

logger = logging.getLogger(__name__)

class MusicCog(commands.Cog):
    ''' A Cog containing music playback commands '''

    bot : DiscodromeClient

    def __init__(self, bot: DiscodromeClient):
        self.bot = bot

    async def get_voice_client(self, interaction: discord.Interaction, *, should_connect: bool=False) -> discord.VoiceClient:
        ''' Returns a voice client instance for the current guild '''

        # Get the voice client for the guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        # Connect to a voice channel
        if voice_client is None and should_connect:
            try:
                voice_client = await interaction.user.voice.channel.connect()
            except AttributeError:
                await ui.ErrMsg.cannot_connect_to_voice_channel(interaction)

        return voice_client

    @app_commands.command(name="play", description="Plays a specified track")
    @app_commands.describe(query="Enter a search query")
    async def play(self, interaction: discord.Interaction, query: str=None) -> None:
        ''' Play a track matching the given title/artist query '''

        # Check if user is in voice channel
        if interaction.user.voice is None:
            return await ui.ErrMsg.user_not_in_voice_channel(interaction)

        # Get a valid voice channel connection
        voice_client = await self.get_voice_client(interaction, should_connect=True)

        # Don't attempt playback if the bot is already playing
        if voice_client.is_playing() and query is None:
            return await ui.ErrMsg.already_playing(interaction)

        # Get the guild's player
        player = data.guild_data(interaction.guild_id).player

        # Check queue if no query is provided
        if query is None:

            # Display error if queue is empty & autoplay is disabled
            if player.queue == [] and data.guild_properties(interaction.guild_id).autoplay_mode == data.AutoplayMode.NONE:
                return await ui.ErrMsg.queue_is_empty(interaction)

            # Begin playback of queue
            await ui.SysMsg.starting_queue_playback(interaction)
            await player.play_audio_queue(interaction, voice_client)
            return

        # Send our query to the subsonic API and retrieve a list of 1 song
        songs = subsonic.search(query, artist_count=0, album_count=0, song_count=1)

        # Display an error if the query returned no results
        if len(songs) == 0:
            await ui.ErrMsg.msg(interaction, f"No result found for **{query}**.")
            return
        
        # Add the first result to the queue and handle queue playback
        player.queue.append(songs[0])

        await ui.SysMsg.added_to_queue(interaction, songs[0])
        await player.play_audio_queue(interaction, voice_client)

        # Check if there are no users in the voice channel after the song finishes
        if len(voice_client.channel.members) == 1:
            # Wait for 10 seconds
            await asyncio.sleep(10)
            
            # Check again if there are still no users in the voice channel
            if len(voice_client.channel.members) == 1:
                # Disconnect the bot and clear the queue
                await voice_client.disconnect()
                player.queue.clear()
                await ui.SysMsg.msg(interaction, "The bot has disconnected and cleared the queue as there are no users in the voice channel.")


    @app_commands.command(name="stop", description="Stop playing the current track")
    async def stop(self, interaction: discord.Interaction) -> None:
        ''' Disconnect from the active voice channel '''

        # Get the voice client instance for the current guild
        voice_client = await self.get_voice_client(interaction)

        # Check if our voice client is connected
        if voice_client is None:
            await ui.ErrMsg.bot_not_in_voice_channel(interaction)
            return

        # Check if there are other users in the voice channel
        if len(voice_client.channel.members) > 1:
            await ui.SysMsg.msg(interaction, "The bot will stay connected as there are other users in the voice channel.")
            return

        # Disconnect the voice client if no other users are in the channel
        await interaction.guild.voice_client.disconnect()

        # Display disconnect confirmation
        await ui.SysMsg.disconnected(interaction)


    @app_commands.command(name="queue", description="View the current queue")
    async def show_queue(self, interaction: discord.Interaction) -> None:
        ''' Show the current queue '''

        # Get the audio queue for the current guild
        queue = data.guild_data(interaction.guild_id).player.queue

        # Create a string to store the output of our queue
        output = ""

        # Loop over our queue, adding each song into our output string
        for i, song in enumerate(queue):
            output += f"{i+1}. **{song.title}** - *{song.artist}*\n{song.album} ({song.duration_printable})\n\n"

        # Check if our output string is empty & update it accordingly
        if output == "":
            output = "Queue is empty!"

        # Show the user their queue
        await ui.SysMsg.msg(interaction, "Queue", output)


    @app_commands.command(name="clear", description="Clear the current queue")
    async def clear_queue(self, interaction: discord.Interaction) -> None:
        '''Clear the queue'''
        queue = data.guild_data(interaction.guild_id).player.queue
        queue.clear()

        # Let the user know that the queue has been cleared
        await ui.SysMsg.queue_cleared(interaction)


    @app_commands.command(name="skip", description="Skip the current track")
    async def skip(self, interaction: discord.Interaction) -> None:
        ''' Skip the current track '''

        # Get the voice client instance
        voice_client = await self.get_voice_client(interaction)

        # Check if the bot is connected to a voice channel
        if voice_client is None:
            await ui.ErrMsg.bot_not_in_voice_channel(interaction)
            return

        # Check if the bot is playing music
        if not voice_client.is_playing():
            await ui.ErrMsg.not_playing(interaction)
            return

        # Stop the current song
        voice_client.stop()

        # Display confirmation message
        await ui.SysMsg.skipping(interaction)


    @app_commands.command(name="autoplay", description="Toggles autoplay")
    @app_commands.describe(mode="Determines the method to use when autoplaying")
    @app_commands.choices(mode=[
        app_commands.Choice(name="None", value="none"),
        app_commands.Choice(name="Random", value="random"),
        app_commands.Choice(name="Similar", value="similar"),
    ])
    async def autoplay(self, interaction: discord.Interaction, mode: app_commands.Choice[str]) -> None:
        ''' Toggles autoplay '''

        # Update the autoplay properties
        match mode.value:
            case "none":
                data.guild_properties(interaction.guild_id).autoplay_mode = data.AutoplayMode.NONE
            case "random":
                data.guild_properties(interaction.guild_id).autoplay_mode = data.AutoplayMode.RANDOM
            case "similar":
                data.guild_properties(interaction.guild_id).autoplay_mode = data.AutoplayMode.SIMILAR

        # Display message indicating new status of autoplay
        if mode.value == "none":
            await ui.SysMsg.msg(interaction, f"Autoplay disabled by {interaction.user.display_name}")
        else:
            await ui.SysMsg.msg(interaction, f"Autoplay enabled by {interaction.user.display_name}", f"Autoplay mode: **{mode.name}**")

        # If the bot is connected to a voice channel and autoplay is enabled, start queue playback
        voice_client = await self.get_voice_client(interaction)
        if voice_client is not None and not voice_client.is_playing():
            player = data.guild_data(interaction.guild_id).player
            await player.play_audio_queue(interaction, voice_client)

async def setup(bot: DiscodromeClient):
    ''' Setup function for the music.py cog '''

    await bot.add_cog(MusicCog(bot))
