from PyQt6.QtWidgets import QMenuBar

from prototype_ui.actions import Actions


class MenuBarManager:
    def __init__(self, menu_bar: QMenuBar, actions: Actions):
        self._menu_bar = menu_bar
        self._actions = actions
        self.setup_menu_bar()

    def setup_menu_bar(self):
        self._create_file_menu()

    def _create_file_menu(self):
        menu = self._menu_bar.addMenu("File")
        menu.addAction(self._actions.change_directory)
        menu.addSeparator()
        menu.addAction(self._actions.file_new)
        menu.addAction(self._actions.file_open)
        menu.addSeparator()
        menu.addAction(self._actions.file_save)
        menu.addAction(self._actions.file_save_as)
