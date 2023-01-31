#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import os

from src.action_space.action import Action
from src.action_space.action_space import ActionSpace
from src.main.version import VERSION


VALID_HYPER_PARAMETER_LOSS_TYPE = ["HUBER", "MEAN_SQUARED_ERROR"]


class LogMeta:
    #
    # PUBLIC interface (this whole class is basically just a data structure, so it's all public)
    #

    def display_for_debug(self):
        print("Model name = ", self.model_name)

        print("World name = ", self.world_name)
        print("Race type = ", self.race_type)
        print("Job type = ", self.job_type)

        print("Episode Stats:")
        self.episode_stats.display_for_debug()

    def __init__(self):
        self.hyper = HyperParameters()
        self.episode_stats = LogMeta.EpisodeStats()

        self.model_name = ""

        self.world_name = ""
        self.race_type = ""
        self.job_type = ""

        self.action_space = ActionSpace()

    def get_as_json(self):
        new_json = dict()
        new_json["guru_version"] = VERSION
        new_json["model_name"] = self.model_name
        new_json["world_name"] = self.world_name
        new_json["race_type"] = self.race_type
        new_json["job_type"] = self.job_type

        new_json["hyper"] = self.hyper.to_json()
        new_json["episode_stats"] = self.episode_stats.get_as_json()

        new_json["action_space"] = self._get_action_space_as_json_list()

        return new_json

    def set_from_json(self, received_json):
        self.model_name = received_json["model_name"]
        self.world_name = received_json["world_name"]
        self.race_type = received_json["race_type"]
        self.job_type = received_json["job_type"]

        self.hyper.set_from_json(received_json["hyper"])
        self.episode_stats.set_from_json(received_json["episode_stats"])

        self.action_space = self._get_action_space_from_json(received_json)

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

    class EpisodeStats:
        def __init__(self):
            self.episode_count = 0
            self.success_count = 0
            self.iteration_count = 0

            self.average_percent_complete = 0.0

            self.best_steps = 0
            self.average_steps = 0
            self.worst_steps = 0

            self.best_time = 0.0
            self.average_time = 0.0
            self.worst_time = 0.0

            self.best_distance = 0.0
            self.average_distance = 0.0
            self.worst_distance = 0.0

            self.best_reward = 0.0
            self.average_reward = 0.0
            self.worst_reward = 0.0

        def display_for_debug(self):
            print("    Episode count = ", self.episode_count)
            print("    Iteration count = ", self.iteration_count)
            print("    Success count = ", self.success_count)
            print("    Success percent = ", round(self.success_count / self.episode_count * 100))

            print("    Average Percent Complete % = ", round(self.average_percent_complete))

            print("    Best steps = ", self.best_steps)
            print("    Average steps = ", self.average_steps)
            print("    Worst steps = ", self.worst_steps)

            print("    Best time = ", self.best_time)
            print("    Average time = ", self.average_time)
            print("    Worst time = ", self.worst_time)

            print("    Best distance = ", round(self.best_distance, 2))
            print("    Average distance = ", round(self.average_distance, 2))
            print("    Worst distance = ", round(self.worst_distance, 2))

        def get_as_json(self):
            new_json = dict()
            new_json["episode_count"] = self.episode_count
            new_json["iteration_count"] = self.iteration_count
            new_json["success_count"] = self.success_count

            new_json["average_percent_complete"] = self.average_percent_complete

            new_json["best_steps"] = self.best_steps
            new_json["average_steps"] = self.average_steps
            new_json["worst_steps"] = self.worst_steps

            new_json["best_time"] = self.best_time
            new_json["average_time"] = self.average_time
            new_json["worst_time"] = self.worst_time

            new_json["best_distance"] = self.best_distance
            new_json["average_distance"] = self.average_distance
            new_json["worst_distance"] = self.worst_distance

            new_json["best_reward"] = self.best_reward
            new_json["average_reward"] = self.average_reward
            new_json["worst_reward"] = self.worst_reward

            return new_json

        def set_from_json(self, received_json):
            self.episode_count = received_json["episode_count"]
            self.iteration_count = received_json["iteration_count"]
            self.success_count = received_json["success_count"]

            self.average_percent_complete = received_json["average_percent_complete"]

            self.best_steps = received_json["best_steps"]
            self.average_steps = received_json["average_steps"]
            self.worst_steps = received_json["worst_steps"]

            self.best_time = received_json["best_time"]
            self.average_time = received_json["average_time"]
            self.worst_time = received_json["worst_time"]

            self.best_distance = received_json["best_distance"]
            self.average_distance = received_json["average_distance"]
            self.worst_distance = received_json["worst_distance"]

            self.best_reward = received_json["best_reward"]
            self.average_reward = received_json["average_reward"]
            self.worst_reward = received_json["worst_reward"]


