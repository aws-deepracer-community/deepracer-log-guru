#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import json
import re

from src.event.event_meta import Event
from src.log.log_meta import LogMeta
from src.action_space.action import Action
from src.log.meta_field import MetaField

#
# PUBLIC Constants and Interface
#

EPISODE_STARTS_WITH = "SIM_TRACE_LOG"
SENT_SIGTERM = "Sent SIGTERM"
STILL_EVALUATING = "Reset agent"


def parse_intro_event(line_of_text: str, log_meta: LogMeta):
    if line_of_text.startswith("{'") and PARAM_JOB_TYPE in line_of_text and PARAM_WORLD_NAME in line_of_text:
        parameters = json.loads(line_of_text.replace("'", "\""))

        _set_parameter_string_value(parameters, PARAM_WORLD_NAME, log_meta.world_name)
        _set_parameter_string_value(parameters, PARAM_JOB_TYPE, log_meta.job_type)

        if PARAM_OA_OBJECT_POSITIONS in parameters:
            log_meta.oa_locations.set("TODO")     # TODO

        _set_parameter_string_value(parameters, PARAM_RACE_TYPE, log_meta.race_type,
                                    {"HEAD_TO_HEAD_RACING": "HEAD_TO_HEAD"})

        _set_parameter_integer_value(parameters, PARAM_OA_NUMBER_OF_OBSTACLES, log_meta.oa_number)
        _set_parameter_float_value(parameters, PARAM_OA_MIN_DISTANCE_BETWEEN_OBSTACLES,
                                   log_meta.oa_min_distance_between)
        _set_parameter_boolean_value(parameters, PARAM_OA_RANDOMIZE_OBSTACLE_LOCATIONS, log_meta.oa_randomize)
        _set_parameter_string_value(parameters, PARAM_OA_OBSTACLE_TYPE, log_meta.oa_type,
                                    {"deepracer_box_obstacle": "PURPLE_BOX"})

        _set_parameter_integer_value(parameters, PARAM_H2H_NUMBER_OF_BOT_CARS, log_meta.h2h_number)
        _set_parameter_float_value(parameters, PARAM_H2H_BOT_CAR_SPEED, log_meta.h2h_speed)

        if PARAM_OA_IS_OBSTACLE_BOT_CAR in parameters:
            if _text_to_bool(parameters[PARAM_OA_IS_OBSTACLE_BOT_CAR]):
                log_meta.oa_type.set("BOT_CAR")
            else:
                log_meta.oa_type.set("BROWN_BOX")

    _set_hyper_integer_value(line_of_text, HYPER_BATCH_SIZE, log_meta.batch_size)
    _set_hyper_float_value(line_of_text, HYPER_ENTROPY, log_meta.beta_entropy)
    _set_hyper_float_value(line_of_text, HYPER_DISCOUNT_FACTOR, log_meta.discount_factor)
    _set_hyper_string_value(line_of_text, HYPER_LOSS_TYPE, log_meta.loss_type)
    _set_hyper_float_value(line_of_text, HYPER_LEARNING_RATE, log_meta.learning_rate)
    _set_hyper_integer_value(line_of_text, HYPER_EPISODES_BETWEEN_TRAINING, log_meta.episodes_per_training_iteration)
    _set_hyper_integer_value(line_of_text, HYPER_EPOCHS, log_meta.epochs)
    _set_hyper_float_value(line_of_text, HYPER_SAC_ALPHA, log_meta.sac_alpha)
    _set_hyper_float_value(line_of_text, HYPER_GREEDY, log_meta.e_greedy_value)
    _set_hyper_integer_value(line_of_text, HYPER_EPSILON_STEPS, log_meta.epsilon_steps)
    _set_hyper_string_value(line_of_text, HYPER_EXPLORATION_TYPE, log_meta.exploration_type)
    _set_hyper_integer_value(line_of_text, HYPER_STACK_SIZE, log_meta.stack_size)
    _set_hyper_float_value(line_of_text, HYPER_TERM_AVG_SCORE, log_meta.termination_average_score)
    _set_hyper_integer_value(line_of_text, HYPER_TERM_MAX_EPISODES, log_meta.termination_max_episodes)

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

    if line_of_text.startswith(CONTINUOUS_ACTION_SPACE_START) and CONTINUOUS_ACTION_SPACE_CONTAINS in line_of_text:
        log_meta.action_space.mark_as_continuous()

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
                        saved_events, saved_debug, saved_object_locations, is_continuous_action_space: bool):
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

PARAM_OA_NUMBER_OF_OBSTACLES = "NUMBER_OF_OBSTACLES"
PARAM_OA_MIN_DISTANCE_BETWEEN_OBSTACLES = "MIN_DISTANCE_BETWEEN_OBSTACLES"
PARAM_OA_RANDOMIZE_OBSTACLE_LOCATIONS = "RANDOMIZE_OBSTACLE_LOCATIONS"
PARAM_OA_OBSTACLE_TYPE = "OBSTACLE_TYPE"
PARAM_OA_IS_OBSTACLE_BOT_CAR = "IS_OBSTACLE_BOT_CAR"
PARAM_OA_OBJECT_POSITIONS = "OBJECT_POSITIONS"

PARAM_H2H_NUMBER_OF_BOT_CARS = "NUMBER_OF_BOT_CARS"
PARAM_H2H_BOT_CAR_SPEED = "BOT_CAR_SPEED"

MISC_MODEL_NAME_OLD_LOGS = "Successfully downloaded model metadata from model-metadata/"
MISC_MODEL_NAME_NEW_LOGS_A = "Successfully downloaded model metadata"
MISC_MODEL_NAME_NEW_LOGS_B = "[s3] Successfully downloaded model metadata"

CONTINUOUS_ACTION_SPACE_START = "Sensor list ["
CONTINUOUS_ACTION_SPACE_CONTAINS = "action_space_type continuous"

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


def _set_hyper_string_value(line_of_text: str, hyper_name: str, meta_field: MetaField):
    if _contains_hyper(line_of_text, hyper_name):
        chop_chars = len(hyper_name) + 6
        meta_field.set(line_of_text[chop_chars:].split('"')[1].upper().replace(" ", "_"))


# Parse the high level training settings

def _set_parameter_string_value(parameters: dict, parameter_name: str, meta_field: MetaField, replacements: dict = None):
    if parameter_name in parameters:
        value = parameters[parameter_name]
        if replacements is not None and value in replacements:
            meta_field.set(replacements[value])
        else:
            meta_field.set(value)


def _set_parameter_integer_value(parameters: dict, parameter_name: str, meta_field: MetaField):
    if parameter_name in parameters:
        meta_field.set(int(parameters[parameter_name]))


def _set_parameter_float_value(parameters: dict, parameter_name: str, meta_field: MetaField):
    if parameter_name in parameters:
        meta_field.set(float(parameters[parameter_name]))


def _set_parameter_boolean_value(parameters: dict, parameter_name: str, meta_field: MetaField):
    if parameter_name in parameters:
        meta_field.set(_text_to_bool(parameters[parameter_name]))


def _text_to_bool(text: str) -> bool:
    value = text.upper().replace(" ", "").replace("\n", "")
    assert value in ("TRUE", "FALSE")
    return value == "TRUE"


