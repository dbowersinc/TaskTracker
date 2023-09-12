from task_tracker.data.model import Task, User, UserCurrentTask, UserTaskStateRecord
from task_tracker.states import STATES
from task_tracker.menus.option import Option


# Return a list of options from tasks
# Provide actions for each option

class TasksHandler:

    def __init__(self, tasks: list[Task], user: User, states=STATES):
        self.tasks = tasks
        self.user = user
        self.states = states

    def get_task_options(self):
        options = []
        change_state = list(filter(lambda current_state: "todo" in current_state["follows"], STATES))[0]["state"]

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

    def set_task_state(self, session, task: Task, state: str):
        task.state = state
        session.add(task)
        self.record_state_change(session, task, state)

    def record_state_change(self, session, task: Task, state: str):
        new_state_record = UserTaskStateRecord(
            user_id=self.user.id,
            task_id=task.id,
            state=state
        )
        new_current_task = UserCurrentTask(
            user_id=self.user.id,
            task_id=task.id
        )
        session.add_all([new_state_record, new_current_task])

    def generate_state_options(self, task: Task):
        options = []
        current_state = self.user.user_current_tasks.task.state
        change_states = list(filter(lambda st: "todo" in st["follows"], STATES))
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
