# Development Guide

## Building Images Locally

### Prerequisites

- Docker or Podman
- Git

### Clone Repository

```bash
git clone https://github.com/zorro/takopi-docker.git
cd takopi-docker
```

### Build Commands

```bash
# Build specific variant
docker build -f Dockerfile.python --build-arg AGENT=all -t takopi:python-all .
docker build -f Dockerfile.typescript --build-arg AGENT=claude -t takopi:typescript-claude .
docker build -f Dockerfile.java --build-arg AGENT=all -t takopi:java-all .

# Build with Podman
podman build -f Dockerfile.python --build-arg AGENT=all -t takopi:python-all .
```

### Build Arguments

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `AGENT` | `all`, `claude`, `codex`, `opencode`, `pi` | `all` | Which agent(s) to pre-install |
| `NODE_MAJOR` | `20`, `22` | `22` | Node.js major version |
| `JAVA_VERSION` | `17`, `21` | `21` | Java version (Java image only) |
| `MAVEN_VERSION` | `3.9.x` | `3.9.9` | Maven version |
| `GRADLE_VERSION` | `8.x` | `8.12` | Gradle version |

## Testing Changes

### Quick Test

```bash
# Build and run interactively
docker build -f Dockerfile.python --build-arg AGENT=claude -t test:latest .
docker run -it --rm test:latest bash
```

### Test Wrapper Scripts

```bash
# Inside container
/opt/takopi-docker/scripts/wrappers/claude --version
```

### Test Configurator

```bash
# Inside container
python3 /opt/takopi-docker/scripts/configurator.py
```

## Project Structure

```
takopi-docker/
├── Dockerfile.base           # Shared base (not built directly)
├── Dockerfile.python         # Python variant
├── Dockerfile.typescript     # TypeScript variant
├── Dockerfile.java           # Java variant
├── scripts/
│   ├── entrypoint.sh         # Container entrypoint
│   ├── configurator.py       # Interactive TUI
│   ├── install-takopi.sh     # Takopi installer
│   ├── install-packages.sh   # System package installer
│   ├── setup-auth.sh         # Auth symlink setup
│   └── wrappers/
│       ├── claude            # Claude wrapper
│       ├── codex             # Codex wrapper
│       ├── opencode          # OpenCode wrapper
│       └── pi                # Pi wrapper
├── docker-compose.yml        # Local dev setup
├── .github/
│   └── workflows/
│       └── build.yml         # CI/CD pipeline
└── docs/
    ├── installation.md
    ├── configuration.md
    ├── agents.md
    └── development.md
```

## Contributing

### Code Style

- Shell scripts: Follow [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- Python: Use ruff for formatting and linting
- Dockerfiles: Follow [hadolint](https://github.com/hadolint/hadolint) recommendations

### Pull Request Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes
4. Test locally with Docker/Podman
5. Submit PR against `main` branch

### Testing Checklist

Before submitting a PR:

- [ ] All Dockerfiles build successfully
- [ ] Podman compatibility verified
- [ ] Wrapper scripts install agents correctly
- [ ] Auth symlinks work with mounted volumes
- [ ] Configurator menus functional
- [ ] No new hadolint warnings

## CI/CD Pipeline

The GitHub Actions workflow:

1. **Build Matrix**: Builds all 15 image variants
2. **Podman Test**: Verifies Podman compatibility
3. **Hadolint**: Validates Dockerfile syntax
4. **Push**: Pushes to ghcr.io on main/tags

### Manual Builds

Trigger manual build via GitHub Actions:
1. Go to Actions tab
2. Select "Build and Push Docker Images"
3. Click "Run workflow"
4. Optionally filter by language/agent

## Releasing

1. Update version in relevant files
2. Create git tag: `git tag v1.0.0`
3. Push tag: `git push origin v1.0.0`
4. GitHub Actions builds and publishes images
5. Release created automatically with changelog
