#!/bin/bash
# Setup authentication symlinks from mounted volumes
# Mount points expected at /mnt/auth/{agent}/
# Symlinks created to standard locations in home directory

set -euo pipefail

AUTH_MOUNT="/mnt/auth"
HOME_DIR="${HOME}"

echo "[takopi-docker] Setting up authentication symlinks..."

# Function to create symlink if source exists
setup_symlink() {
    local source="$1"
    local target="$2"
    local name="$3"

    if [[ -d "${source}" ]]; then
        # Ensure parent directory exists
        mkdir -p "$(dirname "${target}")"

        # Remove existing target if it's a symlink or empty directory
        if [[ -L "${target}" ]]; then
            rm "${target}"
        elif [[ -d "${target}" && -z "$(ls -A "${target}" 2>/dev/null)" ]]; then
            rmdir "${target}" 2>/dev/null || true
        fi

        # Create symlink if target doesn't exist
        if [[ ! -e "${target}" ]]; then
            ln -s "${source}" "${target}"
            echo "[takopi-docker] Linked ${name}: ${source} -> ${target}"
        else
            echo "[takopi-docker] Warning: ${target} already exists, skipping ${name}"
        fi
    else
        echo "[takopi-docker] Note: ${name} auth not mounted (${source} not found)"
    fi
}

# Claude Code: ~/.claude/
setup_symlink "${AUTH_MOUNT}/claude" "${HOME_DIR}/.claude" "Claude Code"

# Codex: ~/.codex/
setup_symlink "${AUTH_MOUNT}/codex" "${HOME_DIR}/.codex" "Codex"

# OpenCode: ~/.local/share/opencode/ and ~/.config/opencode/
if [[ -d "${AUTH_MOUNT}/opencode" ]]; then
    # OpenCode has two config locations
    setup_symlink "${AUTH_MOUNT}/opencode/data" "${HOME_DIR}/.local/share/opencode" "OpenCode data"
    setup_symlink "${AUTH_MOUNT}/opencode/config" "${HOME_DIR}/.config/opencode" "OpenCode config"

    # Also support flat mount (just auth.json in root)
    if [[ -f "${AUTH_MOUNT}/opencode/auth.json" && ! -d "${AUTH_MOUNT}/opencode/data" ]]; then
        mkdir -p "${HOME_DIR}/.local/share/opencode"
        ln -sf "${AUTH_MOUNT}/opencode/auth.json" "${HOME_DIR}/.local/share/opencode/auth.json"
        echo "[takopi-docker] Linked OpenCode auth.json directly"
    fi
else
    echo "[takopi-docker] Note: OpenCode auth not mounted (${AUTH_MOUNT}/opencode not found)"
fi

# Pi: ~/.pi/
setup_symlink "${AUTH_MOUNT}/pi" "${HOME_DIR}/.pi" "Pi"

echo "[takopi-docker] Authentication setup complete"
