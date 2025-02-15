<div align="center">

# Discodrome

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
      - DISCORD_TOKEN=your_discord_token
      - SUBSONIC_URL=your_subsonic_url
      - SUBSONIC_USER=your_subsonic_username
      - SUBSONIC_PASS=your_subsonic_password
    restart: unless-stopped
```

3. Start the bot:
```bash
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables
- `DISCORD_TOKEN`: Your Discord bot token
- `SUBSONIC_URL`: URL of your Subsonic server
- `SUBSONIC_USER`: Subsonic username
- `SUBSONIC_PASS`: Subsonic password
- `AUTOPLAY_DEFAULT`: Default autoplay mode (optional, defaults to "none")
- `MAX_QUEUE_SIZE`: Maximum queue size (optional, defaults to 500)

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

Made with ❤️ by [7eventy7](https://github.com/7eventy7)

</div>
