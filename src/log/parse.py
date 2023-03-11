#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import json
import re
from datetime import date
from enum import Enum

from src.object_avoidance.fixed_object_locations import FixedObjectLocation, Lane
from src.event.event_meta import Event
from src.log.log_meta import LogMeta, NeuralNetworkTopology, Platform, RaceType, ObstacleType, LearningAlgorithm
from src.action_space.action import Action
from src.log.meta_field import MetaField

#
# PUBLIC Constants
#

EPISODE_STARTS_WITH = "SIM_TRACE_LOG"
SENT_SIGTERM = "Sent SIGTERM"
STILL_EVALUATING = "Reset agent"


#
# PUBLIC Interface
#

def parse_intro_event(line_of_text: str, log_meta: LogMeta):
    if DATE_LINE_CPU_WARNING in line_of_text:
        _parse_date_from_cpu_warning(line_of_text, log_meta)

    if DATE_LINE_PASSING_ARG in line_of_text:
        _parse_date_from_argument_message(line_of_text, log_meta)

    if line_of_text.startswith(DRFC_WORKER_INFO_LINE):
        _parse_drfc_worker_id(line_of_text, log_meta)

    if line_of_text.startswith("{'") and PARAM_JOB_TYPE in line_of_text and PARAM_WORLD_NAME in line_of_text:
        _parse_intro_event_parameters(line_of_text, log_meta)

    if line_of_text.startswith('  "') and ":" in line_of_text:
        _parse_hyperparameters(line_of_text, log_meta)

    if not log_meta.model_name.get():
        if line_of_text.startswith(MISC_MODEL_NAME_OLD_LOGS):
            log_meta.model_name.set(line_of_text.split("/")[1])

        if line_of_text.startswith(MISC_MODEL_NAME_NEW_LOGS_A) and \
                not line_of_text.startswith(MISC_MODEL_NAME_OLD_LOGS):
            log_meta.model_name.set(line_of_text.split("/")[2])

        if line_of_text.startswith(MISC_MODEL_NAME_NEW_LOGS_B):
            log_meta.model_name.set(line_of_text.split("/")[2])

        if line_of_text.startswith(MISC_MODEL_NAME_CLOUD_LOGS):
            split_parts = line_of_text[len(MISC_MODEL_NAME_CLOUD_LOGS):].split("/")
            if split_parts[1].startswith(CLOUD_TRAINING_YAML_FILENAME_A) or split_parts[1].startswith(
                    CLOUD_TRAINING_YAML_FILENAME_B):
                log_meta.model_name.set(re.sub("^ *", "", split_parts[0]))  # Strip off leading space(s)

    if line_of_text.startswith(SPECIAL_PARAMS_START_A) or line_of_text.startswith(SPECIAL_PARAMS_START_B):
        _parse_special_params(line_of_text, log_meta)

    if line_of_text.startswith(MISC_ACTION_SPACE_A):
        _parse_actions(line_of_text, log_meta, MISC_ACTION_SPACE_A)

    if line_of_text.startswith(MISC_ACTION_SPACE_B):
        _parse_actions(line_of_text, log_meta, MISC_ACTION_SPACE_B)


def parse_object_locations(line_of_text: str):
    if line_of_text.startswith(OBJECT_LOCATIONS):
        return json.loads(line_of_text[len(OBJECT_LOCATIONS):])
    else:
        return None


