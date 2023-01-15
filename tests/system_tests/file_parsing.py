import filecmp
import os
import unittest
import tkinter as tk

from src.ui.please_wait import PleaseWait
from src.log.log import Log

RESOURCE_DIR = os.path.join("resources", "file_parsing")
EXPECTED_RESULT_DIR = os.path.join(RESOURCE_DIR, "expected_output")

FILE_EXTENSION = ".meta.json"


class DummyPleaseWait(PleaseWait):
    def __init__(self):
        super().__init__(tk.Frame(), tk.Canvas())

    def start(self, title):
        pass

    def stop(self, pause_seconds=0):
        pass

    def set_progress(self, percent_done: float):
        pass


class TestStringMethods(unittest.TestCase):

    def test_load_file(self):
        self._test_parse_file("get-track-dbro-easy-aug-turnpike-training_job_BxX14SAlTzypcxJRR_K45g_logs.tar.gz")

    def _test_parse_file(self, filename: str):
        # Setup
        self.assertTrue(os.path.isdir(RESOURCE_DIR))
        self.assertTrue(os.path.isdir(EXPECTED_RESULT_DIR))

        input_file = os.path.join(RESOURCE_DIR, filename)
        actual_output_file = os.path.join(RESOURCE_DIR, filename + FILE_EXTENSION)
        expected_output_file = os.path.join(EXPECTED_RESULT_DIR, filename + FILE_EXTENSION)

        self.assertTrue(os.path.isfile(input_file))
        self.assertTrue(os.path.isfile(expected_output_file))

        if os.path.exists(actual_output_file):
            os.remove(actual_output_file)

        # Execute
        please_wait = DummyPleaseWait()
        log = Log(RESOURCE_DIR)
        log.parse(filename, please_wait, 10, 20)
        log.save()

        # Verify
        self.assertTrue(filecmp.cmp(expected_output_file, actual_output_file, shallow=False), "Incorrect output JSON")

        # Tear down
        os.remove(actual_output_file)


if __name__ == '__main__':
    unittest.main()
