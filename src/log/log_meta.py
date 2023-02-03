#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import os
from typing import Final

from src.action_space.action import Action
from src.action_space.action_space import ActionSpace
from src.log.meta_field import MetaField, Optionality
from src.main.version import VERSION


VALID_HYPER_PARAMETER_LOSS_TYPE = ["HUBER", "MEAN_SQUARED_ERROR"]

MANDATORY = Optionality.MANDATORY
OPTIONAL = Optionality.OPTIONAL


class LogMeta:
    def __init__(self):
        self._fields = []
        self.guru_version: Final = self._make_field("guru_version", str, MANDATORY)
        self.model_name: Final = self._make_field("model_name", str, MANDATORY)
        self.world_name: Final = self._make_field("world_name", str, MANDATORY)
        self.race_type: Final = self._make_field("race_type", str, MANDATORY)
        self.job_type: Final = self._make_field("job_type", str, MANDATORY)

        self.batch_size: Final = self._make_field("hyper.batch_size", int, MANDATORY, 1, None)
        self.learning_rate: Final = self._make_field("hyper.learning_rate", float, MANDATORY, 0.00000001, 0.001)
        self.discount_factor: Final = self._make_field("hyper.discount_factor", float, MANDATORY, 0.0, 1.0)
        self.loss_type: Final = self._make_field("hyper.loss_type", str, MANDATORY)
        self.episodes_per_training_iteration: Final = self._make_field("hyper.episodes_per_training_iteration", int, MANDATORY, 1, None)
        self.beta_entropy: Final = self._make_field("hyper.beta_entropy", float, OPTIONAL, 0.0, 1.0)
        self.epochs: Final = self._make_field("hyper.epochs", int, OPTIONAL, 1, None)

        self.episode_count: Final = self._make_field("episode_stats.episode_count", int, MANDATORY)
        self.iteration_count: Final = self._make_field("episode_stats.iteration_count", int, MANDATORY)
        self.success_count: Final = self._make_field("episode_stats.success_count", int, MANDATORY)

        self.average_percent_complete: Final = self._make_field("episode_stats.average_percent_complete", float, MANDATORY)

        self.best_steps: Final = self._make_field("episode_stats.best_steps", int, MANDATORY)
        self.average_steps: Final = self._make_field("episode_stats.average_steps", int, MANDATORY)
        self.worst_steps: Final = self._make_field("episode_stats.worst_steps", int, MANDATORY)

        self.best_time: Final = self._make_field("episode_stats.best_time", float, MANDATORY)
        self.average_time: Final = self._make_field("episode_stats.average_time", float, MANDATORY)
        self.worst_time: Final = self._make_field("episode_stats.worst_time", float, MANDATORY)

        self.best_distance: Final = self._make_field("episode_stats.best_distance", float, MANDATORY)
        self.average_distance: Final = self._make_field("episode_stats.average_distance", float, MANDATORY)
        self.worst_distance: Final = self._make_field("episode_stats.worst_distance", float, MANDATORY)

        self.best_reward: Final = self._make_field("episode_stats.best_reward", float, MANDATORY)
        self.average_reward: Final = self._make_field("episode_stats.average_reward", float, MANDATORY)
        self.worst_reward: Final = self._make_field("episode_stats.worst_reward", float, MANDATORY)

        self.action_space = ActionSpace()

    def get_as_json(self) -> dict:
        self.guru_version.set(VERSION)
        result = MetaField.create_json(self._fields)
        result["action_space"] = self._get_action_space_as_json_list()
        return result

    def set_from_json(self, received_json):
        MetaField.parse_json(self._fields, received_json)
        self.action_space = self._get_action_space_from_json(received_json)

    def _make_field(self, json_path: str, data_type: type, optionality: Optionality, min_value=None, max_value=None):
        new_field = MetaField(json_path, data_type, optionality, min_value, max_value)
        self._fields.append(new_field)
        return new_field

    def _get_action_space_as_json_list(self):
        if self.action_space.is_continuous():
            actions_json = dict()
            low_speed, high_speed, low_steering, high_steering = self.action_space.get_continuous_action_limits()
            actions_json["low_speed"] = low_speed
            actions_json["high_speed"] = high_speed
            actions_json["low_steering"] = low_steering
            actions_json["high_steering"] = high_steering
        else:
            actions_json = []
            a: Action
            for a in self.action_space.get_all_actions():
                action_json = dict()
                action_json["speed"] = a.get_speed()
                action_json["steering_angle"] = a.get_steering_angle()
                action_json["index"] = a.get_index()
                actions_json.append(action_json)

        return actions_json

    @staticmethod
    def _get_action_space_from_json(received_json):
        action_space = ActionSpace()
        received_action_space = received_json["action_space"]
        if type(received_action_space) is list:
            for action_json in received_action_space:
                speed = action_json["speed"]
                steering_angle = action_json["steering_angle"]
                index = action_json["index"]
                action_space.add_action(Action(index, speed, steering_angle))
        else:
            action_space.mark_as_continuous()
            action_space.define_continuous_action_limits(received_action_space["low_speed"],
                                                         received_action_space["high_speed"],
                                                         received_action_space["low_steering"],
                                                         received_action_space["high_steering"])
        return action_space


