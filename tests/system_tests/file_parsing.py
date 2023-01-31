import filecmp
import os
import unittest
import tkinter as tk

from src.ui.please_wait import PleaseWait
from src.log.log import Log

RESOURCE_DIR = os.path.join("resources", "file_parsing")
INPUT_FILES_DIR = os.path.join(RESOURCE_DIR, "input_log_files")
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

    # Naming convention for tests to show combinations of file types
    #       training                    [ others to come, e.g. evaluation and leaderboard ]
    #       console  /  drfc
    #       log  /  zip
    #       tt  /  oa  /  h2h / h2hoa
    #       discrete  /  continuous
    #       ppo / sac
    #       [ month and year ]

    def test_parse_training_drfc_log_oa_discrete_ppo_aug_2022(self):
        self._test_parse_file("deepracer-0_robomaker.1.vpbdhdkgumibcp5eye7f60xyg.log")

    def test_parse_training_console_zip_tt_discrete_ppo_aug_2020(self):
        self._test_parse_file("dmh-mars-v14-proto-ChampCup-g-training_job_GjvAD1blTUaYAeW79EQEBQ_logs.tar.gz")

    def test_parse_training_console_zip_tt_discrete_ppo_aug_2022(self):
        self._test_parse_file("get-track-dbro-easy-aug-turnpike-training_job_BxX14SAlTzypcxJRR_K45g_logs.tar.gz")

    def test_parse_training_console_log_tt_continuous_ppo_may_2022(self):
        self._test_parse_file("training-20220525035255-0NVXkrNsS0qJ1yHgfIXR6Q-robomaker.continuous_May_2022.log")

    def test_parse_training_console_log_tt_discrete_ppo_july_2022(self):
        self._test_parse_file("training-20220721141556-OUjJCTWHR7SeYQs_-7xc4A-robomaker.log")

    def test_parse_training_console_log_tt_discrete_ppo_june_2022(self):
        # from: deepracer-utils/tests/deepracer/logs/sample-console-logs/logs/training/
        self._test_parse_file("training-20220611230353-EHNgTNY2T9-77qXhqjBi6A-robomaker.log")

    def test_parse_training_console_log_tt_discrete_ppo_oct_2021(self):
        self._test_parse_file("training-20211020114346-TfRNRwzjRW2UIpugm7Gd-Q-robomaker.log")

    def test_parse_training_drfc_log_tt_discrete_ppo_oct_2021(self):
        self._test_parse_file("deepracer-0_robomaker.1.ynytdrw16nuhl8y1pauseuelw.log")

    def test_parse_training_console_zip_tt_continuous_ppo_sep_2022(self):
        self._test_parse_file("try-continuous-action-space-training_job_dY6qyhqlQi2LlSh97kPYiw_logs.tar.gz")

    def test_parse_training_console_zip_h2hoa_continuous_sac_jan_2023(self):
        self._test_parse_file("head-to-head-short-session-training_job_O-uWGmcTSAyrIj9X2PFXxQ_logs.tar.gz")

    def test_parse_training_console_zip_tt_continuous_sac_jan_2023(self):
        self._test_parse_file("sac-short-session-training_job_30Ieq368TqS-fa6QaRM3qA_logs.tar.gz")

    def _test_parse_file(self, filename: str):
        # Setup
        self.assertTrue(os.path.isdir(RESOURCE_DIR))
        self.assertTrue(os.path.isdir(INPUT_FILES_DIR))
        self.assertTrue(os.path.isdir(EXPECTED_RESULT_DIR))

        input_file = os.path.join(INPUT_FILES_DIR, filename)
        actual_output_file = os.path.join(INPUT_FILES_DIR, filename + FILE_EXTENSION)
        expected_output_file = os.path.join(EXPECTED_RESULT_DIR, filename + FILE_EXTENSION)

        self.assertTrue(os.path.isfile(input_file))
        self.assertTrue(os.path.isfile(expected_output_file))

        if os.path.exists(actual_output_file):
            os.remove(actual_output_file)

        # Execute
        please_wait = DummyPleaseWait()
        log = Log(INPUT_FILES_DIR)
        log.parse(filename, please_wait, 10, 20)
        log.save()

        # Verify
        self.assertTrue(filecmp.cmp(expected_output_file, actual_output_file, shallow=False), "Incorrect output JSON")

        # Tear down
        os.remove(actual_output_file)


if __name__ == '__main__':
    unittest.main()
