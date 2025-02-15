# submeister

## Running with Docker

The submeister application can be run using Docker. The Docker image is automatically built and pushed to DockerHub whenever changes are pushed to the main branch on GitHub.

To pull the latest Docker image, run:
```
docker pull <DOCKERHUB_USERNAME>/submeister:latest
```

To run the submeister container, use the following command:
```
docker run -e DISCORD_TOKEN=your_discord_token -e SUBSONIC_URL=your_subsonic_url -e SUBSONIC_USER=your_subsonic_username -e SUBSONIC_PASS=your_subsonic_password <DOCKERHUB_USERNAME>/submeister:latest
```

Replace the following environment variables with your own values:
- `DISCORD_TOKEN`: Your Discord bot token.
- `SUBSONIC_URL`: The URL of your Subsonic server.
- `SUBSONIC_USER`: Your Subsonic username.
- `SUBSONIC_PASS`: Your Subsonic password.

Make sure to set these environment variables when running the Docker container to ensure the application functions correctly.
A powerful Discord bot that streams music from your personal SubSonic server.
