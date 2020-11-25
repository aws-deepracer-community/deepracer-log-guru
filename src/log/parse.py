import math
import json

from src.event.event_meta import Event
from src.log.log_meta import LogMeta
from src.action_space.action import  Action

EPISODE_STARTS_WITH = "SIM_TRACE_LOG"
SENT_SIGTERM = "Sent SIGTERM"

HYPER_BATCH_SIZE = "batch_size"
HYPER_ENTROPY = "beta_entropy"
HYPER_DISCOUNT_FACTOR = "discount_factor"
HYPER_LOSS_TYPE = "loss_type"
HYPER_LEARNING_RATE = "lr"
HYPER_EPISODES_BETWEEN_TRAINING = "num_episodes_between_training"
HYPER_EPOCHS = "num_epochs"

PARAM_WORLD_NAME = "WORLD_NAME"
PARAM_RACE_TYPE = "RACE_TYPE"
PARAM_JOB_TYPE = "JOB_TYPE"

MISC_MODEL_NAME_OLD_LOGS = "Successfully downloaded model metadata from model-metadata/"
MISC_MODEL_NAME_NEW_LOGS_A = "Successfully downloaded model metadata"
MISC_MODEL_NAME_NEW_LOGS_B = "[s3] Successfully downloaded model metadata"

# For handling cloud, here are the example of cloud and non-cloud
#   cloud       [s3] Successfully downloaded yaml file from s3 key DMH-Champ-Round1-OA-B-3/training-params.yaml
#   non-cloud   [s3] Successfully downloaded yaml file from s3 key data-56b52007-8142-46cd-a9cc-370feb620f0c/models/Champ-Obj-Avoidance-03/sagemaker-robomaker-artifacts/training_params_634ecc9a-b12d-4350-99ac-3320f88e9fbe.yaml to local ./custom_files/training_params_634ecc9a-b12d-4350-99ac-3320f88e9fbe.yaml.

MISC_MODEL_NAME_CLOUD_LOGS = "[s3] Successfully downloaded yaml file from s3 key"
CLOUD_TRAINING_YAML_FILENAME = "training-params.yaml"


MISC_ACTION_SPACE_A = "Loaded action space from file: "
MISC_ACTION_SPACE_B = "Action space from file: "

EVALUATION_REWARD_START = "## agent: Finished evaluation phase. Success rate = 0.0, Avg Total Reward = "
EVALUATION_PROGRESSES_START = "Number of evaluations: "

def parse_intro_event(str, log_meta :LogMeta):
    if contains_hyper(str, HYPER_BATCH_SIZE):
        log_meta.hyper.batch_size = get_hyper_integer_value(str, HYPER_BATCH_SIZE)

    if contains_hyper(str, HYPER_ENTROPY):
        log_meta.hyper.entropy = get_hyper_float_value(str, HYPER_ENTROPY)

    if contains_hyper(str, HYPER_DISCOUNT_FACTOR):
        log_meta.hyper.discount_factor = get_hyper_float_value(str, HYPER_DISCOUNT_FACTOR)

    if contains_hyper(str, HYPER_LOSS_TYPE):
        log_meta.hyper.loss_type = get_hyper_string_value(str, HYPER_LOSS_TYPE)

    if contains_hyper(str, HYPER_LEARNING_RATE):
        log_meta.hyper.learning_rate = get_hyper_float_value(str, HYPER_LEARNING_RATE)

    if contains_hyper(str, HYPER_EPISODES_BETWEEN_TRAINING):
        log_meta.hyper.episodes_between_training = get_hyper_integer_value(str, HYPER_EPISODES_BETWEEN_TRAINING)

    if contains_hyper(str, HYPER_EPOCHS):
        log_meta.hyper.epochs = get_hyper_integer_value(str, HYPER_EPOCHS)

    if contains_parameter(str, PARAM_WORLD_NAME):
        log_meta.world_name = get_parameter_string_value(str, PARAM_WORLD_NAME)

    if contains_parameter(str, PARAM_RACE_TYPE):
        log_meta.race_type = get_parameter_string_value(str, PARAM_RACE_TYPE)

    if contains_parameter(str, PARAM_JOB_TYPE):
        log_meta.job_type = get_parameter_string_value(str, PARAM_JOB_TYPE)

    if log_meta.model_name == "":
        if str.startswith(MISC_MODEL_NAME_OLD_LOGS):
            log_meta.model_name = str.split("/")[1]

        if str.startswith(MISC_MODEL_NAME_NEW_LOGS_A) and not str.startswith(MISC_MODEL_NAME_OLD_LOGS):
            log_meta.model_name = str.split("/")[2]

        if str.startswith(MISC_MODEL_NAME_NEW_LOGS_B):
            log_meta.model_name = str.split("/")[2]

        if str.startswith(MISC_MODEL_NAME_CLOUD_LOGS):
            split_parts = str[len(MISC_MODEL_NAME_CLOUD_LOGS):].split("/")
            if split_parts[1].startswith(CLOUD_TRAINING_YAML_FILENAME):
                log_meta.model_name = split_parts[0]

    if str.startswith(MISC_ACTION_SPACE_A):
        parse_actions(str, log_meta, MISC_ACTION_SPACE_A)

    if str.startswith(MISC_ACTION_SPACE_B):
        parse_actions(str, log_meta, MISC_ACTION_SPACE_B)


