#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import os
from enum import Enum, auto
from typing import Final, Self

from object_avoidance.fixed_object_locations import FixedObjectLocations
from src.action_space.action import Action
from src.action_space.action_space import ActionSpace
from src.log.meta_field import MetaField, MetaFields, Optionality
from src.main.version import VERSION

MANDATORY = Optionality.MANDATORY
OPTIONAL = Optionality.OPTIONAL


class LossType(Enum):
    HUBER = auto()
    MEAN_SQUARED_ERROR = auto()


class JobType(Enum):
    TRAINING = auto()


class Platform(Enum):
    AWS_CONSOLE = auto()
    DEEPRACER_FOR_CLOUD = auto()


class LearningAlgorithm(Enum):
    CLIPPED_PPO = auto()
    SAC = auto()


class RaceType(Enum):
    TIME_TRIAL = auto()
    OBJECT_AVOIDANCE = auto()
    HEAD_TO_HEAD = auto()


class ObstacleType(Enum):
    BROWN_BOX = auto()
    PURPLE_BOX = auto()
    BOT_CAR = auto()


class CarTrimColour(Enum):
    BLACK = auto()
    GREY = auto()
    BLUE = auto()
    RED = auto()
    ORANGE = auto()
    WHITE = auto()
    PURPLE = auto()


class NeuralNetworkTopology(Enum):
    DEEP_CONVOLUTIONAL_3_LAYER = auto()


class ExplorationType(Enum):
    CATEGORICAL = auto()
    ADDITIVE_NOISE = auto()


class ActionSpaceType(Enum):
    DISCRETE = auto()
    CONTINUOUS = auto()


