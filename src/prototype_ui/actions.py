import os

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QStyle

ICON_DIRECTORY = os.path.join("icons")
ICON_FILE_EXTENSION = ".png"


class Actions:
    def __init__(self, style: QStyle):
        self._style = style
        assert os.path.isdir(ICON_DIRECTORY)

        self.file_new = QAction("New")
        self.file_new.setShortcut("Ctrl+N")
        self.file_new.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowBack))

        self.file_open = QAction("Open")
        self.file_open.setShortcut("Ctrl+O")
        self.file_open.setIcon(self.get_custom_icon("sample_icon"))

        self.file_save = QAction("Save")
        self.file_save.setShortcut("Ctrl+S")
        self.file_save.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon))

        self.file_save_as = QAction("Save As")
        self.file_save_as.setShortcut("Ctrl+A")
        self.file_save_as.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))

    @staticmethod
    def get_custom_icon(icon_name: str):
        file_path = os.path.join(ICON_DIRECTORY, icon_name + ".png")
        assert os.path.isfile(file_path)
        return QIcon(file_path)