class OsFileStats:
    _FIELD_UID = "uid"
    _FIELD_SIZE = "size"
    _FIELD_ATIME = "atime"
    _FIELD_MTIME = "mtime"
    _FIELD_CTIME = "ctime"

    def __init__(self, json: dict = None):
        if json:
            assert(isinstance(json, dict))
            self._uid = json[self._FIELD_UID]
            self._size = json[self._FIELD_SIZE]
            self._atime = json[self._FIELD_ATIME]
            self._mtime = json[self._FIELD_MTIME]
            self._ctime = json[self._FIELD_CTIME]
            self._validate()
        else:
            self._uid = 0
            self._size = 0
            self._atime = 0.0
            self._mtime = 0.0
            self._ctime = 0.0

    def set_stats(self, stat_result: os.stat_result) -> None:
        assert (isinstance(stat_result, os.stat_result))
        self._uid = stat_result.st_uid
        self._size = stat_result.st_size
        self._atime = stat_result.st_atime
        self._mtime = stat_result.st_mtime
        self._ctime = stat_result.st_ctime
        self._validate()

    def to_json(self) -> dict:
        return {
            self._FIELD_UID: self._uid,
            self._FIELD_SIZE: self._size,
            self._FIELD_ATIME: self._atime,
            self._FIELD_MTIME: self._mtime,
            self._FIELD_CTIME: self._ctime
        }

    def matches(self, stat_result: os.stat_result) -> bool:
        return (
                stat_result.st_uid == self._uid and
                stat_result.st_size == self._size and
                stat_result.st_atime == self._atime and
                stat_result.st_mtime == self._mtime and
                stat_result.st_ctime == self._ctime
        )

    def _validate(self):
        assert_integer_greater_than_or_equal_to_zero(self._uid)
        assert_integer_greater_than_zero(self._size)
        assert_float_greater_than_zero(self._atime)
        assert_float_greater_than_zero(self._mtime)
        assert_float_greater_than_zero(self._ctime)


class LogFile:
    _FIELD_NAME = "name"
    _FIELD_OS_STATS = "os_stats"

    def __init__(self, json: dict = None):
        if json:
            assert (isinstance(json, dict))
            self.name = json[self._FIELD_NAME]
            self.os_stats = OsFileStats(json[self._FIELD_OS_STATS])
            self._validate()
        else:
            self.name = ""
            self.os_stats = OsFileStats()

    def to_json(self) -> dict:
        self._validate()
        return {
            self._FIELD_NAME: self.name,
            self._FIELD_OS_STATS: self.os_stats.to_json()
        }

    def _validate(self):
        assert_non_empty_string(self.name)
        assert(isinstance(self.os_stats, OsFileStats))


def assert_integer_greater_than_zero(value: int):
    assert(isinstance(value, int) and value > 0)


def assert_integer_greater_than_or_equal_to_zero(value: int):
    assert(isinstance(value, int) and value >= 0)


def assert_integer_inclusive_range(value: int, range1: int, range2: int):
    assert (isinstance(value, int) and min(range1, range2) <= value <= max(range1, range2))


def assert_float_greater_than_zero(value: float):
    assert(isinstance(value, float) and value > 0.0)


def assert_float_greater_than_or_equal_to_zero(value: float):
    assert(isinstance(value, float) and value >= 0.0)


def assert_float_inclusive_range(value: float, range1: float, range2: float):
    assert (isinstance(value, float) and min(range1, range2) <= value <= max(range1, range2))


def assert_non_empty_string(value: str):
    assert(isinstance(value, str) and str != "")


# Same again for optional fields where needed

def assert_optional_integer_greater_than_zero(value: int):
    if value is not None:
        assert_integer_greater_than_zero(value)


def assert_optional_float_inclusive_range(value: float, range1: float, range2: float):
    if value is not None:
        assert_float_inclusive_range(value, range1, range2)