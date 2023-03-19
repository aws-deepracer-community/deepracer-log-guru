# v4 UI STATUS - CONVERSION IN PROGRESS
# *************************************

#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QMainWindow, QGridLayout, QVBoxLayout, QPushButton

from src.log.log_utils import get_model_info_for_open_model_dialog, OpenFileInfo
from src.ui.please_wait import PleaseWait
from src.tracks.track import Track

from src.personalize.configuration.analysis import TIME_BEFORE_FIRST_STEP
from utils.formatting import get_pretty_whole_percentage, get_pretty_large_integer


class OpenFileDialog(QDialog):
    def __init__(self, parent: QMainWindow, please_wait: PleaseWait, current_track: Track, log_directory: str, chosen_file_callback: callable):
        super().__init__(parent)

        self._chosen_file_callback = chosen_file_callback

        log_info, hidden_log_count = get_model_info_for_open_model_dialog(current_track, log_directory, please_wait)

        all_best_times = []
        all_average_times = []
        all_progress_percent = []
        all_success_percent = []

        show_laps = False
        log: OpenFileInfo
        for log in log_info:
            log_meta = log.log_meta
            if log_meta.average_steps.get() > 0:
                all_best_times.append(log_meta.best_time.get() + TIME_BEFORE_FIRST_STEP)
                all_average_times.append(log_meta.average_time.get() + TIME_BEFORE_FIRST_STEP)
                show_laps = True
            all_progress_percent.append(self._get_progress_percent(log_meta))
            all_success_percent.append(self._get_success_percent(log_meta))

        if len(all_progress_percent) == 0:
            best_progress_percent = 0.0
            best_success_percent = 0.0
        else:
            best_progress_percent = max(all_progress_percent)
            best_success_percent = max(all_success_percent)

        if show_laps:
            best_best_times = min(all_best_times)
            best_average_times = min(all_average_times)
        else:
            best_best_times = None
            best_average_times = None

        self.setWindowTitle("Open Log File")

        log_layout = QGridLayout()
        log_layout.setHorizontalSpacing(15)

        log_layout.addWidget(_make_centred_label("Episodes"), 0, 3)
        log_layout.addWidget(_make_centred_label("Average\nProgress"), 0, 4)
        log_layout.addWidget(_make_centred_label("Full\nLaps"), 0, 5)

        if show_laps:
            log_layout.addWidget(_make_centred_label("Best\nLap"), 0, 6)
            log_layout.addWidget(_make_centred_label("Average\nLap"), 0, 7)

        row = 1
        for log in log_info:
            if len(log.source_files) == 1:
                file_names = log.source_files[0]
            else:
                file_names = log.source_files

            log_meta = log.log_meta

            progress_percent = self._get_progress_percent(log_meta)
            success_percent = self._get_success_percent(log_meta)

            # self._place_in_grid(row, 0, tk.Button(master, text=log.display_name, command=callback), "E")
            button = QPushButton(log.display_name)
            button.setStyleSheet("text-align:left")
            button.clicked.connect(lambda state, x=file_names, y=log.display_name: self._callback_open_file(x, y))  # Magic ?!!?!?!
            log_layout.addWidget(button, row, 0)

            log_layout.addWidget(_make_centred_label(log_meta.race_type.get().name), row, 1)
            log_layout.addWidget(_make_centred_label(log_meta.job_type.get().name), row, 2)
            log_layout.addWidget(self._make_large_integer_label(log_meta.episode_count.get()), row, 3)
            log_layout.addWidget(self._make_percent_label(progress_percent, best_progress_percent), row, 4)
            log_layout.addWidget(self._make_percent_label(success_percent, best_success_percent), row, 5)

            if show_laps:
                log_layout.addWidget(self._make_lap_time_label(log_meta.best_time.get(), best_best_times), row, 6)
                log_layout.addWidget(self._make_lap_time_label(log_meta.average_time.get(), best_average_times), row, 7)

            row += 1


        # SAMPLE CODE

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(log_layout)
        layout.addSpacing(10)
        layout.addWidget(button_box, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _callback_open_file(self, file_names, model_title):
        self._chosen_file_callback(file_names, model_title)
        self.accept()

    @staticmethod
    def _get_progress_percent(log_meta):
        return log_meta.average_percent_complete.get()

    @staticmethod
    def _get_success_percent(log_meta):
        return log_meta.success_count.get() / log_meta.episode_count.get() * 100

    @staticmethod
    def _make_percent_label(value, best_value):
        formatted_text = get_pretty_whole_percentage(value)
        if value >= 0.99 * best_value and value > 0.0:
            return _make_centred_label(formatted_text, "palegreen")
            # return tk.Label(master, text=formatted_text, background="palegreen", justify=tk.CENTER)
        elif value >= 0.97 * best_value and value > 0.0:
            return _make_centred_label(formatted_text, "lightskyblue")
            # return tk.Label(master, text=formatted_text, background="lightblue1", justify=tk.CENTER)
        else:
            return _make_centred_label(formatted_text)
            # return tk.Label(master, text=formatted_text, justify=tk.CENTER)

    @staticmethod
    def _make_large_integer_label(value):
        label = QLabel(get_pretty_large_integer(value))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    @staticmethod
    def _make_lap_time_label(seconds, best_seconds):
        if seconds > 0.0:
            seconds += TIME_BEFORE_FIRST_STEP
            formatted_text = str(round(seconds, 1)) + " s"
        else:
            formatted_text = "---"

        if best_seconds >= 0.99 * seconds and seconds > 0.0:
            return _make_centred_label(formatted_text, "palegreen")
        elif best_seconds >= 0.97 * seconds and seconds > 0.0:
            return _make_centred_label(formatted_text, "lightskyblue")
        else:
            return _make_centred_label(formatted_text)


def _make_centred_label(display_value: str, colour: str = None):
    label = QLabel(display_value)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    if colour is not None:
        label.setStyleSheet("background-color: " + colour)
    return label
