# v4 UI STATUS - BRAND NEW
# ************************

import os

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QStyle


ICON_DIRECTORY = os.path.join("../icons")
ICON_FILE_EXTENSION = ".png"


# Open, Info, Directory, Options, Exit


class Actions:
    def __init__(self, style: QStyle):
        self._style = style
        assert os.path.isdir(ICON_DIRECTORY)

        # REAL
        self.open_file = QAction("Open")
        self.open_file.setShortcut("Ctrl+O")
        self.open_file.setStatusTip("Open log file(s)")
        self.open_file.setIcon(self.get_custom_icon("open_file"))

        self.file_info = QAction("Info")
        self.file_info.setShortcut("Ctrl+I")
        self.file_info.setStatusTip("Get information about the currently open log file(s)")
        self.file_info.setIcon(self.get_custom_icon("file_info"))

        self.change_log_directory = QAction("Directory")
        self.change_log_directory.setShortcut("Ctrl+D")
        self.change_log_directory.setStatusTip("Change log file source directory")
        self.change_log_directory.setIcon(self.get_custom_icon("change_log_directory"))

        self.set_file_options = QAction("Options")
        self.set_file_options.setStatusTip("Set special options for opening log file(s)")

        self.exit = QAction("Exit")
        self.exit.setStatusTip("Exit application")

        # Example of how to set a standard icon when I need to ....

        #         self.change_log_directory.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_DirIcon))

    @staticmethod
    def get_custom_icon(icon_name: str):
        file_path = os.path.join(ICON_DIRECTORY, icon_name + ".png")
        assert os.path.isfile(file_path)
        return QIcon(file_path)
