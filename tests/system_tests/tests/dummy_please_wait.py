import unittest
import tkinter as tk

from ui.please_wait import PleaseWait


class DummyPleaseWait(PleaseWait):
    def __init__(self, test_case: unittest.TestCase):
        super().__init__(tk.Frame(), tk.Canvas())
        self.start_percent = 100
        self.current_percent = 0
        self._test_case = test_case

    def start(self, title):
        pass

    def stop(self, pause_seconds=0):
        pass

    def set_progress(self, percent_done: float):
        self._test_case.assertTrue(self.current_percent <= percent_done <= 100)
        self.current_percent = percent_done
        if percent_done < self.start_percent:
            self.start_percent = percent_done