def parse_actions(str, log_meta :LogMeta, starts_with):
    raw_actions = str[len(starts_with):].replace("'", "\"")

    actions = json.loads(raw_actions)
    for index, a in enumerate(actions):
        if "index" in a:
            assert a["index"] == index
        new_action = Action(index, a["speed"], a["steering_angle"])
        log_meta.action_space[index] = new_action


def parse_episode_event(input, episodes, saved_events, saved_debug):

    if len(saved_events) > 15:
        print(input)

    assert len(saved_events) < 20

    if not episodes:
        episodes.append([])

    input = input.split("\n", 1)[0]

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
     status) = input[14:].split(",")

    event_meta = Event()

    event_meta.episode = int(episode)
    event_meta.step = int(step)
    event_meta.x = float(x)
    event_meta.y = float(y)
    event_meta.heading = float(heading)
    event_meta.steering_angle = float(steering_angle)
    event_meta.speed = float(speed)
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

    if event_meta.step > len(episodes[-1]) + 1 or event_meta.episode > len(episodes) - 1:
        saved_events.append(event_meta)
        return

    assert event_meta.episode == len(episodes) - 1

    if event_meta.step != len(episodes[-1]) + 1:
        print("WARNING - something wrong near step " + str(event_meta.step) + " of episode " + str(len(episodes) - 1))

    episodes[-1].append(event_meta)
    if event_meta.job_completed:
        episodes.append([])

    added = True
    while added:
        added = False
        for s in saved_events:
            if s.step == len(episodes[-1]) + 1 and s.episode == len(episodes) - 1:
                episodes[-1].append(s)
                saved_events.remove(s)
                added = True
                if s.job_completed:
                    episodes.append([])
                break

def parse_evaluation_reward_info(str):
    if str.startswith(EVALUATION_REWARD_START):
        return float(str[len(EVALUATION_REWARD_START):])
    else:
        return None

def parse_evaluation_progress_info(str):
    if str.startswith(EVALUATION_PROGRESSES_START):
        info = str[len(EVALUATION_PROGRESSES_START):]
        count = int(info.split(" ")[0])

        progresses_as_strings = info[:-2].split("[")[1].split(",")
        progresses = []
        for p in progresses_as_strings:
            progresses.append(float(p))

        assert count == len(progresses)

        return count, progresses
    else:
        return None, None




# Parse hyper parameters

def contains_hyper(str, hyper_name):
    return str.startswith('  "' + hyper_name + '": ')

def get_hyper_integer_value(str, hyper_name):
    chop_chars = len(hyper_name) + 6

    return int(str[chop_chars:].split(",")[0])

def get_hyper_float_value(str, hyper_name):
    chop_chars = len(hyper_name) + 6

    return float(str[chop_chars:].split(",")[0])

def get_hyper_string_value(str, hyper_name):
    chop_chars = len(hyper_name) + 6
    return str[chop_chars:].split('"')[1]


# Parse the high level training settings

def contains_parameter(str, parameter_name):
    return str.startswith(" * /" + parameter_name + ": ")

def get_parameter_string_value(str, parameter_name):
    chop_chars = len(parameter_name) + 6
    return str[chop_chars:].split("\n")[0]

