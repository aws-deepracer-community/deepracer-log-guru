import sys
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QProgressBar

from prototype_ui.actions import Actions
from prototype_ui.menubar import MenuBarManager
from prototype_ui.toolbar import ToolBarManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(200, 200)
        self.resize(500, 400)
        self.setWindowTitle("Example")

        # Status Bar
        self._status_bar_label = QLabel("Hello Status Bar")
        self._status_bar_progress = QProgressBar()
        self._status_bar_progress.setRange(0, 10)
        self._status_bar_progress.setValue(7)
        self.statusBar().addPermanentWidget(self._status_bar_label)
        self.statusBar().addPermanentWidget(self._status_bar_progress)

        # Define UI actions
        self._actions = Actions(self.style())

        # Menu & Tool bars
        self._menu_bar_manager = MenuBarManager(self.menuBar(), self._actions)
        self._tool_bar_manager = ToolBarManager(self.addToolBar("Main"), self._actions)

        # Connect actions with callback methods to implement them
        self._actions.file_new.triggered.connect(self._new_file)
        self._actions.file_open.triggered.connect(self._open_file)

        self.canvas = QLabel("Hello")
        self.setCentralWidget(self.canvas)

        self.show()

    def _new_file(self):
        print("New File")
        self.statusBar().showMessage("Hello Briefly", 5000)    # 5 secs

    def _open_file(self):
        self.canvas.setCursor(Qt.CursorShape.CrossCursor)


if __name__ == '__main__':
    app = QApplication([])

    # app.setStyleSheet("QLabel { color: red }   QProgressBar::chunk { background-color: blue }")

    window = MainWindow()
    sys.exit(app.exec())
