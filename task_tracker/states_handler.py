from task_tracker.taskshandler import TasksHandler
from task_tracker.states import STATES

class StatesHandler:

    def __init__(self, states):
        self.states = states

    def generate_state_options(self, current_state, tasks_handler: TasksHandler):
        options = []
        for state in self.states:
            if state["state"] == current_state:
                continue
            options.append(Option(
                summary=state["state"],
                description=state["description"],
                action=lambda session: self.set_task_state(
                    session,
                    task,
                    state["state"]
                )))
        return options