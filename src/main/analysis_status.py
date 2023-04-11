from src.episode.episode_filter import EpisodeFilter
from src.log.log import Log
from src.tracks.track import Track


class AnalysisStatus:
    def __init__(self):
        self._track: Track | None = None
        self._log: Log | None = None
        self._model_name = ""
        self._episode_filter = EpisodeFilter()

    def open_log(self, log: Log, model_name: str):
        self._log = log
        self._model_name = model_name

    def set_track(self, track: Track):
        self._track = track

    def get_log(self):
        return self._log

    def get_model_name(self):
        return self._model_name

    def get_track(self):
        return self._track

    def get_episode_filter(self):
        return self._episode_filter



