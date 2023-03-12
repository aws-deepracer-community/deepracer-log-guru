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
        self._toolbar.addAction(self._actions.open_file)
        self._toolbar.addAction(self._actions.file_info)
        self._toolbar.addAction(self._actions.change_log_directory)