class LogMeta:
    def __init__(self):
        self._fields = []
        self.guru_version: Final = self._make_field("guru_version", str, MANDATORY)
        self.model_name: Final = self._make_field("model_name", str, MANDATORY)
        self.model_name.allow_modifications()

        self.job_type: Final = self._make_field("job.type", JobType, MANDATORY)
        self.platform: Final = self._make_field("job.platform", Platform, MANDATORY)
        self.workers: Final = self._make_field("job.workers", int, MANDATORY, 1, None)
        self.worker_id: Final = self._make_field("job.worker_id", int, MANDATORY, 0, None)
        self.start_date: Final = self._make_field("job.start_date", str, MANDATORY)

        self.learning_algorithm: Final = self._make_field("training.learning_algorithm", LearningAlgorithm, OPTIONAL)
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

        self.race_type: Final = self._make_field("race.type", RaceType, MANDATORY)

        self.oa_number: Final = self._make_field("race.object_avoidance.number", int, OPTIONAL, 1, None)
        self.oa_min_distance_between: Final = self._make_field("race.object_avoidance.min_distance_between", float,
                                                               OPTIONAL, 0.0, None)
        self.oa_randomize: Final = self._make_field("race.object_avoidance.randomize_locations", bool, OPTIONAL)
        self.oa_type: Final = self._make_field("race.object_avoidance.type", ObstacleType, OPTIONAL)

        self.h2h_number_of_bots: Final = self._make_field("race.head_to_head.number", int, OPTIONAL, 1, None)
        self.h2h_speed: Final = self._make_field("race.head_to_head.speed", float, OPTIONAL, 0.1, 4.0)
        self.h2h_min_distance_between: Final = self._make_field("race.head_to_head.min_distance_between", float,
                                                                OPTIONAL, 0.0, None)
        self.h2h_randomize_bot_locations: Final = self._make_field("race.head_to_head.randomize_bot_locations", bool,
                                                                   OPTIONAL)
        self.h2h_allow_lane_changes: Final = self._make_field("race.head_to_head.allow_lane_changes", bool, OPTIONAL)
        self.h2h_lower_lane_change_time: Final = self._make_field("race.head_to_head.lane_changes.lower_change_time",
                                                                  float,
                                                                  OPTIONAL, 1.0, 5.0)
        self.h2h_upper_lane_change_time: Final = self._make_field("race.head_to_head.lane_changes.upper_change_time",
                                                                  float,
                                                                  OPTIONAL, 1.0, 5.0)
        self.h2h_lane_change_distance: Final = self._make_field("race.head_to_head.lane_changes.distance", float,
                                                                OPTIONAL, 0.0, None)

        self.car_trim_colour: Final = self._make_field("car.trim_colour", CarTrimColour, MANDATORY)
        self.car_name: Final = self._make_field("car.name", str, OPTIONAL)
        self.car_shell_type: Final = self._make_field("car.shell_type", str, MANDATORY)

        self.sensors: Final = self._make_field("car.sensors", list, MANDATORY)
        self.sensors.set_allowed_values(["SINGLE_CAMERA", "STEREO_CAMERAS", "LIDAR", "SECTOR_LIDAR"])

        self.lidar_number_of_sectors: Final = self._make_field("car.lidar.number_of_sectors", int, OPTIONAL)
        self.lidar_number_of_values_per_sector: Final = self._make_field("car.lidar.number_of_values_per_sector", int,
                                                                         OPTIONAL)
        self.lidar_clipping_distance: Final = self._make_field("car.lidar.clipping_distance", float, OPTIONAL)
        self.neural_network_topology: Final = self._make_field("neural_network.topology", NeuralNetworkTopology,
                                                               MANDATORY)

        self.batch_size: Final = self._make_field("hyperparameters.batch_size", int, OPTIONAL, 1, None)
        self.learning_rate: Final = self._make_field("hyperparameters.learning_rate", float, OPTIONAL, 0.00000001,
                                                     0.001)
        self.discount_factor: Final = self._make_field("hyperparameters.discount_factor", float, OPTIONAL, 0.0, 1.0)
        self.loss_type: Final = self._make_field("hyperparameters.loss_type", LossType, OPTIONAL)
        self.episodes_per_training_iteration: Final = self._make_field(
            "hyperparameters.episodes_per_training_iteration", int, OPTIONAL, 1, None)
        self.beta_entropy: Final = self._make_field("hyperparameters.beta_entropy", float, OPTIONAL, 0.0, 1.0)
        self.epochs: Final = self._make_field("hyperparameters.epochs", int, OPTIONAL, 1, None)
        self.sac_alpha: Final = self._make_field("hyperparameters.sac_alpha", float, OPTIONAL, 0.0, None)
        self.e_greedy_value: Final = self._make_field("hyperparameters.e_greedy_value", float, OPTIONAL, 0.0, None)
        self.epsilon_steps: Final = self._make_field("hyperparameters.epsilon_steps", int, OPTIONAL, 1, None)
        self.exploration_type: Final = self._make_field("hyperparameters.exploration_type", ExplorationType, OPTIONAL)
        self.stack_size: Final = self._make_field("hyperparameters.stack_size", int, OPTIONAL, 1, None)
        self.termination_average_score: Final = self._make_field("hyperparameters.termination_condition.average_score",
                                                                 float, OPTIONAL, 0.0, None)
        self.termination_max_episodes: Final = self._make_field("hyperparameters.termination_condition.max_episodes",
                                                                int, OPTIONAL, 1, None)

        self.episode_count: Final = self._make_field("episode_stats.episode_count", int, MANDATORY)
        self.iteration_count: Final = self._make_field("episode_stats.iteration_count", int, MANDATORY)
        self.success_count: Final = self._make_field("episode_stats.success_count", int,
                                                     MANDATORY).allow_modifications()

        self.average_percent_complete: Final = self._make_field("episode_stats.average_percent_complete", float,
                                                                MANDATORY)

        self.best_steps: Final = self._make_field("episode_stats.best_steps", int, MANDATORY).allow_modifications()
        self.average_steps: Final = self._make_field("episode_stats.average_steps", int,
                                                     MANDATORY).allow_modifications()
        self.worst_steps: Final = self._make_field("episode_stats.worst_steps", int, MANDATORY).allow_modifications()

        self.best_time: Final = self._make_field("episode_stats.best_time", float, MANDATORY).allow_modifications()
        self.average_time: Final = self._make_field("episode_stats.average_time", float,
                                                    MANDATORY).allow_modifications()
        self.worst_time: Final = self._make_field("episode_stats.worst_time", float, MANDATORY).allow_modifications()

        self.best_distance: Final = self._make_field("episode_stats.best_distance", float,
                                                     MANDATORY).allow_modifications()
        self.average_distance: Final = self._make_field("episode_stats.average_distance", float,
                                                        MANDATORY).allow_modifications()
        self.worst_distance: Final = self._make_field("episode_stats.worst_distance", float,
                                                      MANDATORY).allow_modifications()

        self.best_reward: Final = self._make_field("episode_stats.best_reward", float, MANDATORY).allow_modifications()
        self.average_reward: Final = self._make_field("episode_stats.average_reward", float,
                                                      MANDATORY).allow_modifications()
        self.worst_reward: Final = self._make_field("episode_stats.worst_reward", float,
                                                    MANDATORY).allow_modifications()

        self.action_space_type: Final = self._make_field("action_space.type", ActionSpaceType, MANDATORY)
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

    def set_from_json(self, received_json: dict) -> None:
        MetaFields.parse_json(self._fields, received_json)
        self.action_space = self._get_action_space_from_json(received_json)
        if "object_avoidance" in received_json["race"]:
            if "fixed_locations" in received_json["race"]["object_avoidance"]:
                self.fixed_object_locations.set_from_meta_json_list(
                    received_json["race"]["object_avoidance"]["fixed_locations"])

    def merge_from_multi_logs(self, multi_log_meta: list[Self]):
        assert len(multi_log_meta) >= 2

        # Some fields are different per log, so need to be arbitrarily set to the value in the FIRST merged log
        self.worker_id.set(multi_log_meta[0].worker_id.get())
        self.alternate_direction.set(multi_log_meta[0].alternate_direction.get())
        self.start_position_offset.set(multi_log_meta[0].start_position_offset.get())
        self.change_start_position.set(multi_log_meta[0].change_start_position.get())
        self.round_robin_advance_distance.set(multi_log_meta[0].round_robin_advance_distance.get())
        self.file_name.set(multi_log_meta[0].file_name.get())
        self.file_uid.set(multi_log_meta[0].file_uid.get())
        self.file_size.set(multi_log_meta[0].file_size.get())
        self.file_ctime.set(multi_log_meta[0].file_ctime.get())
        self.file_mtime.set(multi_log_meta[0].file_mtime.get())
        self.oa_number.set(multi_log_meta[0].oa_number.get())
        self.oa_min_distance_between.set(multi_log_meta[0].oa_min_distance_between.get())
        self.oa_randomize.set(multi_log_meta[0].oa_randomize.get())
        self.oa_type.set(multi_log_meta[0].oa_type.get())
        self.h2h_number_of_bots.set(multi_log_meta[0].h2h_number_of_bots.get())
        self.h2h_speed.set(multi_log_meta[0].h2h_speed.get())
        self.h2h_min_distance_between.set(multi_log_meta[0].h2h_min_distance_between.get())
        self.h2h_randomize_bot_locations.set(multi_log_meta[0].h2h_randomize_bot_locations.get())
        self.h2h_allow_lane_changes.set(multi_log_meta[0].h2h_allow_lane_changes.get())
        self.h2h_lower_lane_change_time.set(multi_log_meta[0].h2h_lower_lane_change_time.get())
        self.h2h_upper_lane_change_time.set(multi_log_meta[0].h2h_upper_lane_change_time.get())
        self.h2h_lane_change_distance.set(multi_log_meta[0].h2h_lane_change_distance.get())
        self.action_space = multi_log_meta[0].action_space
        self.fixed_object_locations = multi_log_meta[0].fixed_object_locations

        # Initialize cumulative calculations to be in the log meta at the end
        episode_count = 0
        success_count = 0

        # Initialize comparative (best/worst) calculations to the first log meta (better behaviour than presuming 0)
        iteration_count = multi_log_meta[0].iteration_count.get()
        best_steps = multi_log_meta[0].best_steps.get()
        worst_steps = multi_log_meta[0].worst_steps.get()
        best_time = multi_log_meta[0].best_time.get()
        worst_time = multi_log_meta[0].worst_time.get()
        best_distance = multi_log_meta[0].best_distance.get()
        worst_distance = multi_log_meta[0].worst_distance.get()
        best_reward = multi_log_meta[0].best_reward.get()
        worst_reward = multi_log_meta[0].worst_reward.get()

        # Initialize averages which need to calculated from a sum ... tot up "total_for" each one and calculate later
        total_for_average_percent_complete = 0
        total_for_average_steps = 0
        total_for_average_time = 0
        total_for_average_distance = 0
        total_for_average_reward = 0

        m: LogMeta
        for m in multi_log_meta:
            # Many of the fields are same for all meta - the duplicate detection per field will catch any problems
            self.guru_version.set(m.guru_version.get())
            self.model_name.set(m.model_name.get())
            self.job_type.set(m.job_type.get())
            self.platform.set(m.platform.get())
            self.workers.set(m.workers.get())
            self.start_date.set(m.start_date.get())
            self.learning_algorithm.set(m.learning_algorithm.get())
            self.min_evaluations_per_iteration.set(m.min_evaluations_per_iteration.get())
            self.domain_randomization.set(m.domain_randomization.get())
            self.simulation_version.set(m.simulation_version.get())
            self.track_name.set(m.track_name.get())
            self.race_type.set(m.race_type.get())
            self.car_trim_colour.set(m.car_trim_colour.get())
            self.car_name.set(m.car_name.get())
            self.car_shell_type.set(m.car_shell_type.get())
            self.sensors.set(m.sensors.get())
            self.lidar_number_of_sectors.set(m.lidar_number_of_sectors.get())
            self.lidar_number_of_values_per_sector.set(m.lidar_number_of_values_per_sector.get())
            self.lidar_clipping_distance.set(m.lidar_clipping_distance.get())
            self.neural_network_topology.set(m.neural_network_topology.get())
            self.batch_size.set(m.batch_size.get())
            self.learning_rate.set(m.learning_rate.get())
            self.discount_factor.set(m.discount_factor.get())
            self.loss_type.set(m.loss_type.get())
            self.episodes_per_training_iteration.set(m.episodes_per_training_iteration.get())
            self.beta_entropy.set(m.beta_entropy.get())
            self.epochs.set(m.epochs.get())
            self.sac_alpha.set(m.sac_alpha.get())
            self.e_greedy_value.set(m.e_greedy_value.get())
            self.epsilon_steps.set(m.epsilon_steps.get())
            self.exploration_type.set(m.exploration_type.get())
            self.stack_size.set(m.stack_size.get())
            self.termination_average_score.set(m.termination_average_score.get())
            self.termination_max_episodes.set(m.termination_max_episodes.get())
            self.action_space_type.set(m.action_space_type.get())
            self.action_space_min_speed.set(m.action_space_min_speed.get())
            self.action_space_max_speed.set(m.action_space_max_speed.get())
            self.action_space_max_left_steering.set(m.action_space_max_left_steering.get())
            self.action_space_max_right_steering.set(m.action_space_max_right_steering.get())

            # Cumulative calculations
            episode_count += m.episode_count.get()
            success_count += m.success_count.get()

            # Comparative calculations
            iteration_count = max(iteration_count, m.iteration_count.get())
            best_steps = min(best_steps, m.best_steps.get())
            worst_steps = max(worst_steps, m.worst_steps.get())
            best_time = min(best_time, m.best_time.get())
            worst_time = max(worst_time, m.worst_time.get())
            best_distance = min(best_distance, m.best_distance.get())
            worst_distance = max(worst_distance, m.worst_distance.get())
            best_reward = max(best_reward, m.best_reward.get())
            worst_reward = min(worst_reward, m.worst_reward.get())

            # Totting up for averages
            total_for_average_percent_complete += m.average_percent_complete.get() * m.episode_count.get()
            total_for_average_reward += m.average_reward.get() * m.episode_count.get()

            if m.success_count.get() > 0:
                total_for_average_steps += m.average_steps.get() * m.success_count.get()         # BEWARE - Success laps
                total_for_average_time += m.average_time.get() * m.success_count.get()           # BEWARE - Success laps
                total_for_average_distance += m.average_distance.get() * m.success_count.get()   # BEWARE - Success laps

        # Finally we are ready to set the calculated stats combined from all the meta
        self.episode_count.set(episode_count)
        self.success_count.set(success_count)
        self.iteration_count.set(iteration_count)

        self.best_steps.set(best_steps)
        self.worst_steps.set(worst_steps)
        self.best_time.set(best_time)
        self.worst_time.set(worst_time)
        self.best_distance.set(best_distance)
        self.worst_distance.set(worst_distance)
        self.best_reward.set(best_reward)
        self.worst_reward.set(worst_reward)

        self.average_percent_complete.set(total_for_average_percent_complete / episode_count)
        self.average_reward.set(total_for_average_reward / episode_count)

        if success_count > 0:
            self.average_steps.set(round(total_for_average_steps / success_count))    # BEWARE - Success laps
            self.average_time.set(total_for_average_time / success_count)             # BEWARE - Success laps
            self.average_distance.set(total_for_average_distance / success_count)     # BEWARE - Success laps
        else:
            self.average_steps.set(0)
            self.average_time.set(0.0)
            self.average_distance.set(0.0)

    def _make_field(self, json_path: str, data_type: type, optionality: Optionality, min_value=None,
                    max_value=None) -> MetaField:
        new_field = MetaField(json_path, data_type, optionality, min_value, max_value)
        self._fields.append(new_field)
        return new_field

    def _set_meta_fields_based_on_action_space(self) -> None:
        if self.action_space.is_continuous():
            low_speed, high_speed, low_steering, high_steering = self.action_space.get_continuous_action_limits()
            self.action_space_type.set(ActionSpaceType.CONTINUOUS)
        else:
            low_speed, high_speed, low_steering, high_steering = self.action_space.get_discrete_action_limits()
            self.action_space_type.set(ActionSpaceType.DISCRETE)

        self.action_space_min_speed.set(float(low_speed))
        self.action_space_max_speed.set(float(high_speed))
        self.action_space_max_left_steering.set(float(high_steering))
        self.action_space_max_right_steering.set(float(low_steering))

    def _get_action_space_as_json_list(self) -> list:
        assert (not self.action_space.is_continuous())

        actions_json = []
        a: Action
        for a in self.action_space.get_all_actions():
            action_json = dict()
            action_json["speed"] = a.get_speed()
            action_json["steering_angle"] = a.get_steering_angle()
            actions_json.append(action_json)

        return actions_json

    def _get_action_space_from_json(self, received_json) -> ActionSpace:
        action_space = ActionSpace()
        if self.action_space_type.get() == ActionSpaceType.DISCRETE:
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