def parse_episode_event(line_of_text: str, episode_events, episode_object_locations,
                        saved_events, saved_debug, saved_object_locations, is_continuous_action_space: bool) -> None:
    if len(saved_events) > 15:
        print(line_of_text)

    assert len(saved_events) < 20

    if not episode_events:
        episode_events.append([])
        episode_object_locations.append([])

    input_line = line_of_text.split("\n", 1)[0]

    if is_continuous_action_space:
        (episode,
         step,
         x,
         y,
         heading,
         steering_angle,
         speed,
         action_taken,
         action_taken_2,
         reward,
         job_completed,
         all_wheels_on_track,
         progress,
         closest_waypoint_index,
         track_length,
         time,
         status) = input_line[14:].split(",")[:17]

        if "]" not in action_taken_2:
            (episode,
             step,
             x,
             y,
             heading,
             steering_angle,
             speed,
             action_taken,
             reward,
             job_completed,
             all_wheels_on_track,
             progress,
             closest_waypoint_index,
             track_length,
             time,
             status) = input_line[14:].split(",")[:16]
    else:
        (episode,
         step,
         x,
         y,
         heading,
         steering_angle,
         speed,
         action_taken,
         reward,
         job_completed,
         all_wheels_on_track,
         progress,
         closest_waypoint_index,
         track_length,
         time,
         status) = input_line[14:].split(",")[:16]

    event_meta = Event()

    event_meta.episode = int(episode)
    event_meta.step = int(step)
    event_meta.x = float(x)
    event_meta.y = float(y)
    event_meta.heading = float(heading)
    event_meta.steering_angle = float(steering_angle)
    event_meta.speed = float(speed)
    if is_continuous_action_space:
        event_meta.action_taken = None
    else:
        event_meta.action_taken = int(action_taken)
    event_meta.reward = float(reward)
    event_meta.job_completed = (job_completed == "True")
    event_meta.all_wheels_on_track = (all_wheels_on_track == "True")
    event_meta.progress = float(progress)
    event_meta.closest_waypoint_index = int(closest_waypoint_index)
    event_meta.time = float(time)
    event_meta.status = status
    event_meta.track_length = float(track_length)

    event_meta.debug_log = saved_debug

    if event_meta.step > len(episode_events[-1]) + 1 or event_meta.episode > len(episode_events) - 1:
        saved_events.append(event_meta)
        return

    assert event_meta.episode == len(episode_events) - 1
    assert len(episode_events) == len(episode_object_locations)

    if event_meta.step != len(episode_events[-1]) + 1:
        print("WARNING - something wrong near step " + str(event_meta.step) +
              " of episode " + str(len(episode_events) - 1))

    episode_events[-1].append(event_meta)
    if event_meta.job_completed:
        episode_events.append([])
        episode_object_locations.append([])

    if saved_object_locations and not episode_object_locations[-1]:
        episode_object_locations[-1] = saved_object_locations

    added = True
    while added:
        added = False
        for s in saved_events:
            if s.step == len(episode_events[-1]) + 1 and s.episode == len(episode_events) - 1:
                episode_events[-1].append(s)
                saved_events.remove(s)
                added = True
                if s.job_completed:
                    episode_events.append([])
                    episode_object_locations.append([])
                break


def parse_evaluation_reward_info(line_of_text: str):
    if line_of_text.startswith(EVALUATION_REWARD_START):
        return float(line_of_text[len(EVALUATION_REWARD_START):])
    else:
        return None


def parse_evaluation_progress_info(line_of_text: str):
    start_str_len = 0
    if line_of_text.startswith(EVALUATION_PROGRESSES_START_OLD):
        start_str_len = len(EVALUATION_PROGRESSES_START_OLD)
    elif line_of_text.startswith(EVALUATION_PROGRESSES_START):
        start_str_len = len(EVALUATION_PROGRESSES_START)

    if start_str_len > 0:
        info = line_of_text[start_str_len:]
        count = int(info.split(" ")[0])

        progresses_as_strings = info[:-2].split("[")[1].split(",")
        progresses = []
        for p in progresses_as_strings:
            progresses.append(max(0.0, float(p)))  # Added max with zero to avoid rare oddity of negative progress!!!

        assert count == len(progresses)

        return progresses
    else:
        return None


#
# PRIVATE Constants and Implementation
#

HYPER_BATCH_SIZE = "batch_size"
HYPER_ENTROPY = "beta_entropy"
HYPER_DISCOUNT_FACTOR = "discount_factor"
HYPER_LOSS_TYPE = "loss_type"
HYPER_LEARNING_RATE = "lr"
HYPER_EPISODES_BETWEEN_TRAINING = "num_episodes_between_training"
HYPER_EPOCHS = "num_epochs"
HYPER_SAC_ALPHA = "sac_alpha"
HYPER_GREEDY = "e_greedy_value"
HYPER_EPSILON_STEPS = "epsilon_steps"
HYPER_EXPLORATION_TYPE = "exploration_type"
HYPER_STACK_SIZE = "stack_size"
HYPER_TERM_AVG_SCORE = "term_cond_avg_score"
HYPER_TERM_MAX_EPISODES = "term_cond_max_episodes"

PARAM_WORLD_NAME = "WORLD_NAME"
PARAM_RACE_TYPE = "RACE_TYPE"
PARAM_JOB_TYPE = "JOB_TYPE"
PARAM_DOMAIN_RANDOMIZATION = "ENABLE_DOMAIN_RANDOMIZATION"
PARAM_NUM_WORKERS = "NUM_WORKERS"

