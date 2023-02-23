#
# DeepRacer Guru
#
# Version 4.0 onwards
#
# Copyright (c) 2023 dmh23
#
import filecmp
import json
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

EXPECTED_MULTI_META = os.path.join(os.path.dirname(__file__), "..", "resources", "file_loading")


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
        expected_step_counts = [25, 24, 25, 27, 15, 35, 22, 20, 22, 25,
                                44, 34, 22, 25, 23, 18, 25, 2, 22, 35,
                                60, 34, 38, 41, 20, 33, 16, 17, 26, 25,
                                12, 20, 25, 27, 19, 17, 16, 21, 26, 21,
                                20, 26, 19, 19, 19, 22, 20, 50, 27, 22,
                                27, 26, 24, 36, 21, 35, 18, 15, 27, 23,
                                54, 17, 18, 38, 21, 17, 17, 14, 18, 42,
                                39, 30, 29, 24, 26, 22, 16, 30, 23, 20,
                                37]

        expected_quarters = [1] * 20 + [2] * 20 + [3] * 21 + [4] * 20
        log = self._test_load_episodes(["deepracer-0_robomaker.1.mh77xxe01xgkyky72m378gnwp.log", "deepracer-0_robomaker.2.pleai77ybzcn6yor58nl46ic7.log"],
                                       Reinvent2022Track,
                                       expected_step_counts, expected_quarters)

        self._verify_log_meta_json(log, "test_load_two_worker_log_files.json")

        # TODO - lots more checks on "log" and its contents
        # TODO - including testing a complete log meta setup, have a file to do JSON diff rather than code asserts)

    def _test_load_episodes(self, filenames: Union[str, list], track_type: type, expected_step_counts: list,
                            expected_quarters: list) -> Log:
        # Check valid test case & basic environment
        self.assertEqual(len(expected_quarters), len(expected_step_counts))  # Ensure valid test case
        self.assertTrue(os.path.isdir(INPUT_FILES_DIR))
        if isinstance(filenames, str):
            filenames = [filenames]
        for f in filenames:
            self.assertTrue(os.path.isfile(os.path.join(INPUT_FILES_DIR, f)))

        # Setup meta JSON files, by copying from expected output of the other tests and reinstate the
        # mtime and ctime back to the values of the file in the meta JSON rather than the test placeholder values

        meta_filenames = []
        for f in filenames:
            meta_filename = f + FILE_EXTENSION
            meta_filenames.append(meta_filename)

            log = Log(META_FILES_DIR)
            log.load_meta(meta_filename)
            meta = log.get_log_meta()
            meta.file_mtime.allow_modifications()
            meta.file_ctime.allow_modifications()
            meta_os_stats = os.stat(os.path.join(INPUT_FILES_DIR, f))
            meta.file_mtime.set(meta_os_stats.st_mtime)
            meta.file_ctime.set(meta_os_stats.st_ctime)
            log.save(INPUT_FILES_DIR)

        all_tracks = {}
        track = track_type()
        track.prepare(all_tracks)

        # Execute
        please_wait = DummyPleaseWait(self)
        log = Log(INPUT_FILES_DIR)
        if len(meta_filenames) == 1:
            log.load_all(meta_filenames[0], please_wait, track)
        else:
            log.load_all(meta_filenames, please_wait, track)

        # Tear down
        for f in filenames:
            os.remove(os.path.join(INPUT_FILES_DIR, f + FILE_EXTENSION))

        # Verify
        self.assertEqual(0, round(please_wait.start_percent))
        self.assertEqual(100, please_wait.current_percent)
        self.assertEqual(log.get_log_meta().episode_count.get(), len(log.get_episodes()))
        self.assertEqual(len(expected_step_counts), len(log.get_episodes()))
        for index, e in enumerate(log.get_episodes()):
            self.assertEqual(expected_step_counts[index], e.step_count)
            self.assertEqual(expected_quarters[index], e.quarter)
            self.assertEqual(index, e.id)

        # Return for additional specific validation
        return log

    def _verify_log_meta_json(self, log: Log, expected_json_filename: str):
        actual_json_output_file = os.path.join(INPUT_FILES_DIR, "Multi_meta.json")
        expected_json_output_file = os.path.join(EXPECTED_MULTI_META, expected_json_filename)
        with open(actual_json_output_file, "w+") as meta_file:
            log_json = log._log_meta.get_as_json()
            json.dump(log_json, meta_file, indent=2)

        self.assertTrue(filecmp.cmp(expected_json_output_file, actual_json_output_file, shallow=False), "Incorrect multi JSON")
        os.remove(actual_json_output_file)



# 25, 24, 25, 27, 15, 35, 22, 20, 22, 25
# 60, 34, 38, 41, 20, 33, 16, 17, 26, 25
# 20, 26, 19, 19, 19, 22, 20, 50, 27, 22
# 54, 17, 18, 38, 21, 17, 17, 14, 18, 42
# ----
# 14 UNFINISHED *****



############################################

# 44, 34, 22, 25, 23, 18, 25, 2, 22, 35
# 12, 20, 25, 27, 19, 17, 16, 21, 26, 21
# 27, 26, 24, 36, 21, 35, 18, 15, 27, 23
# 39, 30, 29, 24, 26, 22, 16, 30, 23, 20
# 37