# Configuration Reference

## Environment Variables

### TAKOPI_SYS_INSTALL

Install system packages at container startup.

**Format**: Comma-separated list of apt package names

**Example**:
```bash
docker run -it \
  -e TAKOPI_SYS_INSTALL=ripgrep,fd-find,jq,htop \
  ghcr.io/zorro/takopi-docker:python-all
```

### TAKOPI_PLUGIN_INSTALL

Install takopi plugins at container startup.

**Format**: Comma-separated list of PyPI packages or Git URLs

**Detection**: URLs starting with `http://`, `https://`, or `git://` are treated as Git repositories. Everything else is treated as a PyPI package.

**Examples**:
```bash
# PyPI packages
-e TAKOPI_PLUGIN_INSTALL=takopi-slack,takopi-discord

# Git repositories
-e TAKOPI_PLUGIN_INSTALL=https://github.com/user/my-plugin.git

# Mixed
-e TAKOPI_PLUGIN_INSTALL=takopi-slack,https://github.com/user/custom-engine.git
```

## Auth Mount Points

Authentication credentials are mounted at `/mnt/auth/` and symlinked to standard locations.

| Agent | Mount Point | Symlinked To |
|-------|-------------|--------------|
| Claude | `/mnt/auth/claude/` | `~/.claude/` |
| Codex | `/mnt/auth/codex/` | `~/.codex/` |
| OpenCode | `/mnt/auth/opencode/config/` | `~/.config/opencode/` |
| OpenCode | `/mnt/auth/opencode/data/` | `~/.local/share/opencode/` |
| Pi | `/mnt/auth/pi/` | `~/.pi/` |

### Missing Auth Handling

If auth directories are not mounted:
- A warning is printed (container continues)
- Agents will prompt for authentication interactively
- Symlinks are not created for missing mounts

## Wrapper Script Behavior

Wrapper scripts in `/opt/takopi-docker/scripts/wrappers/` intercept agent commands.

### Auto-Installation

If an agent is not installed, the wrapper:
1. Detects the missing binary
2. Runs the official installation command
3. Creates a timestamp file
4. Executes the agent

### Auto-Updates

Every 24 hours, the wrapper:
1. Checks `~/.takopi-docker/last-update-{agent}` timestamp
2. If >24h old, triggers background update
3. Update runs asynchronously (non-blocking)
4. Updates timestamp on completion

### Disabling Auto-Updates

Set the timestamp file to a future date:
```bash
touch -d "2099-01-01" ~/.takopi-docker/last-update-claude
```

## Entrypoint Behavior

The container entrypoint (`/opt/takopi-docker/scripts/entrypoint.sh`):

1. **Auth Setup**: Creates symlinks from `/mnt/auth/` to home directories
2. **Package Install**: Runs `apt install` if `TAKOPI_SYS_INSTALL` is set
3. **Takopi Install**: Installs/updates takopi and plugins
4. **Command Selection**:
   - If arguments provided: Execute them directly
   - If `~/.takopi/takopi.toml` exists: Run `takopi serve`
   - Otherwise: Launch interactive configurator

### Running Specific Commands

```bash
# Run bash shell
docker run -it ghcr.io/zorro/takopi-docker:python-all bash

# Run specific agent
docker run -it ghcr.io/zorro/takopi-docker:python-all claude

# Run takopi command
docker run -it ghcr.io/zorro/takopi-docker:python-all takopi wizard
```

## Configurator Options

The interactive configurator (`/opt/takopi-docker/scripts/configurator.py`) provides:

### Agents Menu
- Install or update agents
- Configure agent settings
- View installation status

### Takopi Menu
- Run takopi wizard (initial setup)
- View current configuration
- Test Telegram connection

### Plugins Menu
- Install from PyPI
- Install from Git URL

### Packages Menu
- Install system packages
- Search available packages

### Start Menu
- Launch specific agent directly