PARAM_CAR_NAME = "CAR_NAME"
PARAM_BODY_SHELL_TYPE = "BODY_SHELL_TYPE"
PARAM_CAR_COLOR = "CAR_COLOR"

PARAM_OA_NUMBER_OF_OBSTACLES = "NUMBER_OF_OBSTACLES"
PARAM_OA_MIN_DISTANCE_BETWEEN_OBSTACLES = "MIN_DISTANCE_BETWEEN_OBSTACLES"
PARAM_OA_RANDOMIZE_OBSTACLE_LOCATIONS = "RANDOMIZE_OBSTACLE_LOCATIONS"
PARAM_OA_OBSTACLE_TYPE = "OBSTACLE_TYPE"
PARAM_OA_IS_OBSTACLE_BOT_CAR = "IS_OBSTACLE_BOT_CAR"
PARAM_OA_OBJECT_POSITIONS = "OBJECT_POSITIONS"

PARAM_H2H_NUMBER_OF_BOT_CARS = "NUMBER_OF_BOT_CARS"
PARAM_H2H_BOT_CAR_SPEED = "BOT_CAR_SPEED"
PARAM_H2H_MIN_DISTANCE_BETWEEN = "MIN_DISTANCE_BETWEEN_BOT_CARS"
PARAM_H2H_RANDOMIZE_BOT_LOCATIONS = "RANDOMIZE_BOT_CAR_LOCATIONS"
PARAM_H2H_IS_LANE_CHANGE = "IS_LANE_CHANGE"
PARAM_H2H_LOWER_LANE_CHANGE_TIME = "LOWER_LANE_CHANGE_TIME"
PARAM_H2H_UPPER_LANE_CHANGE_TIME = "UPPER_LANE_CHANGE_TIME"
PARAM_H2H_LANE_CHANGE_DISTANCE = "LANE_CHANGE_DISTANCE"

PARAM_ALTERNATE_DRIVING_DIRECTION = "ALTERNATE_DRIVING_DIRECTION"
PARAM_START_POSITION_OFFSET = "START_POSITION_OFFSET"
PARAM_MIN_EVAL_TRIALS = "MIN_EVAL_TRIALS"
PARAM_CHANGE_START_POSITION = "CHANGE_START_POSITION"
PARAM_ROUND_ROBIN_ADVANCE_DIST = "ROUND_ROBIN_ADVANCE_DIST"

MISC_MODEL_NAME_OLD_LOGS = "Successfully downloaded model metadata from model-metadata/"
MISC_MODEL_NAME_NEW_LOGS_A = "Successfully downloaded model metadata"
MISC_MODEL_NAME_NEW_LOGS_B = "[s3] Successfully downloaded model metadata"

DATE_LINE_CPU_WARNING = "Your CPU supports instructions "
DATE_LINE_PASSING_ARG = "passing arg to libvncserver"

DRFC_WORKER_INFO_LINE = "Starting as worker "

SPECIAL_PARAMS_START_A = "Sensor list ['"
SPECIAL_PARAMS_START_B = "Sensor list [u'"
CONTINUOUS_ACTION_SPACE_CONTAINS = "action_space_type continuous"
SIMAPP_VERSION_CONTAINS = ", simapp_version "
SENSOR_LIST_CONTAINS = "Sensor list "
LIDAR_CONFIG_CONTAINS = " lidar_config "
NEURAL_TOPOLOGY_CONTAINS = "], network "
TRAINING_ALGORITHM_CONTAINS = ", training_algorithm "

# For handling cloud, here are the example of cloud and non-cloud
#   cloud       [s3] Successfully downloaded yaml file from s3 key DMH-Champ-Round1-OA-B-3/training-params.yaml
#   non-cloud   [s3] Successfully downloaded yaml file from s3 key data-56b52007-8142-46cd-a9cc-370feb620f0c/models/Champ-Obj-Avoidance-03/sagemaker-robomaker-artifacts/training_params_634ecc9a-b12d-4350-99ac-3320f88e9fbe.yaml to local ./custom_files/training_params_634ecc9a-b12d-4350-99ac-3320f88e9fbe.yaml.

MISC_MODEL_NAME_CLOUD_LOGS = "[s3] Successfully downloaded yaml file from s3 key"
CLOUD_TRAINING_YAML_FILENAME_A = "training_params.yaml"  # New
CLOUD_TRAINING_YAML_FILENAME_B = "training-params.yaml"  # Older logs

MISC_ACTION_SPACE_A = "Loaded action space from file: "
MISC_ACTION_SPACE_B = "Action space from file: "

OBJECT_LOCATIONS = "DRG-OBJECTS:"

