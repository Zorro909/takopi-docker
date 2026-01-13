# takopi-docker

Docker images for running [takopi](https://github.com/zorro/takopi) with AI coding agents in containerized environments.

## Features

- **Multiple Language Variants**: Python, TypeScript, and Java development environments
- **All Major AI Coding Agents**: Claude Code, Codex, OpenCode, and Pi
- **Interactive Configurator**: TUI-based setup for agents and takopi
- **Auto-Updates**: Wrapper scripts check for agent updates daily
- **Auth Persistence**: Mount your credentials from the host
- **Plugin Support**: Install takopi plugins from PyPI or Git
- **System Packages**: Dynamic apt package installation

## Quick Start

```bash
# Pull the Python image with all agents
docker pull ghcr.io/zorro/takopi-docker:python-all

# Run with auth mounted
docker run -it \
  -v ~/.claude:/mnt/auth/claude:ro \
  -v ~/.takopi:/home/takopi/.takopi \
  ghcr.io/zorro/takopi-docker:python-all
```

## Available Images

| Tag | Description |
|-----|-------------|
| `python-all` | Python + all agents |
| `python-claude` | Python + Claude Code only |
| `python-codex` | Python + Codex only |
| `python-opencode` | Python + OpenCode only |
| `python-pi` | Python + Pi only |
| `typescript-all` | TypeScript + all agents |
| `typescript-claude` | TypeScript + Claude Code only |
| `java-all` | Java + all agents |
| ... | (15 total combinations) |

## Documentation

- [Installation Guide](docs/installation.md) - Setup and configuration
- [Configuration Reference](docs/configuration.md) - Environment variables and options
- [Agent Details](docs/agents.md) - Per-agent authentication and features
- [Development Guide](docs/development.md) - Building and contributing

## Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/zorro/takopi-docker.git
cd takopi-docker

# Create projects directory
mkdir -p projects

# Start the Python variant
docker compose up -d takopi-python

# Or start the configurator
docker compose --profile configure up configurator
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TAKOPI_SYS_INSTALL` | System packages to install | `ripgrep,fd-find` |
| `TAKOPI_PLUGIN_INSTALL` | Plugins to install | `my-plugin,https://github.com/user/repo.git` |

## License

MIT
