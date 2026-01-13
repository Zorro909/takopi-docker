#!/bin/bash
# Install takopi and optional plugins
# Plugins are specified via TAKOPI_PLUGIN_INSTALL environment variable
# Format: plugin1,plugin2,https://github.com/user/repo.git,...
# Auto-detects pip packages vs git URLs

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[takopi-docker] Installing takopi..."

# Ensure uv is available
if ! command -v uv &>/dev/null; then
    echo "[takopi-docker] Error: uv not found. Please install uv first." >&2
    exit 1
fi

# Install takopi
uv tool install -U takopi

echo "[takopi-docker] takopi installed successfully"

# Install plugins if specified
if [[ -n "${TAKOPI_PLUGIN_INSTALL:-}" ]]; then
    echo "[takopi-docker] Installing plugins..."

    # Split by comma
    IFS=',' read -ra PLUGINS <<< "${TAKOPI_PLUGIN_INSTALL}"

    for plugin in "${PLUGINS[@]}"; do
        # Trim whitespace
        plugin=$(echo "${plugin}" | xargs)

        if [[ -z "${plugin}" ]]; then
            continue
        fi

        # Auto-detect: if starts with http://, https://, or git://, treat as git URL
        if [[ "${plugin}" =~ ^(https?|git):// ]]; then
            echo "[takopi-docker] Installing plugin from git: ${plugin}"
            # Clone to temp dir and install
            temp_dir=$(mktemp -d)
            git clone --depth 1 "${plugin}" "${temp_dir}/plugin"
            uv tool install -U "${temp_dir}/plugin"
            rm -rf "${temp_dir}"
        else
            echo "[takopi-docker] Installing plugin from PyPI: ${plugin}"
            uv tool install -U "${plugin}"
        fi
    done

    echo "[takopi-docker] All plugins installed"
fi

echo "[takopi-docker] Installation complete"
