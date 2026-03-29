import asyncio

from src.models.entities import TaskStatus, Task, TaskRepo
from src.db import init_db, get_db


def main():
    print("Hello from dutyy!")

    asyncio.run(init_db())


if __name__ == "__main__":
    main()
