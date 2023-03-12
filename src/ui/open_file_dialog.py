# v4 UI STATUS - CONVERSION IN PROGRESS
# *************************************

#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QMainWindow, QGridLayout

from src.log.log_utils import get_model_info_for_open_model_dialog, OpenFileInfo
from src.ui.please_wait import PleaseWait
from src.tracks.track import Track

from src.personalize.configuration.analysis import TIME_BEFORE_FIRST_STEP
from utils.formatting import get_pretty_whole_percentage, get_pretty_large_integer


class OpenFileDialog(QDialog):
    def __init__(self, parent: QMainWindow, please_wait: PleaseWait, current_track: Track, log_directory: str):
        super().__init__(parent)

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

        self.layout = QGridLayout()

        # self._place_in_grid(0, 3, tk.Label(master, text="Episodes", justify=tk.CENTER))
        # self._place_in_grid(0, 4, tk.Label(master, text="Average\nProgress", justify=tk.CENTER))
        # self._place_in_grid(0, 5, tk.Label(master, text="Full\nLaps", justify=tk.CENTER))

        self.layout.addWidget(QLabel("Episodes"), 0, 3)
        self.layout.addWidget(QLabel("Average\nProgress"), 0, 4)
        self.layout.addWidget(QLabel("Full\nLaps"), 0, 5)

        if show_laps:
            # self._place_in_grid(0, 6, tk.Label(master, text="Best\nLap", justify=tk.CENTER))
            # self._place_in_grid(0, 7, tk.Label(master, text="Average\nLap", justify=tk.CENTER))

            self.layout.addWidget(QLabel("Best\nLap"), 0, 6)
            self.layout.addWidget(QLabel("Average\nLap"), 0, 7)

        row = 1

        for log in log_info:
            if len(log.source_files) == 1:
                file_names = log.source_files[0]
            else:
                file_names = log.source_files

            # TODO equivalent:
            #   def callback(f=file_names): self._callback_open_file(f)

            log_meta = log.log_meta

            progress_percent = self._get_progress_percent(log_meta)
            success_percent = self._get_success_percent(log_meta)

            self.layout.addWidget(QLabel(log.display_name), row, 0)
            self.layout.addWidget(QLabel(log_meta.race_type.get().name), row, 1)
            self.layout.addWidget(QLabel(log_meta.job_type.get().name), row, 2)

            self.layout.addWidget(self._make_large_integer_label(log_meta.episode_count.get()), row, 3)
            self.layout.addWidget(self._make_percent_label(progress_percent, best_progress_percent), row, 4)
            self.layout.addWidget(self._make_percent_label(success_percent, best_success_percent), row, 5)


            # self._place_in_grid(row, 0, tk.Button(master, text=log.display_name, command=callback), "E")
            # self._place_in_grid(row, 1, tk.Label(master, text=log_meta.race_type.get().name), "E")
            # self._place_in_grid(row, 2, tk.Label(master, text=log_meta.job_type.get().name), "E")
            # self._place_in_grid(row, 3, self._make_large_integer_label(master, log_meta.episode_count.get()))
            # self._place_in_grid(row, 4, self._make_percent_label(master, progress_percent, best_progress_percent))
            # self._place_in_grid(row, 5, self._make_percent_label(master, success_percent, best_success_percent))

            if show_laps:
                self.layout.addWidget(self._make_lap_time_label(log_meta.best_time.get(), best_best_times), row, 6)
                self.layout.addWidget(self._make_lap_time_label(log_meta.average_time.get(), best_average_times), row, 7)

                # self._place_in_grid(row, 6, self._make_lap_time_label(master,
                #                                                       log_meta.best_time.get(),
                #                                                       best_best_times))
                # self._place_in_grid(row, 7, self._make_lap_time_label(master,
                #                                                       log_meta.average_time.get(),
                #                                                       best_average_times))

            row += 1


        # SAMPLE CODE


        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)



        self.layout.addWidget(self.buttonBox, row, 4)
        self.setLayout(self.layout)

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
            return QLabel(formatted_text)
            # return tk.Label(master, text=formatted_text, background="palegreen", justify=tk.CENTER)
        elif value >= 0.97 * best_value and value > 0.0:
            return QLabel(formatted_text)
            # return tk.Label(master, text=formatted_text, background="lightblue1", justify=tk.CENTER)
        else:
            return QLabel(formatted_text)
            # return tk.Label(master, text=formatted_text, justify=tk.CENTER)

    @staticmethod
    def _make_large_integer_label(value):
        # return tk.Label(master, text=get_pretty_large_integer(value), justify=tk.CENTER)
        return QLabel(get_pretty_large_integer(value))

    @staticmethod
    def _make_lap_time_label(seconds, best_seconds):
        if seconds > 0.0:
            seconds += TIME_BEFORE_FIRST_STEP
            formatted_text = str(round(seconds, 1)) + " s"
        else:
            formatted_text = "---"

        if best_seconds >= 0.99 * seconds and seconds > 0.0:
            return QLabel(formatted_text)
            # return tk.Label(master, text=formatted_text, background="palegreen", justify=tk.CENTER)
        elif best_seconds >= 0.97 * seconds and seconds > 0.0:
            return QLabel(formatted_text)
            # return tk.Label(master, text=formatted_text, background="lightblue1", justify=tk.CENTER)
        else:
            return QLabel(formatted_text)
            # return tk.Label(master, text=formatted_text, justify=tk.CENTER)
