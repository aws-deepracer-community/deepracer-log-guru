# v4 UI STATUS - BRAND NEW
# ************************

from PyQt6.QtWidgets import QToolBar

from src.ui.actions import Actions


class ToolBarManager:
    def __init__(self, tool_bar: QToolBar, actions: Actions):
        self._toolbar = tool_bar
        self._actions = actions
        self.setup_tool_bar()

    def setup_tool_bar(self):
        self._toolbar.addAction(self._actions.change_directory)

        self._toolbar.addAction(self._actions.file_new)
        self._toolbar.addAction(self._actions.file_open)
        self._toolbar.addAction(self._actions.file_save)
        self._toolbar.addAction(self._actions.file_save_as)
