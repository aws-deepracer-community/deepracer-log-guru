import sys
import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QProgressBar, QFileDialog

from src.configuration.config_manager import ConfigManager
from src.ui.actions import Actions
from src.ui.menubar import MenuBarManager
from src.ui.please_wait import PleaseWait
from src.ui.toolbar import ToolBarManager
from src.graphics.track_analysis_canvas import TrackAnalysisCanvas
from src.tracks.tracks import get_all_tracks
from src.ui.open_file_dialog import OpenFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #
        # First of all, get config manager up and running so we have access to any settings that it manages for us
        #
        self._config_manager = ConfigManager()

        # PROTOTYPE FROM HERE

        self.setMinimumSize(200, 200)
        self.resize(1800, 400)
        self.setWindowTitle("Example")

        # Status Bar
        self._please_wait = PleaseWait(self.statusBar(), self.set_busy_cursor, self.set_normal_cursor)

        # Define UI actions
        self._actions = Actions(self.style())

        # Menu & Tool bars
        self._menu_bar_manager = MenuBarManager(self.menuBar(), self._actions)
        self._tool_bar_manager = ToolBarManager(self.addToolBar("Main"), self._actions)

        # Connect actions with callback methods to implement them
        self._actions.open_file.triggered.connect(self._action_open_file)
        self._actions.file_info.triggered.connect(self._action_file_info)
        self._actions.change_log_directory.triggered.connect(self._action_change_log_directory)
        self._actions.set_file_options.triggered.connect(self._action_set_file_options)
        self._actions.exit.triggered.connect(self._action_exit)

        # Canvas etc. comments TODO

        self.canvas = TrackAnalysisCanvas()
        self.setCentralWidget(self.canvas)
        self.make_status_bar_tall_enough_to_contain_progress_bar()

        self.show()

        # Initialise tracks & draw here temporarily to prove everything works or not

        self._tracks = get_all_tracks()
        self._current_track = self._tracks["arctic_pro_cw"]
        self._current_track.configure_track_canvas(self.canvas)
        # self.canvas.set_track_area(TrackArea(0, 0, 10, 10))
        self._current_track.draw_track_edges(self.canvas, Qt.GlobalColor.red)
        self._current_track.draw_waypoints(self.canvas, Qt.GlobalColor.blue, 2, 5)

    def set_busy_cursor(self):
        self.setCursor(Qt.CursorShape.WaitCursor)

    def set_normal_cursor(self):
        self.unsetCursor()

    def make_status_bar_tall_enough_to_contain_progress_bar(self):
        dummy_sizing_progress_bar = QProgressBar()
        self.statusBar().addPermanentWidget(dummy_sizing_progress_bar)
        h = self.statusBar().geometry().height()
        self.statusBar().removeWidget(dummy_sizing_progress_bar)
        self.statusBar().setMinimumHeight(h)

    def _action_open_file(self):
        dlg = OpenFileDialog(self, self._please_wait, self._current_track, self._config_manager.get_log_directory())
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")

    def _action_file_info(self):
        print("File Info - NOT IMPLEMENTED YET IN VERSION 4")

    def _action_change_log_directory(self):
        new_directory = QFileDialog.getExistingDirectory(self, self._actions.change_log_directory.statusTip(), self._config_manager.get_log_directory())
        if new_directory != "":
            self._config_manager.set_log_directory(new_directory)
            # self.menu_bar.refresh()   # TODO - Equivalent in new UI is to be determined

    def _action_set_file_options(self):
        print("File Options - NOT IMPLEMENTED YET IN VERSION 4")

    def _action_exit(self):
        print("File Exit - NOT IMPLEMENTED YET IN VERSION 4")


if __name__ == '__main__':
    app = QApplication([])

    # app.setStyleSheet("QLabel { color: red }   QProgressBar::chunk { background-color: blue }")

    window = MainWindow()
    sys.exit(app.exec())
