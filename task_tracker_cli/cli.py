import click

from task_tracker.data.db import engine
from task_tracker.data.db import Session


@click.group()
def tasks():
    pass


@tasks.command()
def drop_db():
    """Drop database"""
    from task_tracker.data.model import Base

    Base.metadata.drop_all(engine)
    click.echo("Database dropped.")


@tasks.command()
def init_db():
    """Initialize database"""
    from task_tracker.data.model import Base

    Base.metadata.create_all(engine)
    click.echo("Database initialized.")


@tasks.command()
def load_data():
    """Load sample data."""
    from task_tracker.data.test_data import USER, TASKS
    from task_tracker.data.model import User, Task

    with Session() as session:
        for user in USER:
            session.add(User(**user))
        for task in TASKS:
            session.add(Task(**task))
        session.commit()

    click.echo("sample data loaded.")


@tasks.command()
@click.option("-p", "--pass", 'password')
@click.argument("username")
def run(username, password):
    from task_tracker.main import handle_user
    from task_tracker.data.model import User
    # User connection
    response = handle_user(username, password)
    current_user = response["user"]
    if current_user:
        click.echo(f"Welcome {current_user.username}!")
    else:
        click.echo("User not found.")
    # Actions based on user current tasks

    # Report and exit || perform another action
    click.echo("Goodbye!")


