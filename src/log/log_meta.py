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
from src.log.meta_field import MetaField, MetaFields, Optionality
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
        self.job_type: Final = self._make_field("job_type", str, MANDATORY)

        self.file_name = self._make_field("log_file.name", str, MANDATORY)
        self.file_uid = self._make_field("log_file.os_stats.uid", int, MANDATORY)
        self.file_size = self._make_field("log_file.os_stats.size", int, MANDATORY)
        self.file_ctime = self._make_field("log_file.os_stats.ctime", float, MANDATORY)
        self.file_mtime = self._make_field("log_file.os_stats.mtime", float, MANDATORY)

        self.race_type: Final = self._make_field("race.type", str, MANDATORY)
        self.oa_number: Final = self._make_field("race.object_avoidance.number", int, OPTIONAL, 1, None)
        self.oa_randomize: Final = self._make_field("race.object_avoidance.randomize_locations", bool, OPTIONAL)

        self.batch_size: Final = self._make_field("hyperparameters.batch_size", int, OPTIONAL, 1, None)
        self.learning_rate: Final = self._make_field("hyperparameters.learning_rate", float, OPTIONAL, 0.00000001, 0.001)
        self.discount_factor: Final = self._make_field("hyperparameters.discount_factor", float, OPTIONAL, 0.0, 1.0)
        self.loss_type: Final = self._make_field("hyperparameters.loss_type", str, OPTIONAL)
        self.episodes_per_training_iteration: Final = self._make_field("hyperparameters.episodes_per_training_iteration", int, OPTIONAL, 1, None)
        self.beta_entropy: Final = self._make_field("hyperparameters.beta_entropy", float, OPTIONAL, 0.0, 1.0)
        self.epochs: Final = self._make_field("hyperparameters.epochs", int, OPTIONAL, 1, None)
        self.sac_alpha: Final = self._make_field("hyperparameters.sac_alpha", float, OPTIONAL, 0.0, None)
        self.e_greedy_value: Final = self._make_field("hyperparameters.e_greedy_value", float, OPTIONAL, 0.0, None)
        self.epsilon_steps: Final = self._make_field("hyperparameters.epsilon_steps", int, OPTIONAL, 1, None)
        self.exploration_type: Final = self._make_field("hyperparameters.exploration_type", str, OPTIONAL)
        self.stack_size: Final = self._make_field("hyperparameters.stack_size", int, OPTIONAL, 1, None)
        self.termination_average_score: Final = self._make_field("hyperparameters.termination_condition.average_score", float, OPTIONAL, 0.0, None)
        self.termination_max_episodes: Final = self._make_field("hyperparameters.termination_condition.max_episodes", int, OPTIONAL, 1, None)

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

        self.action_space_type: Final = self._make_field("action_space.type", str, MANDATORY)
        self.action_space_min_speed: Final = self._make_field("action_space.min_speed", float, MANDATORY, 0.1, 4.0)
        self.action_space_max_speed: Final = self._make_field("action_space.max_speed", float, MANDATORY, 0.1, 4.0)
        self.action_space_max_left_steering: Final = self._make_field("action_space.max_left_steering", float, MANDATORY, 0.0, 30.0)
        self.action_space_max_right_steering: Final = self._make_field("action_space.max_right_steering", float, MANDATORY, -30.0, 0.0)

        self.action_space = ActionSpace()

    def set_file_os_stats(self, stat_result: os.stat_result) -> None:
        self.file_uid.set(stat_result.st_uid)
        self.file_size.set(stat_result.st_size)
        self.file_mtime.set(stat_result.st_mtime)
        self.file_ctime.set(stat_result.st_ctime)

    def matches_os_stats(self, stat_result: os.stat_result) -> bool:
        return (
                stat_result.st_uid == self.file_uid.get() and
                stat_result.st_size == self.file_size.get() and
                stat_result.st_mtime == self.file_mtime.get() and
                stat_result.st_ctime == self.file_ctime.get()
        )

    def get_as_json(self) -> dict:
        self.guru_version.set(VERSION)
        self._set_meta_fields_based_on_action_space()
        result = MetaFields.create_json(self._fields)
        if not self.action_space.is_continuous():
            result["action_space"]["actions"] = self._get_action_space_as_json_list()   # DISCRETE ONLY
        return result

    def set_from_json(self, received_json):
        MetaFields.parse_json(self._fields, received_json)
        self.action_space = self._get_action_space_from_json(received_json)

    def _make_field(self, json_path: str, data_type: type, optionality: Optionality, min_value=None, max_value=None):
        new_field = MetaField(json_path, data_type, optionality, min_value, max_value)
        self._fields.append(new_field)
        return new_field

    def _set_meta_fields_based_on_action_space(self):
        if self.action_space.is_continuous():
            low_speed, high_speed, low_steering, high_steering = self.action_space.get_continuous_action_limits()
            self.action_space_type.set("CONTINUOUS")
        else:
            low_speed, high_speed, low_steering, high_steering = self.action_space.get_discrete_action_limits()
            self.action_space_type.set("DISCRETE")

        self.action_space_min_speed.set(float(low_speed))
        self.action_space_max_speed.set(float(high_speed))
        self.action_space_max_left_steering.set(float(high_steering))
        self.action_space_max_right_steering.set(float(low_steering))

    def _get_action_space_as_json_list(self):
        assert(not self.action_space.is_continuous())

        actions_json = []
        a: Action
        for a in self.action_space.get_all_actions():
            action_json = dict()
            action_json["speed"] = a.get_speed()
            action_json["steering_angle"] = a.get_steering_angle()
            actions_json.append(action_json)

        return actions_json

    def _get_action_space_from_json(self, received_json):
        action_space = ActionSpace()
        if self.action_space_type.get() == "DISCRETE":
            index = 0
            for action_json in received_json["action_space"]["actions"]:
                speed = action_json["speed"]
                steering_angle = action_json["steering_angle"]
                action_space.add_action(Action(index, speed, steering_angle))
                index += 1
        else:
            action_space.mark_as_continuous()
            action_space.define_continuous_action_limits(self.action_space_min_speed.get(),
                                                         self.action_space_max_speed.get(),
                                                         self.action_space_max_right_steering.get(),
                                                         self.action_space_max_left_steering.get())
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



import sys
print(sys.version)
