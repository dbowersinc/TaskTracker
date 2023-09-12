
class Option:
    """
    Option is a single option object to be used in a list of options.
    Action is a callback function to be executed when the option is selected.
    """

    def __init__(self, summary, description, action, confirm=False, **kwargs):
        self.summary = summary
        self.description = description
        self.action = action
        self.params = kwargs
        self.confirm = confirm

    def execute_action(self, **kwargs):
        """Execute the action."""
        self.action(**kwargs, **self.params)

    def __repr__(self):
        return f"<Option(description={self.summary!r}, action={self.action!r})>"