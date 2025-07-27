import click

from mm_cli.commands import add_commands


@click.group()
@click.version_option()
def cli():
    """MonarchMoney CLI - Extract data to CSV files"""
    pass


add_commands(cli)
