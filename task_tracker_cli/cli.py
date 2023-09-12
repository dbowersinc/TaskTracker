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
    from task_tracker.data.model import User, Task
    from task_tracker.taskshandler import TasksHandler
    from task_tracker.menus.menu import Menu
    from sqlalchemy import select
    running = True


    while running:
        # User connection
        with Session() as session:
            response = handle_user(session, username, password)
            current_user = response["user"]
            if current_user:
                click.echo(f"Welcome {current_user.username}!")
                # User logged in, is there a current task?
                if current_user.user_current_tasks:
                    click.echo(f"Current task: {current_user.user_current_tasks.description}")
                    states_handler = TasksHandler([current_user.current_task], current_user)
                    state_options = Menu("Task State", "Select a state for the current task.",
                                         states_handler.get_state_options())
                    display_menu(state_options, session)

                else:
                    click.echo("No current task. Delivering list of tasks.")
                    # Get list of tasks marked todo.
                    todo_tasks = session.scalars(select(Task).where(Task.state == "todo")).all()
                    tasks_handler = TasksHandler(todo_tasks, current_user)
                    tasks_menu = Menu("Tasks", "Select a task to work on.", tasks_handler.get_task_options())
                    display_menu(tasks_menu, session)
                    # click.echo(f"{tasks_menu.title}\n{tasks_menu.intro}")
                    # for option in tasks_menu.options_menu:
                    #     click.echo(f"{option}")
                    # TODO: Accept string input to enter a new task.
                    # TODO: A option to enter a new task.

            else:
                click.echo("User not found.")
            session.commit()

        # publish action report and prompt for another action

        # If user selects exit then running is False
        running = False

        # Save the user and password to environment variables if running is True.


    # Report and exit || perform another action
    click.echo("Goodbye!")


def display_menu(menu, session):
    click.echo(f"{menu.title}\n{menu.intro}")
    for option in menu.options_menu:
        click.echo(f"{option}")
    request_idx = click.prompt("Make selection", type=int)
    result = menu.select_option(idx=request_idx, session=session)
    return result
