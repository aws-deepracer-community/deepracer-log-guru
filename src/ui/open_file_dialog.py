#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

from src.personalize.configuration.analysis import TIME_BEFORE_FIRST_STEP
from src.ui.dialog import Dialog
from src.log.log_utils import get_model_info_for_open_model_dialog, OpenFileInfo

from src.utils.formatting import get_pretty_whole_percentage, get_pretty_large_integer
from ui.please_wait import PleaseWait


class OpenFileDialog(Dialog):
    def __init__(self, parent, please_wait: PleaseWait):
        self._please_wait = please_wait
        super().__init__(parent, "Open File")

    def body(self, master):
        log_info, hidden_log_count = get_model_info_for_open_model_dialog(self.parent.current_track,
                                                                          self.parent.get_log_directory(),
                                                                          self._please_wait)
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

        self._place_in_grid(0, 3, tk.Label(master, text="Episodes", justify=tk.CENTER))
        self._place_in_grid(0, 4, tk.Label(master, text="Average\nProgress", justify=tk.CENTER))
        self._place_in_grid(0, 5, tk.Label(master, text="Full\nLaps", justify=tk.CENTER))
        if show_laps:
            self._place_in_grid(0, 6, tk.Label(master, text="Best\nLap", justify=tk.CENTER))
            self._place_in_grid(0, 7, tk.Label(master, text="Average\nLap", justify=tk.CENTER))

        row = 1

        for log in log_info:
            file_names = log.source_files[0]
            callback = lambda file_names=file_names: self._callback_open_file(file_names)

            log_meta = log.log_meta

            progress_percent = self._get_progress_percent(log_meta)
            success_percent = self._get_success_percent(log_meta)

            self._place_in_grid(row, 0, tk.Button(master, text=log.display_name, command=callback), "E")
            self._place_in_grid(row, 1, tk.Label(master, text=log_meta.race_type.get().name), "E")
            self._place_in_grid(row, 2, tk.Label(master, text=log_meta.job_type.get().name), "E")

            self._place_in_grid(row, 3, self._make_large_integer_label(master, log_meta.episode_count.get()))

            self._place_in_grid(row, 4, self._make_percent_label(master, progress_percent, best_progress_percent))
            self._place_in_grid(row, 5, self._make_percent_label(master, success_percent, best_success_percent))
            if show_laps:
                self._place_in_grid(row, 6, self._make_lap_time_label(master,
                                                                      log_meta.best_time.get(),
                                                                      best_best_times))
                self._place_in_grid(row, 7, self._make_lap_time_label(master,
                                                                      log_meta.average_time.get(),
                                                                      best_average_times))

            row += 1

        if hidden_log_count > 0:
            if hidden_log_count == 1:
                hidden_text = "Note: One log file is not shown, choose the correct track to see it"
            else:
                hidden_text = "Note: " + str(hidden_log_count) + " log files are not shown, choose other tracks to see them"
            tk.Label(master, text=hidden_text, foreground="red").grid(row=row, column=0, columnspan=6,
                                                                      pady=5, sticky="W")

    @staticmethod
    def _get_progress_percent(log_meta):
        return log_meta.average_percent_complete.get()

    @staticmethod
    def _get_success_percent(log_meta):
        return log_meta.success_count.get() / log_meta.episode_count.get() * 100

    @staticmethod
    def _make_percent_label(master, value, best_value):
        formatted_text = get_pretty_whole_percentage(value)
        if value >= 0.99 * best_value and value > 0.0:
            return tk.Label(master, text=formatted_text, background="palegreen", justify=tk.CENTER)
        elif value >= 0.97 * best_value and value > 0.0:
            return tk.Label(master, text=formatted_text, background="lightblue1", justify=tk.CENTER)
        else:
            return tk.Label(master, text=formatted_text, justify=tk.CENTER)

    @staticmethod
    def _make_lap_time_label(master, seconds, best_seconds):
        if seconds > 0.0:
            seconds += TIME_BEFORE_FIRST_STEP
            formatted_text = str(round(seconds, 1)) + " s"
        else:
            formatted_text = "---"

        if best_seconds >= 0.99 * seconds and seconds > 0.0:
            return tk.Label(master, text=formatted_text, background="palegreen", justify=tk.CENTER)
        elif best_seconds >= 0.97 * seconds and seconds > 0.0:
            return tk.Label(master, text=formatted_text, background="lightblue1", justify=tk.CENTER)
        else:
            return tk.Label(master, text=formatted_text, justify=tk.CENTER)

    @staticmethod
    def _make_large_integer_label(master, value):
        return tk.Label(master, text=get_pretty_large_integer(value), justify=tk.CENTER)

    # Not needed for now, since I removed the inaccurate training minutes attribute
    # @staticmethod
    # def _make_hours_and_minutes_label(master, minutes):
    #    return tk.Label(master, text=get_pretty_hours_and_minutes(minutes), justify=tk.CENTER)

    def buttonbox(self):
        box = tk.Frame(self)

        tk.Button(box, text="Cancel", width=10, command=self.cancel).pack()

        self.bind("<Return>", self.cancel)
        self.bind("<Escape>", self.cancel)

        box.pack(pady=5)

    def apply(self):
        pass

    def validate(self):
        return True

    @staticmethod
    def _place_in_grid(row, column, widget, sticky="NSEW"):
        widget.grid(row=row, column=column, padx=7, pady=3, sticky=sticky)

    def _callback_open_file(self, file_name):
        self.cancel()
        self.parent.callback_open_this_file(file_name)
