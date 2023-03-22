import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QApplication, QProgressBar, QFileDialog

from src.log.log import Log
from src.configuration.config_manager import ConfigManager
from src.ui.actions import Actions
from src.ui.menubar import MenuBarManager
from src.ui.please_wait import PleaseWait
from src.ui.toolbar import ToolBarManager
from src.graphics.track_analysis_canvas import TrackAnalysisCanvas
from src.tracks.tracks import get_all_tracks
from src.ui.open_file_dialog import OpenFileDialog
from ui.icons import get_custom_icon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #
        # First of all, get config manager up and running so that we have access to any settings that it manages for us
        #
        self._config_manager = ConfigManager()

        # PROTOTYPE FROM HERE

        self.setMinimumSize(200, 200)
        self.resize(1000, 800)
        self.setWindowTitle("DeepRacer Guru")
        self.setWindowIcon(get_custom_icon("window_icon"))

        # Status Bar
        self._please_wait = PleaseWait(self.statusBar())

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

        # Internal variable(s) to communicate from dialogs to main after they are closed
        self._open_file_dialog_chosen_files = None

        # Main variables to keep details of current open logs etc.
        self._log: Log | None = None
        self._current_model_ui_title = ""

        # Canvas etc. comments TODO

        self.canvas = TrackAnalysisCanvas()
        self.setCentralWidget(self.canvas)
        self.make_status_bar_tall_enough_to_contain_progress_bar()

        self.show()

        # Initialise tracks & draw here temporarily to prove everything works or not

        self._tracks = get_all_tracks()
        self._current_track = self._tracks["arctic_pro_cw"]
        self._current_track.configure_track_canvas(self.canvas)

        track_grey = QColor(75, 75, 75)
        grid_grey = QColor(45, 45, 45)

        self._current_track.draw_track_edges(self.canvas, track_grey)
        self._current_track.draw_waypoints(self.canvas, track_grey, 2, 8)
        self._current_track.draw_section_highlight(self.canvas, track_grey, 0, 20)
        self._current_track.draw_starting_line(self.canvas, track_grey)
        self._current_track.draw_sector_dividers(self.canvas, track_grey)
        self._current_track.draw_waypoint_labels(self.canvas, track_grey, 9)
        self._current_track.draw_grid(self.canvas, grid_grey)

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
        dlg = OpenFileDialog(self, self._please_wait, self._current_track, self._config_manager.get_log_directory(), self._chosen_open_file_callback)
        if not dlg.exec():
            print("Cancelled dialog")
            return

        self._current_model_ui_title = self._open_file_dialog_chosen_model_title
        self.setWindowTitle(self._current_model_ui_title)

        self._log = Log(self._config_manager.get_log_directory())
        self._log.load_all(self._open_file_dialog_chosen_files, self._please_wait, self._current_track,
                           self._config_manager.get_calculate_new_reward(),
                           self._config_manager.get_calculate_alternate_discount_factors())

    def _chosen_open_file_callback(self, file_names, model_title):
        self._open_file_dialog_chosen_files = file_names
        self._open_file_dialog_chosen_model_title = model_title

    def _action_file_info(self):
        print("DEBUG FILE INFO")
        print("Title / Model Name =", self._current_model_ui_title)
        print("Log directory =", self._log.get_log_directory())
        print("Log filename(s) =", self._log.get_log_file_name())
        print("Log meta filename(s) =", self._log.get_meta_file_name())

    def _action_change_log_directory(self):
        new_directory = QFileDialog.getExistingDirectory(self, self._actions.change_log_directory.statusTip(), self._config_manager.get_log_directory())
        if new_directory != "":
            self._config_manager.set_log_directory(new_directory)
            # self.menu_bar.refresh()   # TODO - Equivalent in new UI is to be determined

    def _action_set_file_options(self):
        print("File Options - NOT IMPLEMENTED YET IN VERSION 4")

    def _action_exit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication([])

    # app.setStyleSheet("QLabel { color: red }   QProgressBar::chunk { background-color: blue }")

    window = MainWindow()
    sys.exit(app.exec())
