from task_tracker.menus.option import Option


class Menu:
    """
    Options is to be used to create an option menu for the user.
    Describe and option and assign it an action.
    It will deliver a list of options to be plugged into your application.
    """
    OPTIONS_MAIN = [Option("Cancel", "cancel", lambda **kwargs: print("Cancelled."), False)]

    def __init__(self, title, intro, options_list: list[Option], parent_menu=None):
        self.title = title
        self.intro = intro
        self.options_list = Menu.OPTIONS_MAIN + options_list
        self.options_menu = self.create_options_menu()
        self.parent_menu = parent_menu

    def create_options_menu(self):
        """Create the options menu."""
        options_menu = []
        for idx, option in enumerate(self.options_list):
            options_menu.append(f"{idx}. {option.summary}")
        return options_menu

    def get_confirm_statement(self, idx: int):
        stmt = f"Confirm: {self.options_list[idx].description} (y/n) "
        return stmt

    def select_option(self, idx: int, **kwargs):
        """Select an option."""
        self.options_list[idx].execute_action(**kwargs)

    def add_option(self, option: Option):
        self.options_list.append(option)
        self.options_menu = self.create_options_menu()

    def change_top_option(self, option: Option):
        self.options_list[0] = option
        self.options_menu = self.create_options_menu()

    def __repr__(self):
        return f"<Option(description={self.description!r}, action={self.action!r})>"