EVALUATION_REWARD_START = "## agent: Finished evaluation phase. Success rate = 0.0, Avg Total Reward = "
EVALUATION_PROGRESSES_START_OLD = "Number of evaluations: "
EVALUATION_PROGRESSES_START = "[BestModelSelection] Number of evaluations: "


def _parse_date_from_cpu_warning(line_of_text: str, log_meta: LogMeta) -> None:
    # Example:
    # 2023-02-05 16:23:13.599375: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
    #
    if not log_meta.start_date.get():    # Edge condition, date can cross midnight, so trust only the 1st one found
        start_date = date.fromisoformat(line_of_text.split(" ")[0])
        log_meta.start_date.set(str(start_date))


def _parse_date_from_argument_message(line_of_text: str, log_meta: LogMeta) -> None:
    # Example:
    # 10/07/2022 13:55:29 passing arg to libvncserver: -rfbport
    #
    if not log_meta.start_date.get():    # Edge condition, date can cross midnight, so trust only the 1st one found
        date_parts = line_of_text.split(" ")[0].split("/")
        start_date = date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
        log_meta.start_date.set(str(start_date))


def _parse_drfc_worker_id(line_of_text: str, log_meta: LogMeta) -> None:
    # Example:
    # Starting as worker 0, using world 2022_july_pro and configuration training_params.yaml.
    #
    log_meta.platform.set(Platform.DEEPRACER_FOR_CLOUD)
    pos = line_of_text.find(DRFC_WORKER_INFO_LINE)
    log_meta.worker_id.set(int(line_of_text[pos + len(DRFC_WORKER_INFO_LINE):].split(",")[0]))


def _parse_hyperparameters(line_of_text: str, log_meta: LogMeta) -> None:
    # Example:
    #   "batch_size": 256,
    #   "beta_entropy": 0.01,
    #   "discount_factor": 0.97,
    #   "e_greedy_value": 0.05,
    #   "epsilon_steps": 10000,
    #   "exploration_type": "categorical",
    #   "loss_type": "huber",
    #   "lr": 0.0003,
    #   "num_episodes_between_training": 40,
    #   "num_epochs": 5,
    #   "stack_size": 1,
    #   "term_cond_avg_score": 35000.0,
    #   "term_cond_max_episodes": 100000
    _set_hyper_integer_value(line_of_text, HYPER_BATCH_SIZE, log_meta.batch_size)
    _set_hyper_float_value(line_of_text, HYPER_ENTROPY, log_meta.beta_entropy)
    _set_hyper_float_value(line_of_text, HYPER_DISCOUNT_FACTOR, log_meta.discount_factor)
    _set_hyper_string_value(line_of_text, HYPER_LOSS_TYPE, log_meta.loss_type, convert_to_enum=True)
    _set_hyper_float_value(line_of_text, HYPER_LEARNING_RATE, log_meta.learning_rate)
    _set_hyper_integer_value(line_of_text, HYPER_EPISODES_BETWEEN_TRAINING, log_meta.episodes_per_training_iteration)
    _set_hyper_integer_value(line_of_text, HYPER_EPOCHS, log_meta.epochs)
    _set_hyper_float_value(line_of_text, HYPER_SAC_ALPHA, log_meta.sac_alpha)
    _set_hyper_float_value(line_of_text, HYPER_GREEDY, log_meta.e_greedy_value)
    _set_hyper_integer_value(line_of_text, HYPER_EPSILON_STEPS, log_meta.epsilon_steps)
    _set_hyper_string_value(line_of_text, HYPER_EXPLORATION_TYPE, log_meta.exploration_type, convert_to_enum=True)
    _set_hyper_integer_value(line_of_text, HYPER_STACK_SIZE, log_meta.stack_size)
    _set_hyper_float_value(line_of_text, HYPER_TERM_AVG_SCORE, log_meta.termination_average_score)
    _set_hyper_integer_value(line_of_text, HYPER_TERM_MAX_EPISODES, log_meta.termination_max_episodes)


