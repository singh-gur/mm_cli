from pathlib import Path

import click
from monarchmoney import MonarchMoney

CONFIG_DIR = Path.home() / ".config" / "mm-cli"
TOKEN_FILE = CONFIG_DIR / "token"


@click.group()
def auth():
    """Authentication commands"""
    pass


@auth.command()
@click.option("--email", prompt=True, help="Your MonarchMoney email")
@click.option("--password", prompt=True, hide_input=True, help="Your MonarchMoney password")
def login(email, password):
    """Login to MonarchMoney and save authentication token"""
    try:
        mm = MonarchMoney()
        mm.login(email, password)

        # Save token
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(mm.token)

        click.echo("✓ Successfully logged in and saved token")
    except Exception as e:
        click.echo(f"✗ Login failed: {e}", err=True)
        raise click.Abort()


@auth.command()
def logout():
    """Remove saved authentication token"""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        click.echo("✓ Logged out successfully")
    else:
        click.echo("No saved token found")


@auth.command()
def status():
    """Check authentication status"""
    if TOKEN_FILE.exists():
        click.echo("✓ Authenticated (token found)")
    else:
        click.echo("✗ Not authenticated")


def get_authenticated_client():
    """Get authenticated MonarchMoney client"""
    if not TOKEN_FILE.exists():
        click.echo("✗ Not authenticated. Run 'mm-cli auth login' first.", err=True)
        raise click.Abort()

    with open(TOKEN_FILE) as f:
        token = f.read().strip()

    mm = MonarchMoney()
    mm.token = token
    return mm
