import click

from task_tracker.data.db import Session


@click.group()
def tasks():
    pass


@tasks.command()
def drop_db():
    """Drop database"""
    from task_tracker.data.base import Base

    Base.metadata.drop_all()


@tasks.command()
def init_db():
    """Initialize database"""
    from task_tracker.data.base import Base

    Base.metadata.create_all()


@tasks.command()
def load_data():
    """Load sample data."""
    from task_tracker.data.test_data import USER, TASKS
    from task_tracker.data.user_model import User, Task

    with Session() as session:
        for user in USER:
            session.add(User(**user))
        for task in TASKS:
            session.add(Task(**task))
        session.commit()

    print("sample data loaded.")