def _parse_special_params(line_of_text: str, log_meta: LogMeta) -> None:
    # Example line_of_text    (second example is from an older log in 2020)
    #
    # Sensor list ['SECTOR_LIDAR', 'STEREO_CAMERAS'], network DEEP_CONVOLUTIONAL_NETWORK_SHALLOW, simapp_version 5.0, training_algorithm clipped_ppo, action_space_type discrete lidar_config {'num_sectors': 8, 'num_values_per_sector': 8, 'clipping_dist': 2.0}
    # Sensor list [u'FRONT_FACING_CAMERA'], network DEEP_CONVOLUTIONAL_NETWORK_SHALLOW, simapp_version 3.0

    if CONTINUOUS_ACTION_SPACE_CONTAINS in line_of_text:
        log_meta.action_space.mark_as_continuous()

    pos = line_of_text.find(SIMAPP_VERSION_CONTAINS)
    log_meta.simulation_version.set(line_of_text[pos + len(SIMAPP_VERSION_CONTAINS):][:3])

    pos = line_of_text.find(NEURAL_TOPOLOGY_CONTAINS)
    topology = line_of_text[pos + len(NEURAL_TOPOLOGY_CONTAINS):].split(",")[0]
    assert topology == "DEEP_CONVOLUTIONAL_NETWORK_SHALLOW"
    log_meta.neural_network_topology.set(NeuralNetworkTopology.DEEP_CONVOLUTIONAL_3_LAYER)

    if TRAINING_ALGORITHM_CONTAINS in line_of_text:
        pos = line_of_text.find(TRAINING_ALGORITHM_CONTAINS)
        log_meta.learning_algorithm.set_enum_str(
            line_of_text[pos + len(TRAINING_ALGORITHM_CONTAINS):].split(",")[0].upper())
    else:
        log_meta.learning_algorithm.set(LearningAlgorithm.CLIPPED_PPO)

    if SENSOR_LIST_CONTAINS in line_of_text:
        pos = line_of_text.find(SENSOR_LIST_CONTAINS)
        data_string = '{"sensors": ' + line_of_text[pos + len(SENSOR_LIST_CONTAINS):].split("]")[0] + "]}"
        data_string = data_string.replace("[u'", "['").replace(", u'", ", '").replace("'", "\"")
        sensors_list: list = json.loads(data_string)["sensors"]
        if "FRONT_FACING_CAMERA" in sensors_list:
            sensors_list.remove("FRONT_FACING_CAMERA")
            sensors_list.append("SINGLE_CAMERA")
        log_meta.sensors.set(sensors_list)

        if LIDAR_CONFIG_CONTAINS in line_of_text and ("LIDAR" in sensors_list or "SECTOR_LIDAR" in sensors_list):
            pos = line_of_text.find(LIDAR_CONFIG_CONTAINS)
            data_string = line_of_text[pos + len(LIDAR_CONFIG_CONTAINS):].split("}")[0] + "}"
            data_fields = json.loads(data_string.replace("'", "\""))
            log_meta.lidar_number_of_sectors.set(data_fields["num_sectors"])
            log_meta.lidar_number_of_values_per_sector.set(data_fields["num_values_per_sector"])
            log_meta.lidar_clipping_distance.set(data_fields["clipping_dist"])


