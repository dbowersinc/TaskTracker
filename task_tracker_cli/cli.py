import click

from task_tracker.data.db import engine
from task_tracker.data.db import Session
from task_tracker.taskshandler import TasksHandler
from task_tracker.data.model import User, Task



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


    from task_tracker.menus.menu import Menu
    from task_tracker.menus.option import Option
    from sqlalchemy import select
    running = True

    while running:
        # User connection
        with Session() as session:
            find_user = handle_user(session, username, password)
            click.echo(find_user["status"])
            current_user = find_user["user"]

            if current_user:
                click.echo(f"Welcome {current_user.username}!")
                # User logged in, is there a current task?
                if current_user.current_task:
                    task = current_user.current_task
                    click.echo(f"Current task: {task.description}")
                    states_handler = TasksHandler(user=current_user)
                    state_options = Menu(
                        title="Task State",
                        intro="Select a state for the current task.",
                        options_list=states_handler.generate_state_options()
                    )
                    state_options.add_option(Option("Cancel", "cancel", lambda **kwargs: click.echo("Cancelled."), False))
                    display_menu(state_options, session)

                else:
                    click.echo("No current task. Tasks listed from backlog.")
                    # Get list of tasks marked todo.
                    todo_tasks = session.scalars(select(Task).where(Task.state == "todo")).all()
                    for_approval_tasks = session.scalars(select(Task).where(Task.state == "for_approval")).all()
                    paused_tasks = session.scalars(select(Task).where(Task.state == "paused")).all()
                    done_tasks = session.scalars(select(Task).where(Task.state == "done")).all()

                    tasks_handler = TasksHandler(user=current_user, tasks=todo_tasks)
                    todo_options = tasks_handler.get_todo_task_options()
                    print(todo_options)
                    tasks_menu = Menu(
                        title="Tasks",
                        intro="Select a task to work on.",
                        options_list=todo_options)

                    # list tasks for review
                    if for_approval_tasks:

                        for_approval_handler = TasksHandler(user=current_user, tasks=for_approval_tasks)
                        for_approval_menu = Menu(
                            title="Tasks for Approval",
                            intro="Select a task to review.",
                            options_list=for_approval_handler.get_for_approval_task_options(),
                            parent_menu=tasks_menu)
                        for_approval_menu.change_top_option(Option(
                            "Back",
                            "back to main menu",
                            lambda session: display_menu(for_approval_menu.parent_menu, session), False))

                        tasks_menu.add_option(Option(
                            "List tasks for_review",
                            "list tasks for review",
                            lambda session: display_menu(for_approval_menu, session),
                        ))

                    # list tasks paused
                    if paused_tasks:

                        paused_tasks_handler = TasksHandler(user=current_user, tasks=paused_tasks)
                        paused_tasks_menu = Menu(
                            title="Paused Tasks",
                            intro="Select a task to resume.",
                            options_list=paused_tasks_handler.get_paused_task_options(),
                            parent_menu=tasks_menu)
                        paused_tasks_menu.change_top_option(Option(
                            "Back",
                            "back to main menu",
                            lambda session: display_menu(paused_tasks_menu.parent_menu, session), False))

                        tasks_menu.add_option(Option(
                            "List paused tasks",
                            "list paused tasks",
                            lambda session: display_menu(paused_tasks_menu, session),
                        ))

                    # Add menu option to create task.
                    tasks_menu.add_option(Option(
                        summary="Create new task",
                        description="create new task",
                        action=lambda session: create_new_task(this_session=session, user=current_user),
                        confirm=False
                        ))

                    display_menu(tasks_menu, session)
                    # # click.echo(f"{tasks_menu.title}\n{tasks_menu.intro}")
                    # # for option in tasks_menu.options_menu:
                    # #     click.echo(f"{option}")
                    # # TODO: Accept string input to enter a new task.
                    # # TODO: A option to enter a new task.

            else:
                click.echo("User not found.")
            session.commit()

        # publish action report and prompt for another action

        # If user selects exit then running is False
        more_tasks = click.prompt("More tasks? (y/n)", type=str)
        if not more_tasks == "y":
            running = False

        # Save the user and password to environment variables if running is True.

    # Report and exit || perform another action
    click.echo("Goodbye!")


def display_menu(menu, session):
    click.echo(f"{menu.title}\n{menu.intro}")
    for option in menu.options_menu:
        click.echo(f"{option}")
    request_idx = click.prompt("Make selection", type=int)
    menu.select_option(idx=request_idx, session=session)


# Create a new task
def create_new_task(this_session, user):
    new_task_handler = TasksHandler(user=user)
    print(type(user))
    task_title = click.prompt("Enter task title", type=str)
    task_description = click.prompt("Enter task description", type=str)
    new_task = Task(title=task_title, description=task_description, state="created")
    with this_session.no_autoflush:
        new_task_handler.create_new_task(this_session, new_task)
        current_task = click.prompt("Task created. Make this your current task? (y/n)", type=str)
        if current_task == "y":
            new_task_handler.set_task_state(this_session, new_task, "in_progress")
            # this_session.add(user)