class HyperParameters:
    _FIELD_BATCH_SIZE = "batch_size"
    _FIELD_LEARNING_RATE = "learning_rate"
    _FIELD_DISCOUNT_FACTOR = "discount_factor"
    _FIELD_LOSS_TYPE = "loss_type"
    _FIELD_EPISODES_PER_TRAINING_ITERATION = "episodes_per_training_iteration"
    _FIELD_BETA_ENTROPY = "beta_entropy"
    _FIELD_EPOCHS = "epochs"
    # _FIELD_SAC_ALPHA = "sac_alpha"
    # _FIELD_E_GREEDY_VALUE = "e_greedy_value"
    # _FIELD_EPSILON_STEPS = "epsilon_steps"
    # _FIELD_EXPLORATION_TYPE = "exploration_type"
    # _FIELD_STACK_SIZE = "stack_size"
    # _FIELD_TERMINATION_CONDITION = "termination_condition"

    def __init__(self, json: dict = None):
        if json:
            assert (isinstance(json, dict))
            self.batch_size = json[self._FIELD_BATCH_SIZE]
            self.learning_rate = json[self._FIELD_LEARNING_RATE]
            self.discount_factor = json[self._FIELD_DISCOUNT_FACTOR]
            self.loss_type = json[self._FIELD_LOSS_TYPE]
            self.episodes_per_training_iteration = json[self._FIELD_EPISODES_PER_TRAINING_ITERATION]
            self.beta_entropy = json[self._FIELD_BETA_ENTROPY]
            self.epochs = json[self._FIELD_EPOCHS]
            self._validate()
        else:
            self.batch_size = None
            self.learning_rate = None
            self.discount_factor = None
            self.loss_type = None
            self.episodes_per_training_iteration = None
            self.beta_entropy = None
            self.epochs = None

    def to_json(self) -> dict:
        self._validate()
        new_json = {
            self._FIELD_BATCH_SIZE: self.batch_size,
            self._FIELD_LEARNING_RATE: self.learning_rate,
            self._FIELD_DISCOUNT_FACTOR: self.discount_factor,
            self._FIELD_LOSS_TYPE: self.loss_type,
            self._FIELD_EPISODES_PER_TRAINING_ITERATION: self.episodes_per_training_iteration
        }
        if self.beta_entropy is not None:
            new_json[self._FIELD_BETA_ENTROPY] = self.beta_entropy
        if self.epochs is not None:
            new_json[self._FIELD_EPOCHS] = self.epochs
        return new_json

    def _validate(self):
        assert_integer_greater_than_zero(self.batch_size)
        assert_float_inclusive_range(self.learning_rate, 0.001, 0.00000001)
        assert_float_inclusive_range(self.discount_factor, 0.0, 1.0)
        assert(self.loss_type in VALID_HYPER_PARAMETER_LOSS_TYPE)
        assert_integer_greater_than_zero(self.episodes_per_training_iteration)
        assert_optional_float_inclusive_range(self.beta_entropy, 0.0, 1.0)
        assert_optional_integer_greater_than_zero(self.epochs)


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