def _parse_intro_event_parameters(line_of_text: str, log_meta: LogMeta) -> None:
    # Console example:
    # {'METRICS_S3_BUCKET': ['aws-deepracer-data-us-east-1-1'], 'METRICS_S3_OBJECT_KEY': ['data-56b52007-8142-46cd-a9cc-370feb620f0c/models/278f5eae-b941-48e4-a859-cc4a25400115/metrics/training/training-20230205161827-mZZbUMgvSsyoj6lPD7G4NA.json'], 'SIMTRACE_S3_PREFIX': 'data-56b52007-8142-46cd-a9cc-370feb620f0c/models/278f5eae-b941-48e4-a859-cc4a25400115/sim-trace/training', 'SAGEMAKER_SHARED_S3_BUCKET': ['aws-deepracer-data-us-east-1-1'], 'JOB_TYPE': 'TRAINING', 'METRIC_NAMESPACE': 'AWSDeepRacer', 'TARGET_REWARD_SCORE': 'None', 'RACE_TYPE': 'OBJECT_AVOIDANCE', 'WORLD_NAME': '2022_reinvent_champ', 'MP4_S3_OBJECT_PREFIX': 'data-56b52007-8142-46cd-a9cc-370feb620f0c/models/278f5eae-b941-48e4-a859-cc4a25400115/videos/training/training-20230205161827-mZZbUMgvSsyoj6lPD7G4NA', 'ROBOMAKER_SIMULATION_JOB_ACCOUNT_ID': '372026249783', 'TRAINING_JOB_ARN': 'arn:aws:deepracer:us-east-1:694264024003:training_job/mZZbUMgvSsyoj6lPD7G4NA', 'RANDOMIZE_OBSTACLE_LOCATIONS': 'true', 'ALTERNATE_DRIVING_DIRECTION': 'false', 'CAR_COLOR': ['Blue'], 'REWARD_FILE_S3_KEY': 'data-56b52007-8142-46cd-a9cc-370feb620f0c/models/278f5eae-b941-48e4-a859-cc4a25400115/reward_function.py', 'OBSTACLE_TYPE': 'box_obstacle', 'METRIC_NAME': 'TrainingRewardScore', 'AWS_REGION': 'us-east-1', 'MP4_S3_BUCKET': 'aws-deepracer-data-us-east-1-1', 'S3_KMS_CMK_ARN': 'arn:aws:kms:us-east-1:372026249783:key/82661b8b-a07c-4982-9c61-a5b83f3f2023', 'CAR_NAME': 'dfgdfgdgs', 'SIMTRACE_S3_BUCKET': 'aws-deepracer-data-us-east-1-1', 'BODY_SHELL_TYPE': ['deepracer'], 'KINESIS_VIDEO_STREAM_NAME': 'dr-kvs-372026249783-20230205161826-859bb483-3cd5-468d-903c-a79869a65332', 'SAGEMAKER_SHARED_S3_PREFIX': ['data-56b52007-8142-46cd-a9cc-370feb620f0c/models/278f5eae-b941-48e4-a859-cc4a25400115/sagemaker-robomaker-artifacts'], 'CHANGE_START_POSITION': 'true', 'NUMBER_OF_EPISODES': '0', 'NUMBER_OF_OBSTACLES': '2', 'MODEL_METADATA_FILE_S3_KEY': ['data-56b52007-8142-46cd-a9cc-370feb620f0c/models/278f5eae-b941-48e4-a859-cc4a25400115/model_metadata.json']}
    #
    # DRFC example:
    # {'ALTERNATE_DRIVING_DIRECTION': 'False', 'AWS_REGION': 'us-east-1', 'BODY_SHELL_TYPE': ['deepracer'], 'BOT_CAR_SPEED': '2.5', 'CAR_COLOR': ['Black'], 'CAR_NAME': 'FastCar', 'CHANGE_START_POSITION': 'True', 'DISPLAY_NAME': 'FastCar', 'ENABLE_DOMAIN_RANDOMIZATION': 'False', 'IS_LANE_CHANGE': 'True', 'JOB_TYPE': 'TRAINING', 'KINESIS_VIDEO_STREAM_NAME': 'None', 'LANE_CHANGE_DISTANCE': '1.0', 'LOWER_LANE_CHANGE_TIME': '3.0', 'METRICS_S3_BUCKET': ['dmh-base-2023-jan-bucket-1x1o0jxxrxubo'], 'METRICS_S3_OBJECT_KEY': ['Head-To-Bot-Test/metrics/TrainingMetrics.json'], 'MIN_DISTANCE_BETWEEN_BOT_CARS': '2.0', 'MIN_EVAL_TRIALS': '5', 'MODEL_METADATA_FILE_S3_KEY': ['custom_files/model_metadata.json'], 'NUMBER_OF_BOT_CARS': '3', 'NUM_WORKERS': '2', 'PENALTY_SECONDS': '5.0', 'RACER_NAME': 'FastCar', 'RACE_TYPE': 'HEAD_TO_BOT', 'RANDOMIZE_BOT_CAR_LOCATIONS': 'True', 'REWARD_FILE_S3_KEY': 'custom_files/reward_function.py', 'ROBOMAKER_SIMULATION_JOB_ACCOUNT_ID': 'Dummy', 'ROUND_ROBIN_ADVANCE_DIST': '0.1', 'SAGEMAKER_SHARED_S3_BUCKET': ['dmh-base-2023-jan-bucket-1x1o0jxxrxubo'], 'SAGEMAKER_SHARED_S3_PREFIX': ['Head-To-Bot-Test'], 'SIMTRACE_S3_BUCKET': 'dmh-base-2023-jan-bucket-1x1o0jxxrxubo', 'SIMTRACE_S3_PREFIX': 'Head-To-Bot-Test', 'START_POSITION_OFFSET': '0.0', 'TRAINING_JOB_ARN': 'arn:Dummy', 'UPPER_LANE_CHANGE_TIME': '5.0', 'WORLD_NAME': '2022_reinvent_champ'}
    #
    if log_meta.platform.get() is None:
        log_meta.platform.set(Platform.AWS_CONSOLE)
        log_meta.workers.set(1)
        log_meta.worker_id.set(0)

    parameters = json.loads(line_of_text.replace("'", "\""))

    _set_parameter_string_value(parameters, PARAM_WORLD_NAME, log_meta.track_name)
    _set_parameter_string_value(parameters, PARAM_JOB_TYPE, log_meta.job_type, convert_to_enum=True)
    _set_parameter_boolean_value(parameters, PARAM_DOMAIN_RANDOMIZATION, log_meta.domain_randomization)
    _set_parameter_integer_value(parameters, PARAM_NUM_WORKERS, log_meta.workers)
    if log_meta.platform.get() == Platform.DEEPRACER_FOR_CLOUD:
        _set_parameter_string_value(parameters, "SIMTRACE_S3_PREFIX", log_meta.model_name)

    _set_parameter_string_value(parameters, PARAM_CAR_NAME, log_meta.car_name)
    _set_parameter_string_value(parameters, PARAM_BODY_SHELL_TYPE, log_meta.car_shell_type, is_within_list=True)
    _set_parameter_string_value(parameters, PARAM_CAR_COLOR, log_meta.car_trim_colour, is_within_list=True,
                                convert_to_upper=True, convert_to_enum=True)

    if PARAM_OA_OBJECT_POSITIONS in parameters:
        positions = parameters[PARAM_OA_OBJECT_POSITIONS]
        assert (isinstance(positions, list))
        # Example: ['0.1,-1', '0.25,1', '0.4,-1', '0.55,1', '0.7,-1']
        # where -1 is OUTSIDE      and +1 means INSIDE
        for p in positions:
            parts = p.split(",")
            log_meta.fixed_object_locations.add(FixedObjectLocation(float(parts[0]), Lane(int(parts[1]))))

    _set_parameter_string_value(parameters, PARAM_RACE_TYPE, log_meta.race_type,
                                {"HEAD_TO_HEAD_RACING": RaceType.HEAD_TO_HEAD,
                                 "HEAD_TO_BOT": RaceType.HEAD_TO_HEAD}, convert_to_enum=True)

    if log_meta.race_type.get() != RaceType.TIME_TRIAL:  # Important because H2H can be trained with obstacles too
        _set_parameter_integer_value(parameters, PARAM_OA_NUMBER_OF_OBSTACLES, log_meta.oa_number)
        _set_parameter_float_value(parameters, PARAM_OA_MIN_DISTANCE_BETWEEN_OBSTACLES,
                                   log_meta.oa_min_distance_between)
        _set_parameter_boolean_value(parameters, PARAM_OA_RANDOMIZE_OBSTACLE_LOCATIONS, log_meta.oa_randomize)
        _set_parameter_string_value(parameters, PARAM_OA_OBSTACLE_TYPE, log_meta.oa_type,
                                    {"deepracer_box_obstacle": ObstacleType.PURPLE_BOX,
                                     "box_obstacle": ObstacleType.BROWN_BOX}, convert_to_enum=True)

    if log_meta.race_type.get() == RaceType.HEAD_TO_HEAD:
        _set_parameter_integer_value(parameters, PARAM_H2H_NUMBER_OF_BOT_CARS, log_meta.h2h_number_of_bots)
        _set_parameter_float_value(parameters, PARAM_H2H_BOT_CAR_SPEED, log_meta.h2h_speed)

        _set_parameter_float_value(parameters, PARAM_H2H_MIN_DISTANCE_BETWEEN,
                                   log_meta.h2h_min_distance_between)
        _set_parameter_boolean_value(parameters, PARAM_H2H_RANDOMIZE_BOT_LOCATIONS,
                                     log_meta.h2h_randomize_bot_locations)

        _set_parameter_boolean_value(parameters, PARAM_H2H_IS_LANE_CHANGE, log_meta.h2h_allow_lane_changes)
        if log_meta.h2h_allow_lane_changes.get():
            _set_parameter_float_value(parameters, PARAM_H2H_LOWER_LANE_CHANGE_TIME,
                                       log_meta.h2h_lower_lane_change_time)
            _set_parameter_float_value(parameters, PARAM_H2H_UPPER_LANE_CHANGE_TIME,
                                       log_meta.h2h_upper_lane_change_time)
            _set_parameter_float_value(parameters, PARAM_H2H_LANE_CHANGE_DISTANCE,
                                       log_meta.h2h_lane_change_distance)

    _set_parameter_boolean_value(parameters, PARAM_ALTERNATE_DRIVING_DIRECTION, log_meta.alternate_direction)
    _set_parameter_float_value(parameters, PARAM_START_POSITION_OFFSET, log_meta.start_position_offset, 0.0)
    _set_parameter_integer_value(parameters, PARAM_MIN_EVAL_TRIALS, log_meta.min_evaluations_per_iteration)
    _set_parameter_boolean_value(parameters, PARAM_CHANGE_START_POSITION, log_meta.change_start_position)
    if log_meta.change_start_position.get():
        _set_parameter_float_value(parameters, PARAM_ROUND_ROBIN_ADVANCE_DIST, log_meta.round_robin_advance_distance,
                                   0.05)

    if PARAM_OA_IS_OBSTACLE_BOT_CAR in parameters:
        if _text_to_bool(parameters[PARAM_OA_IS_OBSTACLE_BOT_CAR]):
            log_meta.oa_type.set(ObstacleType.BOT_CAR)
        else:
            log_meta.oa_type.set(ObstacleType.BROWN_BOX)


