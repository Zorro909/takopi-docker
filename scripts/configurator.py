#!/usr/bin/env python3
"""
Interactive configurator for takopi-docker.
Provides a menu-based interface to configure agents, takopi, plugins, and packages.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Callable

try:
    import questionary
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except ImportError:
    print("[takopi-docker] Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "questionary"], check=True)
    import questionary
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

console = Console()

# Agent definitions
AGENTS = {
    "claude": {
        "name": "Claude Code",
        "description": "Anthropic's AI coding assistant",
        "check_cmd": "claude --version",
        "install_cmd": "curl -fsSL https://claude.ai/install.sh | bash",
        "config_dir": Path.home() / ".claude",
    },
    "codex": {
        "name": "Codex",
        "description": "OpenAI's coding assistant CLI",
        "check_cmd": "codex --version",
        "install_cmd": "npm install -g @openai/codex",
        "config_dir": Path.home() / ".codex",
    },
    "opencode": {
        "name": "OpenCode",
        "description": "Open source AI coding agent",
        "check_cmd": "opencode --version",
        "install_cmd": "curl -fsSL https://opencode.ai/install | bash",
        "config_dir": Path.home() / ".config" / "opencode",
    },
    "pi": {
        "name": "Pi",
        "description": "Multi-provider AI coding agent",
        "check_cmd": "pi --version",
        "install_cmd": "npm install -g @mariozechner/pi-coding-agent",
        "config_dir": Path.home() / ".pi",
    },
}


def run_command(cmd: str, capture: bool = False) -> tuple[int, str]:
    """Run a shell command and return (exit_code, output)."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture,
            text=True,
            timeout=300,
        )
        return result.returncode, result.stdout if capture else ""
    except subprocess.TimeoutExpired:
        return 1, "Command timed out"
    except Exception as e:
        return 1, str(e)


def is_agent_installed(agent_id: str) -> bool:
    """Check if an agent is installed."""
    agent = AGENTS[agent_id]
    code, _ = run_command(agent["check_cmd"], capture=True)
    return code == 0


def get_agent_status() -> dict[str, bool]:
    """Get installation status of all agents."""
    return {agent_id: is_agent_installed(agent_id) for agent_id in AGENTS}


