# Discodrome 🎵

Discodrome is a powerful Discord bot that streams music from your personal Subsonic server. It allows you to enjoy your own music collection within Discord voice channels, with commands for playing, queueing, skipping tracks, and more.

## Features

🔹 Play music from your Subsonic server in Discord voice channels 🎵
🔹 Queue tracks and manage the playback order 📜
🔹 Skip tracks or clear the entire queue ⏩
🔹 Automatic playback of similar or random tracks 🔁
🔹 Easy setup with Docker or from source 🚀

## Installation

1. Pull the latest Docker image:
   ```
   docker pull 7eventy7/discodrome:latest
   ```

2. Run the Docker container with the required environment variables:
   ```
   docker run -e DISCORD_TOKEN=your_discord_token \
              -e SUBSONIC_URL=your_subsonic_url \
              -e SUBSONIC_USER=your_subsonic_username \
              -e SUBSONIC_PASS=your_subsonic_password \
              7eventy7/discodrome:latest
   ```
   Replace the placeholders with your actual Discord bot token, Subsonic server URL, username, and password.


## Commands

🤖 `/play [query]`: Play a track matching the given query. If no query is provided, resume playback of the current queue.
🤖 `/stop`: Stop playback and disconnect the bot from the voice channel.
🤖 `/queue`: Display the current playback queue.
🤖 `/clear`: Clear all tracks from the playback queue.
🤖 `/skip`: Skip the currently playing track.
🤖 `/autoplay [mode]`: Set the autoplay mode to "none", "random", or "similar". Autoplay will automatically queue tracks after the current queue is exhausted.

## Contributing

Contributions are welcome! 🤝 If you encounter any bugs 🐛 or have suggestions for new features 💡, please open an issue on the [GitHub repository](https://github.com/yourusername/discodrome). If you'd like to contribute code changes 💻, feel free to open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.