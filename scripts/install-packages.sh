#!/bin/bash
# Install system packages dynamically
# Packages are specified via TAKOPI_SYS_INSTALL environment variable
# Format: pkg1,pkg2,pkg3,...

set -euo pipefail

if [[ -z "${TAKOPI_SYS_INSTALL:-}" ]]; then
    echo "[takopi-docker] No system packages to install (TAKOPI_SYS_INSTALL not set)"
    exit 0
fi

echo "[takopi-docker] Installing system packages..."

# Split by comma and convert to space-separated list
IFS=',' read -ra PACKAGES <<< "${TAKOPI_SYS_INSTALL}"

# Build package list
PACKAGE_LIST=""
for pkg in "${PACKAGES[@]}"; do
    # Trim whitespace
    pkg=$(echo "${pkg}" | xargs)
    if [[ -n "${pkg}" ]]; then
        PACKAGE_LIST="${PACKAGE_LIST} ${pkg}"
    fi
done

if [[ -z "${PACKAGE_LIST}" ]]; then
    echo "[takopi-docker] No valid packages specified"
    exit 0
fi

echo "[takopi-docker] Packages to install:${PACKAGE_LIST}"

# Update package lists and install
sudo apt-get update
sudo apt-get install -y ${PACKAGE_LIST}

# Clean up apt cache to reduce image size
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

echo "[takopi-docker] System packages installed successfully"
