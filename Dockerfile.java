# Java development image for takopi-docker
# Includes Java (Eclipse Temurin), Maven, and Gradle

FROM python:3.14-trixie

LABEL org.opencontainers.image.source="https://github.com/zorro/takopi-docker"
LABEL org.opencontainers.image.description="Java development image for takopi"

# Build arguments
ARG AGENT=all
ARG NODE_MAJOR=22
ARG JAVA_VERSION=21
ARG MAVEN_VERSION=3.9.9
ARG GRADLE_VERSION=8.12

# Environment variables
ENV AGENT=${AGENT} \
    PATH="/opt/takopi-docker/scripts/wrappers:/home/takopi/.local/bin:/home/takopi/.cargo/bin:${PATH}" \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    JAVA_HOME="/opt/java/temurin" \
    MAVEN_HOME="/opt/maven" \
    GRADLE_HOME="/opt/gradle"

ENV PATH="${JAVA_HOME}/bin:${MAVEN_HOME}/bin:${GRADLE_HOME}/bin:${PATH}"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    curl \
    wget \
    git \
    ca-certificates \
    gnupg \
    openssh-client \
    jq \
    build-essential \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
        | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" \
        > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && npm config set prefix '/usr/local'

# Install Eclipse Temurin JDK
RUN mkdir -p /opt/java \
    && curl -fsSL "https://github.com/adoptium/temurin${JAVA_VERSION}-binaries/releases/download/jdk-${JAVA_VERSION}%2B35/OpenJDK${JAVA_VERSION}U-jdk_x64_linux_hotspot_${JAVA_VERSION}_35.tar.gz" \
        | tar -xz -C /opt/java \
    && mv /opt/java/jdk-${JAVA_VERSION}+35 /opt/java/temurin

# Install Maven
RUN curl -fsSL "https://archive.apache.org/dist/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz" \
        | tar -xz -C /opt \
    && mv /opt/apache-maven-${MAVEN_VERSION} /opt/maven

# Install Gradle
RUN curl -fsSL "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" -o gradle.zip \
    && unzip -q gradle.zip -d /opt \
    && mv /opt/gradle-${GRADLE_VERSION} /opt/gradle \
    && rm gradle.zip

# Create non-root user with passwordless sudo
RUN useradd -m -s /bin/bash -G sudo takopi \
    && echo "takopi ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/ \
    && mv /root/.local/bin/uvx /usr/local/bin/

# Copy scripts
COPY scripts/ /opt/takopi-docker/scripts/
RUN chmod +x /opt/takopi-docker/scripts/*.sh \
    && chmod +x /opt/takopi-docker/scripts/wrappers/* \
    && chmod +x /opt/takopi-docker/scripts/configurator.py

# Create mount point for auth
RUN mkdir -p /mnt/auth && chown takopi:takopi /mnt/auth

# Switch to non-root user
USER takopi
WORKDIR /home/takopi

# Create necessary directories and configure npm for user-local installs
RUN mkdir -p ~/.takopi-docker ~/.local/bin ~/.local/share ~/.config ~/.m2 ~/.gradle ~/.npm-global \
    && npm config set prefix ~/.npm-global

ENV PATH="/home/takopi/.npm-global/bin:${PATH}"

# Install Python packages for configurator
RUN pip install --user --no-cache-dir rich questionary

# Install agents based on AGENT arg
RUN if [ "$AGENT" = "all" ] || [ "$AGENT" = "claude" ]; then \
        curl -fsSL https://claude.ai/install.sh | bash && \
        touch ~/.takopi-docker/last-update-claude; \
    fi

RUN if [ "$AGENT" = "all" ] || [ "$AGENT" = "codex" ]; then \
        npm install -g @openai/codex && \
        touch ~/.takopi-docker/last-update-codex; \
    fi

RUN if [ "$AGENT" = "all" ] || [ "$AGENT" = "opencode" ]; then \
        ARCH=$(uname -m) && \
        if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then \
            curl -fsSL https://opencode.ai/install | bash && \
            touch ~/.takopi-docker/last-update-opencode; \
        else \
            echo "OpenCode not available for $ARCH, skipping..."; \
        fi \
    fi

RUN if [ "$AGENT" = "all" ] || [ "$AGENT" = "pi" ]; then \
        npm install -g @mariozechner/pi-coding-agent && \
        touch ~/.takopi-docker/last-update-pi; \
    fi

ENTRYPOINT ["/opt/takopi-docker/scripts/entrypoint.sh"]
CMD []
