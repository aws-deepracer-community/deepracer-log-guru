import math
import json

from src.event.event_meta import Event
from src.log.log_meta import LogMeta
from src.action_space.action import  Action

EPISODE_STARTS_WITH = "SIM_TRACE_LOG"

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

MISC_MODEL_NAME = "Successfully downloaded model metadata from model-metadata/"
MISC_ACTION_SPACE = "Loaded action space from file: "


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

    if str.startswith(MISC_MODEL_NAME):
        log_meta.model_name = str.split("/")[1]
        # print("FOUND MODEL NAME:", log_meta.model_name)

    if str.startswith(MISC_ACTION_SPACE):
        raw_actions = str[len(MISC_ACTION_SPACE):].replace("'", "\"")

        actions = json.loads(raw_actions)
        for a in actions:
            new_action = Action(a["index"], a["speed"], a["steering_angle"])
            log_meta.action_space[a["index"]] = new_action

            #print("DEBUG", new_action.get_readable_with_index())


def parse_episode_event(str, episodes, saved_events, saved_debug):
    assert len(saved_events) < 20

    if not episodes:
        episodes.append([])

    str = str.split("\n", 1)[0]

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
     status) = str[14:].split(",")

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

    event_meta.debug_log = saved_debug

    if event_meta.step > len(episodes[-1]) + 1 or event_meta.episode > len(episodes) - 1:
        saved_events.append(event_meta)
        return

    assert event_meta.episode == len(episodes) - 1
    assert event_meta.step == len(episodes[-1]) + 1

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