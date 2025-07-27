from click import Group, Command


def add_commands(cli: Group):
    """Add commands to the CLI group."""
    # dynamically import all commands from the commands directory
    import pkgutil

    from mm_cli import commands

    for _, name, _ in pkgutil.iter_modules(commands.__path__):
        module = __import__(f"mm_cli.commands.{name}", fromlist=[name])
        if hasattr(module, name) and isinstance(getattr(module, name), Group | Command):
            cli.add_command(getattr(module, name))
        elif hasattr(module, "commands") and isinstance(module.commands, list):
            for command in module.commands:
                cli.add_command(command) if isinstance(
                    command, Group | Command
                ) else None

    return cli
