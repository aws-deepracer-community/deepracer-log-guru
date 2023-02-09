#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import os
from typing import Final

from object_avoidance.fixed_object_locations import FixedObjectLocations
from src.action_space.action import Action
from src.action_space.action_space import ActionSpace
from src.log.meta_field import MetaField, MetaFields, Optionality
from src.main.version import VERSION

# VALID_HYPER_PARAMETER_LOSS_TYPE = ["HUBER", "MEAN_SQUARED_ERROR"]

MANDATORY = Optionality.MANDATORY
OPTIONAL = Optionality.OPTIONAL


class LogMeta:
    def __init__(self):
        self._fields = []
        self.guru_version: Final = self._make_field("guru_version", str, MANDATORY)
        self.model_name: Final = self._make_field("model_name", str, MANDATORY)
        self.model_name.allow_modifications()

        self.job_type: Final = self._make_field("job.type", str, MANDATORY)
        self.job_type.set_allowed_values(["TRAINING"])
        self.platform: Final = self._make_field("job.platform", str, MANDATORY)
        self.platform.set_allowed_values(["AWS_CONSOLE", "DEEPRACER_FOR_CLOUD"])
        self.workers: Final = self._make_field("job.workers", int, MANDATORY, 1, None)
        self.worker_id: Final = self._make_field("job.worker_id", int, MANDATORY, 0, None)
        self.start_date: Final = self._make_field("job.start_date", str, MANDATORY)

        self.learning_algorithm: Final = self._make_field("training.learning_algorithm", str, OPTIONAL)
        self.learning_algorithm.set_allowed_values(["CLIPPED_PPO", "SAC"])
        self.alternate_direction: Final = self._make_field("training.alternate_driving_direction", bool, OPTIONAL)
        self.start_position_offset: Final = self._make_field("training.start_position_offset", float, OPTIONAL, 0.0,
                                                             0.999)
        self.change_start_position: Final = self._make_field("training.change_start_position", bool, OPTIONAL)
        self.round_robin_advance_distance: Final = self._make_field("training.round_robin_advance_distance", float,
                                                                    OPTIONAL, 0.0, 0.999)
        self.min_evaluations_per_iteration: Final = self._make_field("training.minimum_evaluations_per_iteration", int,
                                                                     OPTIONAL, 0)

        self.domain_randomization: Final = self._make_field("environment.domain_randomization", bool, OPTIONAL)
        self.simulation_version: Final = self._make_field("environment.simulation_version", str, MANDATORY)
        self.simulation_version.set_allowed_values(["3.0", "4.0", "5.0"])
        self.track_name: Final = self._make_field("environment.track_name", str, MANDATORY)

        self.file_name: Final = self._make_field("log_file.name", str, MANDATORY)
        self.file_uid: Final = self._make_field("log_file.os_stats.uid", int, MANDATORY)
        self.file_size: Final = self._make_field("log_file.os_stats.size", int, MANDATORY)
        self.file_ctime: Final = self._make_field("log_file.os_stats.ctime", float, MANDATORY)
        self.file_mtime: Final = self._make_field("log_file.os_stats.mtime", float, MANDATORY)

        self.race_type: Final = self._make_field("race.type", str, MANDATORY)
        self.race_type.set_allowed_values(["TIME_TRIAL", "OBJECT_AVOIDANCE", "HEAD_TO_HEAD"])

        self.oa_number: Final = self._make_field("race.object_avoidance.number", int, OPTIONAL, 1, None)
        self.oa_min_distance_between: Final = self._make_field("race.object_avoidance.min_distance_between", float, OPTIONAL, 0.0, None)
        self.oa_randomize: Final = self._make_field("race.object_avoidance.randomize_locations", bool, OPTIONAL)
        self.oa_type: Final = self._make_field("race.object_avoidance.type", str, OPTIONAL)
        self.oa_type.set_allowed_values(["BROWN_BOX", "PURPLE_BOX", "BOT_CAR"])

        self.h2h_number: Final = self._make_field("race.head_to_head.number", int, OPTIONAL, 1, None)
        self.h2h_speed: Final = self._make_field("race.head_to_head.speed", float, OPTIONAL, 0.0, 4.0)

        self.sensors: Final = self._make_field("car.sensors", list, MANDATORY)
        self.sensors.set_allowed_values(["SINGLE_CAMERA", "STEREO_CAMERAS", "LIDAR", "SECTOR_LIDAR"])
        self.lidar_number_of_sectors: Final = self._make_field("car.lidar.number_of_sectors", int, OPTIONAL)
        self.lidar_number_of_values_per_sector: Final = self._make_field("car.lidar.number_of_values_per_sector", int, OPTIONAL)
        self.lidar_clipping_distance: Final = self._make_field("car.lidar.clipping_distance", float, OPTIONAL)
        self.neural_network_topology: Final = self._make_field("neural_network.topology", str, MANDATORY)
        self.neural_network_topology.set_allowed_values(["DEEP_CONVOLUTIONAL_3_LAYER"])

        self.batch_size: Final = self._make_field("hyperparameters.batch_size", int, OPTIONAL, 1, None)
        self.learning_rate: Final = self._make_field("hyperparameters.learning_rate", float, OPTIONAL, 0.00000001,
                                                     0.001)
        self.discount_factor: Final = self._make_field("hyperparameters.discount_factor", float, OPTIONAL, 0.0, 1.0)
        self.loss_type: Final = self._make_field("hyperparameters.loss_type", str, OPTIONAL)
        self.loss_type.set_allowed_values(["HUBER", "MEAN_SQUARED_ERROR"])
        self.episodes_per_training_iteration: Final = self._make_field(
            "hyperparameters.episodes_per_training_iteration", int, OPTIONAL, 1, None)
        self.beta_entropy: Final = self._make_field("hyperparameters.beta_entropy", float, OPTIONAL, 0.0, 1.0)
        self.epochs: Final = self._make_field("hyperparameters.epochs", int, OPTIONAL, 1, None)
        self.sac_alpha: Final = self._make_field("hyperparameters.sac_alpha", float, OPTIONAL, 0.0, None)
        self.e_greedy_value: Final = self._make_field("hyperparameters.e_greedy_value", float, OPTIONAL, 0.0, None)
        self.epsilon_steps: Final = self._make_field("hyperparameters.epsilon_steps", int, OPTIONAL, 1, None)
        self.exploration_type: Final = self._make_field("hyperparameters.exploration_type", str, OPTIONAL)
        self.exploration_type.set_allowed_values(["CATEGORICAL", "ADDITIVE_NOISE"])
        self.stack_size: Final = self._make_field("hyperparameters.stack_size", int, OPTIONAL, 1, None)
        self.termination_average_score: Final = self._make_field("hyperparameters.termination_condition.average_score",
                                                                 float, OPTIONAL, 0.0, None)
        self.termination_max_episodes: Final = self._make_field("hyperparameters.termination_condition.max_episodes",
                                                                int, OPTIONAL, 1, None)

        self.episode_count: Final = self._make_field("episode_stats.episode_count", int, MANDATORY)
        self.iteration_count: Final = self._make_field("episode_stats.iteration_count", int, MANDATORY)
        self.success_count: Final = self._make_field("episode_stats.success_count", int, MANDATORY).allow_modifications()

        self.average_percent_complete: Final = self._make_field("episode_stats.average_percent_complete", float,
                                                                MANDATORY)

        self.best_steps: Final = self._make_field("episode_stats.best_steps", int, MANDATORY).allow_modifications()
        self.average_steps: Final = self._make_field("episode_stats.average_steps", int, MANDATORY).allow_modifications()
        self.worst_steps: Final = self._make_field("episode_stats.worst_steps", int, MANDATORY).allow_modifications()

        self.best_time: Final = self._make_field("episode_stats.best_time", float, MANDATORY).allow_modifications()
        self.average_time: Final = self._make_field("episode_stats.average_time", float, MANDATORY).allow_modifications()
        self.worst_time: Final = self._make_field("episode_stats.worst_time", float, MANDATORY).allow_modifications()

        self.best_distance: Final = self._make_field("episode_stats.best_distance", float, MANDATORY).allow_modifications()
        self.average_distance: Final = self._make_field("episode_stats.average_distance", float, MANDATORY).allow_modifications()
        self.worst_distance: Final = self._make_field("episode_stats.worst_distance", float, MANDATORY).allow_modifications()

        self.best_reward: Final = self._make_field("episode_stats.best_reward", float, MANDATORY).allow_modifications()
        self.average_reward: Final = self._make_field("episode_stats.average_reward", float, MANDATORY).allow_modifications()
        self.worst_reward: Final = self._make_field("episode_stats.worst_reward", float, MANDATORY).allow_modifications()

        self.action_space_type: Final = self._make_field("action_space.type", str, MANDATORY)
        self.action_space_type.set_allowed_values(["DISCRETE", "CONTINUOUS"])
        self.action_space_min_speed: Final = self._make_field("action_space.min_speed", float, MANDATORY, 0.1, 4.0)
        self.action_space_max_speed: Final = self._make_field("action_space.max_speed", float, MANDATORY, 0.1, 4.0)
        self.action_space_max_left_steering: Final = self._make_field("action_space.max_left_steering", float,
                                                                      MANDATORY, 0.0, 30.0)
        self.action_space_max_right_steering: Final = self._make_field("action_space.max_right_steering", float,
                                                                       MANDATORY, -30.0, 0.0)

        self.action_space = ActionSpace()
        self.fixed_object_locations = FixedObjectLocations()

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
            result["action_space"]["actions"] = self._get_action_space_as_json_list()
        if self.fixed_object_locations.has_locations():
            result["race"]["object_avoidance"]["fixed_locations"] = self.fixed_object_locations.get_meta_json_list()

        return result

    def set_from_json(self, received_json: dict):
        MetaFields.parse_json(self._fields, received_json)
        self.action_space = self._get_action_space_from_json(received_json)
        if "object_avoidance" in received_json["race"]:
            if "fixed_locations" in received_json["race"]["object_avoidance"]:
                self.fixed_object_locations.set_from_meta_json_list(received_json["race"]["object_avoidance"]["fixed_locations"])

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
        assert (not self.action_space.is_continuous())

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