def _parse_actions(line_of_text: str, log_meta: LogMeta, starts_with: str):
    raw_actions = line_of_text[len(starts_with):].replace("'", "\"")

    actions = json.loads(raw_actions)

    if log_meta.action_space.is_continuous():
        low_speed = actions["speed"]["low"]
        high_speed = actions["speed"]["high"]
        low_steering = actions["steering_angle"]["low"]
        high_steering = actions["steering_angle"]["high"]
        log_meta.action_space.define_continuous_action_limits(low_speed, high_speed, low_steering, high_steering)
    else:
        for index, a in enumerate(actions):
            if "index" in a:
                assert a["index"] == index
            new_action = Action(index, a["speed"], a["steering_angle"])
            log_meta.action_space.add_action(new_action)


# Parse hyper parameters

def _contains_hyper(line_of_text: str, hyper_name: str):
    return line_of_text.startswith('  "' + hyper_name + '": ')


def _set_hyper_integer_value(line_of_text: str, hyper_name: str, meta_field: MetaField):
    if _contains_hyper(line_of_text, hyper_name):
        chop_chars = len(hyper_name) + 6
        meta_field.set(int(line_of_text[chop_chars:].split(",")[0]))


def _set_hyper_float_value(line_of_text: str, hyper_name: str, meta_field: MetaField):
    if _contains_hyper(line_of_text, hyper_name):
        chop_chars = len(hyper_name) + 6
        meta_field.set(float(line_of_text[chop_chars:].split(",")[0]))


