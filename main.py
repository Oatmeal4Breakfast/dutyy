import asyncio
import click
import functools
import uuid
from datetime import datetime, UTC

from src.models.entities import Task, TaskRepo
from src.models.schemas import TaskStatus
from src.db import init_db, get_db


def async_command(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return asyncio.run(fn(*args, **kwargs))

    return wrapper


def print_dutyys(tasks: list[Task]) -> None:
    click.secho(message="=" * 30, fg="yellow", color=True)
    for task in tasks:
        click.secho(
            message=f"Task: {task.name}\nDetails: {task.details}\nStatus: {task.status}\n",
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
            name=name,
            details=details,
            created_at=datetime.now(UTC),
            status=TaskStatus.INCOMPLETE,
        )
        await repo.add(task)
        click.secho(
            message=f"Dutyy with name: {task.name} added...", fg="blue", color=True
        )


@cli.command(name="list")
@click.option("--all", default=False, help="option to filter by incomplete or all")
@async_command
async def list_tasks(all) -> None:
    async for session in get_db():
        repo = TaskRepo(session)
        results: list = []
        if all:
            results: list[Task] = await repo.get_all()
            incomplete = [t for t in results if t.status == TaskStatus.INCOMPLETE]
            print_dutyys(results)
            click.secho(
                message=f"Incomplete dutyys: {len(incomplete)} | Total dutyys: {len(results)} | Percentage Complete: {((len(results) - len(incomplete)) / len(results)) * 100}%",
                fg="green",
                color=True,
            )
        else:
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
        tasks: list[Task] = await repo.search_by_name(name)

        if not tasks:
            raise click.UsageError(f"Could not retrieve task with name: {name}")

        if len(tasks) > 1:
            for idx, task in enumerate(tasks):
                click.echo(message=f"{idx + 1}. {task.name}")
            selected_task = int(
                click.prompt(text="More than one result found. Please select")
            )

            if (selected_task - 1) not in range(0, len(tasks)):
                raise click.UsageError("Selection out of range")

            task = tasks[selected_task - 1]
        else:
            task = tasks[0]

        if task.status == TaskStatus.COMPLETE:
            return

        task.status: str = TaskStatus.COMPLETE
        task.completed_at: datetime = datetime.now(tz=UTC)
        await repo.update(task)


if __name__ == "__main__":
    cli()
