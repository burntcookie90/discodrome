<div align="center">

# DiscoDrome

### Discord bot that streams music from your personal Subsonic server

[![GitHub issues](https://img.shields.io/github/issues/7eventy7/discodrome.svg)](https://github.com/7eventy7/discodrome/issues)
[![Docker Pulls](https://img.shields.io/docker/pulls/7eventy7/discodrome.svg)](https://hub.docker.com/r/7eventy7/discodrome)
[![License](https://img.shields.io/github/license/7eventy7/discodrome.svg)](https://github.com/7eventy7/discodrome/blob/main/LICENSE)

Enjoy your music collection within Discord voice channels with rich playback controls and automation features.

</div>

---

## 🎮 Commands

- `/play [query]`: Play a track matching the query or resume current queue
- `/stop`: Stop playback and disconnect from voice channel
- `/queue`: Display the current playback queue
- `/clear`: Clear all tracks from the queue
- `/skip`: Skip the currently playing track
- `/autoplay [mode]`: Set autoplay mode (none/random/similar)

## 🚀 Getting Started

### Using Docker (Recommended)

1. Pull the latest image:
```bash
docker pull 7eventy7/discodrome:latest
```

2. Create a docker-compose.yml file:
```yaml
version: '3'
services:
  discodrome:
    image: 7eventy7/discodrome:latest
    environment:
      - SUBSONIC_SERVER=your_subsonic_server
      - SUBSONIC_USER=your_subsonic_username
      - SUBSONIC_PASSWORD=your_subsonic_password
      - DISCORD_BOT_TOKEN=your_discord_bot_token
      - DISCORD_TEST_GUILD=your_discord_test_guild
      - DISCORD_OWNER_ID=your_discord_owner_id
      - BOT_STATUS=your_bot_status
    restart: unless-stopped
```

3. Start the bot:
```bash
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables
- `SUBSONIC_SERVER`: URL of your Subsonic server
- `SUBSONIC_USER`: Subsonic username
- `SUBSONIC_PASSWORD`: Subsonic password
- `DISCORD_BOT_TOKEN`: Your Discord bot token
- `DISCORD_TEST_GUILD`: Discord test guild ID
- `DISCORD_OWNER_ID`: Discord owner ID
- `BOT_STATUS`: Bot status message (optional)

## 🛠️ Technical Stack

- Discord.js
- Node.js
- Subsonic API
- Docker
- FFmpeg for audio processing

## 👥 Contributing

We welcome contributions! Whether it's:

- 🐛 Reporting bugs
- 💡 Suggesting features
- 📝 Improving documentation
- 🔍 Submitting fixes
- ✨ Adding new features

Please check our [GitHub Issues](https://github.com/7eventy7/discodrome/issues) before submitting new ones.

## 📝 License

GPL-3.0 license - feel free to use this project for most any purpose.

## 🙏 Acknowledgments

This project is a fork of [Submeister](https://github.com/Gimzie/submeister) by Gimzie. We've built upon their excellent foundation to add new features and improvements while maintaining the core functionality that made the original project great.

---

<div align="center">

Forked with ❤️ by [7eventy7](https://github.com/7eventy7)

</div>
