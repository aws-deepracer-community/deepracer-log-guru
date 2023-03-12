# v4 UI STATUS - CONVERSION IN PROGRESS
# *************************************

from PyQt6.QtWidgets import QMenuBar

from src.ui.actions import Actions


class MenuBarManager:
    def __init__(self, menu_bar: QMenuBar, actions: Actions):
        self._menu_bar = menu_bar
        self._actions = actions
        self.setup_menu_bar()

    def setup_menu_bar(self):
        self._create_file_menu()

    def _create_file_menu(self):
        menu = self._menu_bar.addMenu("File")
        menu.addAction(self._actions.open_file)
        menu.addAction(self._actions.file_info)
        menu.addAction(self._actions.change_log_directory)
        menu.addSeparator()
        menu.addAction(self._actions.set_file_options)
        menu.addSeparator()
        menu.addAction(self._actions.exit)

