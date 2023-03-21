# v4 UI STATUS - CONVERSION IN PROGRESS
# *************************************

#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import time

from PyQt6.QtWidgets import QStatusBar, QLabel, QProgressBar

NEARLY_COMPLETE = 99.99
REDRAW_INTERVAL = 0.15
SMALL_JUMP = 2
BIG_JUMP = 25


class PleaseWait:
    def __init__(self, status_bar: QStatusBar):
        self._percent_done = 0
        self._status_bar = status_bar
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._label_widget = QLabel()

    def start(self, title):
        self._percent_done = 0

        self._label_widget = QLabel(title)
        self._progress_bar.setValue(0)

        self._status_bar.addWidget(self._label_widget)
        self._status_bar.addWidget(self._progress_bar)
        self._progress_bar.show()
        self._label_widget.show()
        self._status_bar.clearMessage()

        self._status_bar.repaint()

    def stop(self, pause_seconds=0):
        time.sleep(pause_seconds)
        self._status_bar.removeWidget(self._label_widget)
        self._status_bar.removeWidget(self._progress_bar)
        self._status_bar.repaint()

    def set_progress(self, percent_done: int | float):
        percent_done = min(100, max(0, round(percent_done)))

        if percent_done > self._percent_done:
            self._percent_done = percent_done
            self._progress_bar.setValue(percent_done)
            self._status_bar.repaint()
