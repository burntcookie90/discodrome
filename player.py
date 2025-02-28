''' A player object that handles playback and data for its respective guild '''

import asyncio
import discord

import data
import subsonic
import ui
import logging

from subsonic import Song

logger = logging.getLogger(__name__)

# Default player data
_default_data: dict[str, any] = {
    "current-song": None,
    "current-position": 0,
    "queue": [],
}

class Player():
    ''' Class that represents an audio player '''
    def __init__(self) -> None:
        self._data = _default_data  
        self._player_loop = None

    @property
    def current_song(self) -> Song:
        '''The current song'''
        return self._data["current-song"]

    @current_song.setter
    def current_song(self, song: Song) -> None:
        self._data["current-song"] = song

    @property
    def current_position(self) -> int:
        ''' The current position for the current song, in seconds. '''
        return self._data["current-position"]

    @current_position.setter
    def current_position(self, position: int) -> None:
        ''' Set the current position for the current song, in seconds. '''
        self._data["current-position"] = position

    @property
    def queue(self) -> list[Song]:
        ''' The current audio queue. '''
        return self._data["queue"]

    @queue.setter
    def queue(self, value: list) -> None:
        self._data["queue"] = value

    @property
    def player_loop(self) -> asyncio.AbstractEventLoop:
        ''' The player loop '''
        return self._player_loop
    
    @player_loop.setter
    def player_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._player_loop = loop





    async def stream_track(self, interaction: discord.Interaction, song: Song, voice_client: discord.VoiceClient) -> None:
        ''' Streams a track from the Subsonic server to a connected voice channel, and updates guild data accordingly '''

        # Make sure the voice client is available
        if voice_client is None:
            await ui.ErrMsg.bot_not_in_voice_channel(interaction)
            return

        # Make sure the bot isn't already playing music
        if voice_client.is_playing():
            await ui.ErrMsg.already_playing(interaction)
            return

        # Get the stream from the Subsonic server, using the provided song's ID
        ffmpeg_options = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                           "options": "-filter:a volume=replaygain=track"}
        audio_src = discord.FFmpegOpusAudio(subsonic.stream(song.song_id), **ffmpeg_options)
        # audio_src.read()

        # TODO: Start a duration timer

        # Begin playing the song
        loop = asyncio.get_event_loop()
        self.player_loop = loop

        # Handle playback finished
        async def playback_finished(error):
            if await self.handle_autoplay(interaction, self.current_song.song_id):
                asyncio.run_coroutine_threadsafe(self.play_audio_queue(interaction, voice_client), loop)
            else:
                # Add a cooldown check before sending the playback ended message
                last_message_time = getattr(interaction.guild, "last_playback_ended_message_time", 0)
                current_time = asyncio.get_running_loop().time()
                if current_time - last_message_time >= 5:  # 5 seconds cooldown
                    asyncio.run_coroutine_threadsafe(ui.SysMsg.playback_ended(interaction), loop)
                    interaction.guild.last_playback_ended_message_time = current_time

        voice_client.play(audio_src, after=playback_finished)


    async def handle_autoplay(self, interaction: discord.Interaction, prev_song_id: str=None) -> bool:
        ''' Handles populating the queue when autoplay is enabled '''

        autoplay_mode = data.guild_properties(interaction.guild_id).autoplay_mode
        queue = data.guild_data(interaction.guild_id).player.queue

        # If queue is notempty or autoplay is disabled, don't handle autoplay
        if queue != [] or autoplay_mode is data.AutoplayMode.NONE:
            return False

        # If there was no previous song provided, we default back to selecting a random song
        if prev_song_id is None:
            autoplay_mode = data.AutoplayMode.RANDOM

        songs = []

        match autoplay_mode:
            case data.AutoplayMode.RANDOM:
                songs = subsonic.get_random_songs(size=1)
            case data.AutoplayMode.SIMILAR:
                songs = subsonic.get_similar_songs(song_id=prev_song_id, count=1)

        # If there's no match, throw an error
        if len(songs) == 0:
            await ui.ErrMsg.msg(interaction, "Failed to obtain a song for autoplay.")
            return False
        
        self.queue.append(songs[0])
        return True
        # Fetch the cover art in advance
        subsonic.get_album_art_file(songs[0].cover_id)


    async def play_audio_queue(self, interaction: discord.Interaction, voice_client: discord.VoiceClient) -> None:
        ''' Plays the audio queue '''

        # Check if the bot is connected to a voice channel; it's the caller's responsibility to open a voice channel
        if voice_client is None:
            await ui.ErrMsg.bot_not_in_voice_channel(interaction)
            return
        
        # Check if the bot is already playing something
        if voice_client.is_playing():
            return


        # Check if the queue contains songs
        if self.queue != []:

            # Pop the first item from the queue and stream the track
            song = self.queue.pop(0)
            self.current_song = song
            await ui.SysMsg.now_playing(interaction, song)
            await self.stream_track(interaction, song, voice_client)
        else:
            # If the queue is empty, playback has ended; we should let the user know
            await ui.SysMsg.playback_ended(interaction)


    async def skip_track(self, interaction: discord.Interaction, voice_client: discord.VoiceClient) -> None:
        ''' Skips the current track and plays the next one in the queue '''

        # Check if the bot is connected to a voice channel; it's the caller's responsibility to open a voice channel
        if voice_client is None:
            await ui.ErrMsg.bot_not_in_voice_channel(interaction)
            return
        logger.debug("Skipping track...")
        # Check if the bot is already playing something
        if voice_client.is_playing():
            voice_client.stop()
            await self.play_audio_queue(interaction, voice_client)
            await ui.SysMsg.skipping(interaction)
        else:
            await ui.ErrMsg.not_playing(interaction)
