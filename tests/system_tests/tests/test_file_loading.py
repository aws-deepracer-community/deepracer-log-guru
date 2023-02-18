#
# DeepRacer Guru
#
# Version 4.0 onwards
#
# Copyright (c) 2023 dmh23
#

import os
import shutil
from typing import Union
import unittest

from episode.episode import Episode
from src.log.log import Log
from system_tests.tests.dummy_please_wait import DummyPleaseWait
from tracks.reinvent_2018_track import Reinvent2018Track
from tracks.reinvent_2022_track import Reinvent2022Track

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "resources", "file_parsing")
INPUT_FILES_DIR = os.path.join(RESOURCE_DIR, "input_log_files")
META_FILES_DIR = os.path.join(RESOURCE_DIR, "expected_output")


FILE_EXTENSION = ".meta.json"


class TestFileLoadingOfAllEpisodes(unittest.TestCase):
    def test_load_single_short_log_file(self):
        expected_step_counts = [139, 141, 142, 87, 156, 132, 138, 144, 143, 137, 133, 144, 147, 141, 133, 141, 140,
                                142, 131, 138]
        expected_quarters = [1] * 5 + [2] * 5 + [3] * 5 + [4] * 5
        log = self._test_load_episodes("training-20220721141556-OUjJCTWHR7SeYQs_-7xc4A-robomaker.log",
                                       Reinvent2018Track,
                                       expected_step_counts, expected_quarters)

        first_episode: Episode = log.get_episodes()[0]
        # print(first_episode.quarter)

    def test_load_two_worker_log_files(self):
        expected_step_counts = [999, 888]
        expected_quarters = [1] * 2
        log = self._test_load_episodes(["deepracer-0_robomaker.1.mh77xxe01xgkyky72m378gnwp.log", "deepracer-0_robomaker.2.pleai77ybzcn6yor58nl46ic7.log"],
                                       Reinvent2022Track,
                                       expected_step_counts, expected_quarters)

    def _test_load_episodes(self, filenames: Union[str, list], track_type: type, expected_step_counts: list,
                            expected_quarters: list) -> Log:
        # Check valid test case & basic environment
        self.assertEqual(len(expected_quarters), len(expected_step_counts))  # Ensure valid test case
        self.assertTrue(os.path.isdir(INPUT_FILES_DIR))
        if isinstance(filenames, str):
            filenames = [filenames]
        for f in filenames:
            self.assertTrue(os.path.isfile(os.path.join(INPUT_FILES_DIR, f)))

        # Setup meta JSON files
        meta_filenames = []
        for f in filenames:
            meta_filename = f + FILE_EXTENSION
            shutil.copyfile(os.path.join(META_FILES_DIR, meta_filename), os.path.join(INPUT_FILES_DIR, meta_filename))
            meta_filenames.append(meta_filename)

        all_tracks = {}
        track = track_type()
        track.prepare(all_tracks)

        # Execute
        please_wait = DummyPleaseWait(self)
        log = Log(INPUT_FILES_DIR)
        log.get_log_meta().file_mtime.allow_modifications()
        log.get_log_meta().file_ctime.allow_modifications()
        if len(meta_filenames) == 1:
            log.load_all(meta_filenames[0], please_wait, track)
        else:
            log.load_all(meta_filenames, please_wait, track)

        # Tear down
        for f in filenames:
            os.remove(os.path.join(INPUT_FILES_DIR, f + FILE_EXTENSION))

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
