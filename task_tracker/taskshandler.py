from task_tracker.data.model import Task, User, UserTaskStateRecord
from task_tracker.states import STATES
from task_tracker.menus.option import Option
from sqlalchemy import select

# Return a list of options from tasks
# Provide actions for each option

class TasksHandler:

    def __init__(self, user: User, tasks: list[Task] = None, states=STATES):
        self.user = user
        self.tasks = tasks
        self.states = states

    def get_todo_task_options(self):
        options = self.generate_options("todo")
        return options

    def get_for_approval_task_options(self):
        options = self.generate_options("for_approval")
        return options

    def get_paused_task_options(self):
        # Paused tasks will need to deliver another prompt for in_progress or in_review.
        options = self.generate_options("paused")
        return options

    def create_new_task(self, session, task: Task):
        session.add(task)
        self.record_state_change(session, task, "created")

    def set_task_state(self, session, task: Task, state: str):
        if state == "in_progress" or state == "in_review":
            self.user.current_task = task
            self.user.current_task.state = state
            session.add(self.user)
        else:
            self.user.current_task = None
            task.state = state
            session.add_all([task, self.user])
        self.record_state_change(session, task, state)

    def record_state_change(self, session, task: Task, state: str):
        new_state_record = UserTaskStateRecord(
            user=self.user,
            task=task,
            state=state
        )
        session.add(new_state_record)

    def generate_options(self, state: str):
        options = []
        change_state = list(filter(lambda current_state: state in current_state["follows"], STATES))[0]["state"]

        for idx, task in enumerate(self.tasks):
            options.append(Option(
                summary=task.title,
                description=task.description,
                action=lambda session: self.set_task_state(
                    session,
                    task,
                    change_state
                )))
        return options

    def generate_state_options(self):
        task = self.user.current_task
        current_state = task.state
        options = self.get_current_state_options(current_state, task)

        return options

    def get_current_state_options(self, current_state: str, task):
        options = []
        change_states = list(filter(lambda st: current_state in st["follows"], STATES))
        for state in change_states:
            options.append(Option(
                summary=state["state"],
                description=state["description"],
                action=lambda session: self.set_task_state(
                    session,
                    task,
                    state["state"]
                )))
        return options

    def set_user_current_task(self, session, task: Task):
        self.user.current_tasks = task

        # new_current_task = session.execute(
        #     select(UserCurrentTask).where(UserCurrentTask.user_id == self.user.id)).scalar_one_or_none()
        # if new_current_task:
        #     new_current_task.task_id = task.id
        # else:
        #     current_task = UserCurrentTask(
        #         user=self.user,
        #         task=task
        #     )
        #     session.add(current_task)
        # self.set_task_state(session, task, "in_progress")