def show_status():
    """Display current status of all agents."""
    console.print()
    table = Table(title="Agent Status")
    table.add_column("Agent", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Config Dir", style="dim")

    status = get_agent_status()
    for agent_id, agent in AGENTS.items():
        installed = status[agent_id]
        status_str = "[green]Installed[/green]" if installed else "[red]Not installed[/red]"
        config_exists = agent["config_dir"].exists()
        config_str = str(agent["config_dir"]) if config_exists else "[dim]Not configured[/dim]"
        table.add_row(agent["name"], status_str, config_str)

    console.print(table)
    console.print()


def menu_agents():
    """Agent installation and management menu."""
    while True:
        show_status()

        choices = [
            questionary.Choice("Install/Update an agent", value="install"),
            questionary.Choice("Configure an agent", value="configure"),
            questionary.Choice("Back to main menu", value="back"),
        ]

        action = questionary.select(
            "What would you like to do?",
            choices=choices,
        ).ask()

        if action == "back" or action is None:
            break
        elif action == "install":
            agent_choices = [
                questionary.Choice(f"{a['name']} - {a['description']}", value=aid)
                for aid, a in AGENTS.items()
            ]
            agent_choices.append(questionary.Choice("Back", value=None))

            agent_id = questionary.select(
                "Select agent to install/update:",
                choices=agent_choices,
            ).ask()

            if agent_id:
                agent = AGENTS[agent_id]
                console.print(f"\n[cyan]Installing {agent['name']}...[/cyan]")
                code, _ = run_command(agent["install_cmd"])
                if code == 0:
                    console.print(f"[green]{agent['name']} installed successfully![/green]")
                else:
                    console.print(f"[red]Failed to install {agent['name']}[/red]")
                input("\nPress Enter to continue...")

        elif action == "configure":
            # Let user run agent-specific setup
            agent_choices = [
                questionary.Choice(f"{a['name']}", value=aid)
                for aid, a in AGENTS.items()
                if is_agent_installed(aid)
            ]
            if not agent_choices:
                console.print("[yellow]No agents installed. Install an agent first.[/yellow]")
                input("\nPress Enter to continue...")
                continue

            agent_choices.append(questionary.Choice("Back", value=None))

            agent_id = questionary.select(
                "Select agent to configure:",
                choices=agent_choices,
            ).ask()

            if agent_id:
                console.print(f"\n[cyan]Launching {AGENTS[agent_id]['name']} configuration...[/cyan]")
                console.print("[dim]Follow the agent's prompts to configure.[/dim]\n")
                # Run agent interactively for configuration
                os.system(agent_id)


def menu_takopi():
    """Takopi configuration menu."""
    while True:
        console.print()
        console.print(Panel("Takopi Configuration", style="cyan"))

        takopi_config = Path.home() / ".takopi" / "takopi.toml"
        config_exists = takopi_config.exists()

        if config_exists:
            console.print(f"[green]Config found:[/green] {takopi_config}")
        else:
            console.print("[yellow]No configuration found[/yellow]")

        choices = [
            questionary.Choice("Run takopi wizard (interactive setup)", value="wizard"),
            questionary.Choice("View current config", value="view"),
            questionary.Choice("Test connection", value="test"),
            questionary.Choice("Back to main menu", value="back"),
        ]

        action = questionary.select(
            "What would you like to do?",
            choices=choices,
        ).ask()

        if action == "back" or action is None:
            break
        elif action == "wizard":
            console.print("\n[cyan]Launching takopi wizard...[/cyan]\n")
            os.system("takopi wizard")
            input("\nPress Enter to continue...")
        elif action == "view":
            if config_exists:
                console.print()
                console.print(takopi_config.read_text())
            else:
                console.print("[yellow]No config to view. Run wizard first.[/yellow]")
            input("\nPress Enter to continue...")
        elif action == "test":
            console.print("\n[cyan]Testing takopi connection...[/cyan]")
            code, output = run_command("takopi ping", capture=True)
            if code == 0:
                console.print("[green]Connection successful![/green]")
            else:
                console.print(f"[red]Connection failed: {output}[/red]")
            input("\nPress Enter to continue...")


def menu_plugins():
    """Plugin installation menu."""
    while True:
        console.print()
        console.print(Panel("Plugin Management", style="cyan"))

        choices = [
            questionary.Choice("Install plugin from PyPI", value="pip"),
            questionary.Choice("Install plugin from Git URL", value="git"),
            questionary.Choice("Back to main menu", value="back"),
        ]

        action = questionary.select(
            "What would you like to do?",
            choices=choices,
        ).ask()

        if action == "back" or action is None:
            break
        elif action == "pip":
            package = questionary.text(
                "Enter PyPI package name:",
                validate=lambda x: len(x.strip()) > 0,
            ).ask()

            if package:
                console.print(f"\n[cyan]Installing {package}...[/cyan]")
                code, _ = run_command(f"uv tool install -U {package}")
                if code == 0:
                    console.print(f"[green]{package} installed successfully![/green]")
                else:
                    console.print(f"[red]Failed to install {package}[/red]")
                input("\nPress Enter to continue...")

        elif action == "git":
            url = questionary.text(
                "Enter Git repository URL:",
                validate=lambda x: x.startswith(("http://", "https://", "git://")),
            ).ask()

            if url:
                console.print(f"\n[cyan]Installing from {url}...[/cyan]")
                # Clone to temp and install
                import tempfile
                with tempfile.TemporaryDirectory() as tmpdir:
                    plugin_dir = os.path.join(tmpdir, "plugin")
                    code, _ = run_command(f"git clone --depth 1 {url} {plugin_dir}")
                    if code == 0:
                        code, _ = run_command(f"uv tool install -U {plugin_dir}")
                        if code == 0:
                            console.print("[green]Plugin installed successfully![/green]")
                        else:
                            console.print("[red]Failed to install plugin[/red]")
                    else:
                        console.print("[red]Failed to clone repository[/red]")
                input("\nPress Enter to continue...")


def menu_packages():
    """System package installation menu."""
    while True:
        console.print()
        console.print(Panel("System Package Management", style="cyan"))

        choices = [
            questionary.Choice("Install system packages", value="install"),
            questionary.Choice("Search for packages", value="search"),
            questionary.Choice("Back to main menu", value="back"),
        ]

        action = questionary.select(
            "What would you like to do?",
            choices=choices,
        ).ask()

        if action == "back" or action is None:
            break
        elif action == "install":
            packages = questionary.text(
                "Enter package names (comma-separated):",
                validate=lambda x: len(x.strip()) > 0,
            ).ask()

            if packages:
                pkg_list = " ".join(p.strip() for p in packages.split(",") if p.strip())
                console.print(f"\n[cyan]Installing: {pkg_list}[/cyan]")
                code, _ = run_command(f"sudo apt-get update && sudo apt-get install -y {pkg_list}")
                if code == 0:
                    console.print("[green]Packages installed successfully![/green]")
                else:
                    console.print("[red]Failed to install packages[/red]")
                input("\nPress Enter to continue...")

        elif action == "search":
            query = questionary.text(
                "Enter search term:",
                validate=lambda x: len(x.strip()) > 0,
            ).ask()

            if query:
                console.print(f"\n[cyan]Searching for {query}...[/cyan]\n")
                run_command(f"apt-cache search {query} | head -20")
                input("\nPress Enter to continue...")


def menu_start_agent():
    """Start a specific agent."""
    console.print()
    console.print(Panel("Start Agent", style="cyan"))

    # Only show installed agents
    status = get_agent_status()
    agent_choices = [
        questionary.Choice(f"{AGENTS[aid]['name']}", value=aid)
        for aid, installed in status.items()
        if installed
    ]

    if not agent_choices:
        console.print("[yellow]No agents installed. Install an agent first.[/yellow]")
        input("\nPress Enter to continue...")
        return

    agent_choices.append(questionary.Choice("Back", value=None))

    agent_id = questionary.select(
        "Select agent to start:",
        choices=agent_choices,
    ).ask()

    if agent_id:
        console.print(f"\n[cyan]Starting {AGENTS[agent_id]['name']}...[/cyan]\n")
        os.system(agent_id)


def main_menu():
    """Main menu loop."""
    while True:
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]takopi-docker[/bold cyan]\n"
            "[dim]Interactive configuration tool[/dim]",
            border_style="cyan",
        ))

        show_status()

        choices = [
            questionary.Choice("Agents - Install and configure AI coding agents", value="agents"),
            questionary.Choice("Takopi - Configure takopi settings", value="takopi"),
            questionary.Choice("Plugins - Install takopi plugins", value="plugins"),
            questionary.Choice("Packages - Install system packages", value="packages"),
            questionary.Choice("Start - Launch an agent directly", value="start"),
            questionary.Choice("Exit", value="exit"),
        ]

        action = questionary.select(
            "What would you like to do?",
            choices=choices,
        ).ask()

        if action == "exit" or action is None:
            console.print("\n[cyan]Goodbye![/cyan]\n")
            break
        elif action == "agents":
            menu_agents()
        elif action == "takopi":
            menu_takopi()
        elif action == "plugins":
            menu_plugins()
        elif action == "packages":
            menu_packages()
        elif action == "start":
            menu_start_agent()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(0)
