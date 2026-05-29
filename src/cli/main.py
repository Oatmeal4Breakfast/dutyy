import click

from src.cli.commands.tasks import (
    init,
    add_dutyy,
    list_tasks,
    mark_complete,
)


@click.group()
def cli() -> None:
    pass


cli.add_command(init)
cli.add_command(add_dutyy)
cli.add_command(list_tasks)
cli.add_command(mark_complete)

if __name__ == "__main__":
    cli()
