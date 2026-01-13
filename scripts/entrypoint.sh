#!/bin/bash
# Main entrypoint for takopi-docker containers
# Handles auth setup, package installation, and service startup

set -euo pipefail

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "  takopi-docker"
echo "=============================================="

# Step 1: Setup authentication symlinks
"${SCRIPTS_DIR}/setup-auth.sh"

# Step 2: Install system packages if requested
if [[ -n "${TAKOPI_SYS_INSTALL:-}" ]]; then
    "${SCRIPTS_DIR}/install-packages.sh"
fi

# Step 3: Install/update takopi and plugins
"${SCRIPTS_DIR}/install-takopi.sh"

echo "=============================================="
echo "  Setup complete!"
echo "=============================================="

# Step 4: Determine what to run
if [[ $# -gt 0 ]]; then
    # Arguments provided, execute them
    echo "[takopi-docker] Running: $*"
    exec "$@"
else
    # No arguments - check if takopi is configured
    TAKOPI_CONFIG="${HOME}/.takopi/takopi.toml"

    if [[ -f "${TAKOPI_CONFIG}" ]]; then
        # Config exists, try to run takopi serve
        echo "[takopi-docker] Starting takopi serve..."
        exec takopi serve
    else
        # No config, launch configurator
        echo "[takopi-docker] No configuration found, launching configurator..."
        exec python3 "${SCRIPTS_DIR}/configurator.py"
    fi
fi
