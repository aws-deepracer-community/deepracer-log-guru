#
# DeepRacer Guru
#
# Version 4.0 onwards
#
# Copyright (c) 2023 dmh23
#

import os
import unittest
import tkinter as tk

from src.ui.please_wait import PleaseWait
from src.log.log import Log
from tracks.reinvent_2018_track import Reinvent2018Track

INPUT_FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "resources", "file_parsing", "input_log_files")

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


class TestFileLoadingOfAllEpisodes(unittest.TestCase):

    def test_example_1(self):
        self._test_load_episodes("training-20220721141556-OUjJCTWHR7SeYQs_-7xc4A-robomaker.log", Reinvent2018Track)

    def _test_load_episodes(self, filename: str, track_type: type):
        # Setup
        meta_filename = filename + FILE_EXTENSION
        self.assertTrue(os.path.isdir(INPUT_FILES_DIR))
        input_file = os.path.join(INPUT_FILES_DIR, filename)
        actual_output_file = os.path.join(INPUT_FILES_DIR, meta_filename)
        self.assertTrue(os.path.isfile(input_file))

        please_wait = DummyPleaseWait()
        log = Log(INPUT_FILES_DIR)
        log.parse(filename, please_wait, 10, 20)
        log.save()
        assert(os.path.isfile(actual_output_file))

        all_tracks = {}
        track = track_type()
        track.prepare(all_tracks)

        # Execute
        log = Log(INPUT_FILES_DIR)
        log.load_all(meta_filename, please_wait, track)

        # Verify
        self.assertEqual(log.get_log_meta().episode_count.get(), len(log.get_episodes()))

        # Tear down
        os.remove(actual_output_file)
