# Installation Guide

## Prerequisites

- Docker or Podman installed
- (Optional) Docker Compose for easy setup
- Host machine credentials for AI agents

## Pulling Images

Images are available from GitHub Container Registry:

```bash
# Python with all agents (recommended for most users)
docker pull ghcr.io/zorro/takopi-docker:python-all

# TypeScript with Claude only
docker pull ghcr.io/zorro/takopi-docker:typescript-claude

# Java with all agents
docker pull ghcr.io/zorro/takopi-docker:java-all
```

## Running the Container

### Basic Usage

```bash
docker run -it ghcr.io/zorro/takopi-docker:python-all
```

This launches the interactive configurator if takopi is not configured.

### With Authentication

Mount your host credentials to enable agent authentication:

```bash
docker run -it \
  -v ~/.claude:/mnt/auth/claude:ro \
  -v ~/.codex:/mnt/auth/codex:ro \
  -v ~/.config/opencode:/mnt/auth/opencode/config:ro \
  -v ~/.local/share/opencode:/mnt/auth/opencode/data:ro \
  -v ~/.pi:/mnt/auth/pi:ro \
  ghcr.io/zorro/takopi-docker:python-all
```

### With Persistent Configuration

```bash
docker run -it \
  -v ~/.claude:/mnt/auth/claude:ro \
  -v takopi-config:/home/takopi/.takopi \
  -v ~/projects:/home/takopi/projects \
  ghcr.io/zorro/takopi-docker:python-all
```

## Using Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/zorro/takopi-docker.git
   cd takopi-docker
   ```

2. Create directories:
   ```bash
   mkdir -p projects
   ```

3. Start the service:
   ```bash
   # Python variant (default)
   docker compose up -d takopi-python

   # TypeScript variant
   docker compose --profile typescript up -d takopi-typescript

   # Java variant
   docker compose --profile java up -d takopi-java
   ```

4. Attach to the container:
   ```bash
   docker compose exec takopi-python bash
   ```

## Using Podman

All images work with Podman:

```bash
podman pull ghcr.io/zorro/takopi-docker:python-all

podman run -it \
  -v ~/.claude:/mnt/auth/claude:ro \
  ghcr.io/zorro/takopi-docker:python-all
```

For rootless Podman with user namespaces:

```bash
podman run -it \
  --userns=keep-id \
  -v ~/.claude:/mnt/auth/claude:ro \
  ghcr.io/zorro/takopi-docker:python-all
```

## Building Locally

```bash
# Clone the repository
git clone https://github.com/zorro/takopi-docker.git
cd takopi-docker

# Build Python variant with all agents
docker build -f Dockerfile.python --build-arg AGENT=all -t takopi:python-all .

# Build with specific agent only
docker build -f Dockerfile.python --build-arg AGENT=claude -t takopi:python-claude .

# Build TypeScript variant
docker build -f Dockerfile.typescript --build-arg AGENT=all -t takopi:typescript-all .

# Build Java variant
docker build -f Dockerfile.java --build-arg AGENT=all -t takopi:java-all .
```

## Volume Mounts Reference

| Purpose | Host Path | Container Path | Mode |
|---------|-----------|----------------|------|
| Claude auth | `~/.claude` | `/mnt/auth/claude` | ro |
| Codex auth | `~/.codex` | `/mnt/auth/codex` | ro |
| OpenCode config | `~/.config/opencode` | `/mnt/auth/opencode/config` | ro |
| OpenCode data | `~/.local/share/opencode` | `/mnt/auth/opencode/data` | ro |
| Pi auth | `~/.pi` | `/mnt/auth/pi` | ro |
| Takopi config | `~/.takopi` | `/home/takopi/.takopi` | rw |
| Projects | `~/projects` | `/home/takopi/projects` | rw |
