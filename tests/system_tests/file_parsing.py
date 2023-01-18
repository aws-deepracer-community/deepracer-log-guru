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


class TestFileParsingWithJsonOutput(unittest.TestCase):

    def test_load_file_1(self):
        self._test_parse_file("deepracer-0_robomaker.1.vpbdhdkgumibcp5eye7f60xyg.log")

    def test_load_file_2(self):
        self._test_parse_file("dmh-mars-v14-proto-ChampCup-g-training_job_GjvAD1blTUaYAeW79EQEBQ_logs.tar.gz")

    def test_load_file_3(self):
        self._test_parse_file("get-track-dbro-easy-aug-turnpike-training_job_BxX14SAlTzypcxJRR_K45g_logs.tar.gz")

    def test_load_file_4(self):
        self._test_parse_file("training-20220525035255-0NVXkrNsS0qJ1yHgfIXR6Q-robomaker.continuous_May_2022.log")

    def test_load_file_5(self):
        self._test_parse_file("training-20220721141556-OUjJCTWHR7SeYQs_-7xc4A-robomaker.log")

    def test_load_community_training_example_log(self):
        # from: deepracer-utils/tests/deepracer/logs/sample-console-logs/logs/training/
        self._test_parse_file("training-20220611230353-EHNgTNY2T9-77qXhqjBi6A-robomaker.log")

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
