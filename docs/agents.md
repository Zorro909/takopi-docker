# AI Coding Agents

## Claude Code

**Provider**: Anthropic
**Description**: Official CLI for Claude AI coding assistant

### Installation Method

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Auth Location

| File | Purpose |
|------|---------|
| `~/.claude/.credentials.json` | OAuth tokens |
| `~/.claude/settings.json` | User preferences |

### Mount Command

```bash
-v ~/.claude:/mnt/auth/claude:ro
```

### First Run

Claude Code will prompt for authentication on first run:
1. Opens browser for OAuth flow
2. Stores credentials in `~/.claude/.credentials.json`

---

## Codex

**Provider**: OpenAI
**Description**: AI coding assistant CLI with ChatGPT Plus/Pro subscription

### Installation Method

```bash
npm install -g @openai/codex
```

### Auth Location

| File | Purpose |
|------|---------|
| `~/.codex/auth.json` | API credentials (chmod 600) |
| `~/.codex/config.toml` | Configuration |

### Mount Command

```bash
-v ~/.codex:/mnt/auth/codex:ro
```

### Authentication Options

1. **ChatGPT Subscription**: OAuth flow via browser
2. **API Key**: Set `OPENAI_API_KEY` environment variable

---

## OpenCode

**Provider**: Open Source (SST)
**Description**: Multi-provider AI coding agent

### Installation Method

```bash
curl -fsSL https://opencode.ai/install | bash
```

### Auth Location

| File | Purpose |
|------|---------|
| `~/.local/share/opencode/auth.json` | API keys/OAuth tokens |
| `~/.config/opencode/opencode.json` | Global configuration |

### Mount Command

```bash
-v ~/.config/opencode:/mnt/auth/opencode/config:ro
-v ~/.local/share/opencode:/mnt/auth/opencode/data:ro
```

### Provider Setup

Run `opencode auth login` to configure providers.

---

## Pi

**Provider**: Mario Zechner
**Description**: Multi-provider AI coding agent supporting many LLM backends

### Installation Method

```bash
npm install -g @mariozechner/pi-coding-agent
```

### Auth Location

| File | Purpose |
|------|---------|
| `~/.pi/settings.json` | Configuration and API keys |
| `~/.pi/agent/sessions/` | Session storage |

### Mount Command

```bash
-v ~/.pi:/mnt/auth/pi:ro
```

### Supported Providers

- Anthropic (Claude)
- OpenAI (GPT-4)
- Google (Gemini)
- Mistral
- Groq
- xAI (Grok)
- OpenRouter
- Ollama (local)

---

## Agent Comparison

| Feature | Claude | Codex | OpenCode | Pi |
|---------|--------|-------|----------|-----|
| Provider | Anthropic | OpenAI | Multi | Multi |
| Install | curl | npm | curl | npm |
| Auth | OAuth | OAuth/Key | OAuth | API Keys |
| Offline | No | No | Ollama | Ollama |
| Free Tier | Limited | No | Varies | Varies |

## Troubleshooting

### Agent Not Found

If wrapper can't find the agent after installation:
1. Check PATH includes wrapper directory
2. Verify installation completed successfully
3. Run agent install command manually

### Auth Issues

If authentication fails:
1. Verify mount paths are correct
2. Check file permissions (should be readable)
3. Try authenticating interactively first
4. Copy credentials from container to host if needed

### Update Issues

If auto-update fails:
1. Check network connectivity
2. Verify npm/curl work inside container
3. Run update manually: `npm update -g @openai/codex`
4. Delete timestamp file to force fresh install
