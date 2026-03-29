import asyncio
import click
import functools
import uuid
from datetime import datetime, UTC

from src.models.entities import Task, TaskRepo
from src.models.schemas import TaskStatus, TaskModel
from src.db import init_db, get_db


def async_command(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return asyncio.run(fn(*args, **kwargs))

    return wrapper


def print_dutyys(tasks: list[Task]) -> None:
    for task in tasks:
        click.secho(
            message=f"Task: {task.name}\nDetails: {task.details}\nStatus: {task.status}",
            fg="yellow",
            color=True,
        )


@click.group()
def cli() -> None:
    pass


@cli.command(name="init")
@async_command
async def init() -> None:
    await init_db()
    click.secho("Database initialized...", fg="yellow", color=True)


@cli.command(name="add")
@click.argument("name")
@click.option("--details", help="details about the task")
@async_command
async def add_dutyy(name: str, details: str) -> None:
    async for session in get_db():
        repo = TaskRepo(session)
        task = Task(
            id=uuid.uuid7(),
            name=name,
            details=details,
            created_at=datetime.now(UTC),
            status=TaskStatus.INCOMPLETE,
        )
        await repo.add(task)
        click.secho(message=f"{task.name} added...", fg="blue", color=True)


@cli.command(name="list")
@click.option("--all", default=False, help="option to filter by incomplete or all")
@async_command
async def list_tasks(all) -> None:
    async for session in get_db():
        repo = TaskRepo(session)
        if all:
            results: list[Task] = await repo.get_all()
            print_dutyys(results)

        results: list[Task] = await repo.get_all_incomplete()
        print_dutyys(results)


@cli.command(name="complete")
@click.argument("name")
@click.option("--status", default="complete")
@async_command
async def mark_complete(name, status):
    async for session in get_db():
        repo = TaskRepo(session)
        click.echo(name)
        task = await repo.get_by_name(name)
        if task is None:
            raise ValueError(f"Could not retrieve task with name {name}")

        if task.status == "complete":
            return

        task.status: str = status
        await repo.update(task)


if __name__ == "__main__":
    cli()
