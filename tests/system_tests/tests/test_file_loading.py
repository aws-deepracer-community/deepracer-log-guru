#
# DeepRacer Guru
#
# Version 4.0 onwards
#
# Copyright (c) 2023 dmh23
#

import os
import unittest

from episode.episode import Episode
from src.log.log import Log
from system_tests.tests.dummy_please_wait import DummyPleaseWait
from tracks.reinvent_2018_track import Reinvent2018Track

INPUT_FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "resources", "file_parsing", "input_log_files")

FILE_EXTENSION = ".meta.json"


class TestFileLoadingOfAllEpisodes(unittest.TestCase):
    def test_example_1(self):
        expected_step_counts = [139, 141, 142, 87, 156, 132, 138, 144, 143, 137, 133, 144, 147, 141, 133, 141, 140,
                                142, 131, 138]
        expected_quarters = [1] * 5 + [2] * 5 + [3] * 5 + [4] * 5
        log = self._test_load_episodes("training-20220721141556-OUjJCTWHR7SeYQs_-7xc4A-robomaker.log",
                                       Reinvent2018Track,
                                       expected_step_counts, expected_quarters)

        first_episode: Episode = log.get_episodes()[0]
        # print(first_episode.quarter)

    def _test_load_episodes(self, filename: str, track_type: type, expected_step_counts: list,
                            expected_quarters: list) -> Log:
        # Setup
        self.assertEqual(len(expected_quarters), len(expected_step_counts))  # Ensure valid test case
        meta_filename = filename + FILE_EXTENSION
        self.assertTrue(os.path.isdir(INPUT_FILES_DIR))
        input_file = os.path.join(INPUT_FILES_DIR, filename)
        actual_output_file = os.path.join(INPUT_FILES_DIR, meta_filename)
        self.assertTrue(os.path.isfile(input_file))

        please_wait = DummyPleaseWait(self)
        log = Log(INPUT_FILES_DIR)
        log.parse(filename, please_wait, 10, 20)
        log.save()
        assert (os.path.isfile(actual_output_file))

        all_tracks = {}
        track = track_type()
        track.prepare(all_tracks)

        # Execute
        please_wait = DummyPleaseWait(self)
        log = Log(INPUT_FILES_DIR)
        log.load_all(meta_filename, please_wait, track)

        # Tear down
        os.remove(actual_output_file)

        # Verify
        self.assertEqual(2, please_wait.start_percent)
        self.assertEqual(100, please_wait.current_percent)
        self.assertEqual(log.get_log_meta().episode_count.get(), len(log.get_episodes()))
        self.assertEqual(len(expected_step_counts), len(log.get_episodes()))
        for index, e in enumerate(log.get_episodes()):
            self.assertEqual(expected_step_counts[index], e.step_count)
            self.assertEqual(expected_quarters[index], e.quarter)
            self.assertEqual(index, e.id)

        # Return for additional specific validation
        return log