def _set_hyper_string_value(line_of_text: str, hyper_name: str, meta_field: MetaField, convert_to_enum: bool = False):
    if _contains_hyper(line_of_text, hyper_name):
        chop_chars = len(hyper_name) + 6
        new_value = line_of_text[chop_chars:].split('"')[1].upper().replace(" ", "_")
        if convert_to_enum:
            meta_field.set_enum_str(new_value)
        else:
            meta_field.set(new_value)


# Parse the high level training settings

def _set_parameter_string_value(parameters: dict, parameter_name: str, meta_field: MetaField,
                                replacements: dict = None, default=None, is_within_list: bool = False, convert_to_upper: bool = False, convert_to_enum: bool = False):
    if parameter_name in parameters:
        value = parameters[parameter_name]
        if is_within_list:
            assert isinstance(value, list)
            assert len(value) == 1
            value = value[0]
        if convert_to_upper:
            value = value.upper()
        if replacements is not None and value in replacements:
            value = replacements[value]
        if convert_to_enum and not isinstance(value, Enum):
            meta_field.set_enum_str(value)
        else:
            meta_field.set(value)
    elif default is not None:
        meta_field.set(default)


def _set_parameter_integer_value(parameters: dict, parameter_name: str, meta_field: MetaField, default=None):
    if parameter_name in parameters:
        meta_field.set(int(parameters[parameter_name]))
    elif default is not None:
        meta_field.set(default)


def _set_parameter_float_value(parameters: dict, parameter_name: str, meta_field: MetaField, default=None):
    if parameter_name in parameters:
        meta_field.set(float(parameters[parameter_name]))
    elif default is not None:
        meta_field.set(default)


def _set_parameter_boolean_value(parameters: dict, parameter_name: str, meta_field: MetaField, default=None):
    if parameter_name in parameters:
        meta_field.set(_text_to_bool(parameters[parameter_name]))
    elif default is not None:
        meta_field.set(default)


def _text_to_bool(text: str) -> bool:
    value = text.upper().replace(" ", "").replace("\n", "")
    assert value in ("TRUE", "FALSE")
    return value == "TRUE"
