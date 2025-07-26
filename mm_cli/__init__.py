import click

from mm_cli.commands import auth, export


@click.group()
@click.version_option()
def cli():
    """MonarchMoney CLI - Extract data to CSV files"""
    pass


cli.add_command(auth.auth)
cli.add_command(export.export)
