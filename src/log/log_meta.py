#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import os
from typing import Union

from src.action_space.action import Action
from src.action_space.action_space import ActionSpace
from src.main.version import VERSION


class LogMeta:
    #
    # PUBLIC interface (this whole class is basically just a data structure, so it's all public)
    #

    def display_for_debug(self):
        print("Model name = ", self.model_name)

        print("World name = ", self.world_name)
        print("Race type = ", self.race_type)
        print("Job type = ", self.job_type)

        print("Hyper:")
        self.hyper.display_for_debug()

        print("Episode Stats:")
        self.episode_stats.display_for_debug()

    def __init__(self):
        self.hyper = LogMeta.HyperMeta()
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

        new_json["hyper"] = self.hyper.get_as_json()
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

    class HyperMeta:
        def __init__(self):
            self.batch_size = 0
            self.entropy = 0.0
            self.discount_factor = 0.0
            self.loss_type = ""
            self.learning_rate = 0
            self.episodes_per_training_iteration = 0
            self.epochs = 0

        def display_for_debug(self):
            print("    Batch size = ", self.batch_size)
            print("    Entropy = ", self.entropy)
            print("    Discount factor = ", self.discount_factor)
            print("    Loss type = ", self.loss_type)
            print("    Learning rate = ", self.learning_rate)
            print("    Episodes per training iteration = ", self.episodes_per_training_iteration)
            print("    Epochs = ", self.epochs)

        def get_as_json(self):
            new_json = dict()
            new_json["batch_size"] = self.batch_size
            new_json["entropy"] = self.entropy
            new_json["discount_factor"] = self.discount_factor
            new_json["loss_type"] = self.loss_type
            new_json["learning_rate"] = self.learning_rate
            new_json["episodes_per_training_iteration"] = self.episodes_per_training_iteration
            new_json["epochs"] = self.epochs
            return new_json

        def set_from_json(self, received_json):
            self.batch_size = received_json["batch_size"]
            self.entropy = received_json["entropy"]
            self.discount_factor = received_json["discount_factor"]
            self.loss_type = received_json["loss_type"]
            self.learning_rate = received_json["learning_rate"]
            self.episodes_per_training_iteration = received_json["episodes_per_training_iteration"]
            self.epochs = received_json["epochs"]


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


def assert_float_greater_than_zero(value: float):
    assert(isinstance(value, float) and value > 0.0)


def assert_non_empty_string(value: str):
    assert(isinstance(value, str) and str != "")
