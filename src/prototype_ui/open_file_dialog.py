from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMainWindow, QTableWidget, QGridLayout

from prototype_ui.log_utils import get_model_info_for_open_model_dialog
from prototype_ui.please_wait import PleaseWait
from prototype_ui.track_v4 import Track



class OpenFileDialog(QDialog):
    def __init__(self, parent: QMainWindow, please_wait: PleaseWait, current_track: Track, log_directory: str):
        super().__init__(parent)

        log_info, hidden_log_count = get_model_info_for_open_model_dialog(current_track, log_directory, please_wait)

        self.layout = QGridLayout()

        for i, title in enumerate(["One", "Two", "Three", "Four"]):
            self.layout.addWidget(QLabel(title), 0, i)
        for i in range(1, 3):
            self.layout.addWidget(QLabel("Hello" + str(i)), i, 2)






        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


        message = QLabel("Something happened, is that OK?")
        #self.layout.addLayout(grid)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
