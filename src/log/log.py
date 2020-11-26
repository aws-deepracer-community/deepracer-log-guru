import pickle
import numpy as np
import os

import time

import src.log.parse as parse

from src.episode.episode import Episode
from src.log.log_meta import LogMeta
from src.ui.please_wait import PleaseWait

META_FILE_SUFFIX = ".meta"
LOG_FILE_SUFFIX = ".log"



class EvaluationPhase:
    def __init__(self, rewards, progresses):
        assert len(rewards) == len(progresses)

        self.length = len(rewards)
        self.rewards = np.array(rewards)
        self.progresses = np.array(progresses)


class Log:
    def __init__(self):
        self.log_meta = LogMeta()
        self.episodes = []
        self.evaluation_phases = []
        self.log_file_name = ""
        self.meta_file_name = ""

    def load_meta(self, meta_file_name):
        self.meta_file_name = meta_file_name
        with open(meta_file_name, 'rb') as file:
            self.log_meta = pickle.load(file)

        # TODO assert log_info is the of the correct LogInfo type

    def load_all(self, meta_file_name, please_wait :PleaseWait):
        please_wait.start("Loading")
        self.load_meta(meta_file_name)
        self.log_file_name = meta_file_name[:-len(META_FILE_SUFFIX)]
        self.parse_episode_events(please_wait, 0, 85, 95)
        self.divide_episodes_into_quarters(please_wait, 95, 100)
        please_wait.stop(0.2)

    def parse(self, log_file_name, please_wait :PleaseWait, min_progress_percent, max_progress_percent):
        self.log_file_name = log_file_name
        self.meta_file_name = log_file_name + META_FILE_SUFFIX

        self.parse_intro_events()
        self.parse_episode_events(
            please_wait,
            min_progress_percent,
            min_progress_percent + 0.9 * (max_progress_percent - min_progress_percent),
            max_progress_percent)

        self.analyze_episode_details()

    def save(self):
        with open(self.meta_file_name, "wb") as meta_file:
            pickle.dump(self.log_meta, meta_file)

    def parse_intro_events(self):
        with open(self.log_file_name, "r") as file:
            for str in file:
                if str.startswith(parse.EPISODE_STARTS_WITH):
                    break
                else:
                    parse.parse_intro_event(str, self.log_meta)

    def parse_episode_events(self, please_wait :PleaseWait, min_progress_percent, mid_progress_percent, max_progress_percent):
        episode_events = []
        episode_object_locations = []
        saved_events = []
        intro = True
        saved_debug = ""
        evaluation_rewards = []
        saved_object_locations = None

        file_size = os.path.getsize(self.log_file_name)
        file_amount_read = 0

        with open(self.log_file_name, "r") as file:
            for str in file:
                if str.startswith(parse.EPISODE_STARTS_WITH):
                    intro = False
                    parse.parse_episode_event(str, episode_events, episode_object_locations, saved_events, saved_debug, saved_object_locations)
                    saved_debug = ""
                    saved_object_locations = None
                elif parse.EPISODE_STARTS_WITH in str and parse.SENT_SIGTERM in str:
                    end_of_str = str[str.find(parse.EPISODE_STARTS_WITH):]
                    intro = False
                    parse.parse_episode_event(end_of_str, episode_events, episode_object_locations, saved_events, saved_debug, saved_object_locations)
                    saved_debug = ""
                    saved_object_locations = None
                elif not intro:
                    evaluation_reward = parse.parse_evaluation_reward_info(str)
                    evaluation_count, evaluation_progresses = parse.parse_evaluation_progress_info(str)
                    object_locations = parse.parse_object_locations(str)

                    if evaluation_reward != None:
                        evaluation_rewards.append(evaluation_reward)
                    elif evaluation_count and evaluation_progresses:
                        assert evaluation_count == len(evaluation_rewards)
                        self.evaluation_phases.append(EvaluationPhase(evaluation_rewards, evaluation_progresses))
                        evaluation_rewards = []
                    elif str.startswith(parse.STILL_EVALUATING):
                        saved_debug = ""    # Make sure debug info doesn't include any output from evaluation phase
                        saved_object_locations = None
                    elif object_locations:
                        saved_object_locations = object_locations
                    else:
                        saved_debug += str
                else:
                    object_locations = parse.parse_object_locations(str)
                    if object_locations:
                        saved_object_locations = object_locations
                        intro = False



                file_amount_read += len(str)
                percent_read = file_amount_read / file_size * 100
                scaled_percent_read = (mid_progress_percent - min_progress_percent) / 100 * percent_read
                please_wait.set_progress(min_progress_percent + scaled_percent_read)

        assert not saved_events

        total_episodes = len(episode_events)

        for i, e in enumerate(episode_events[:-1]):
            iteration = i // self.log_meta.hyper.episodes_between_training
            self.episodes.append(Episode(i, iteration, e, episode_object_locations[i]))
            please_wait.set_progress(
                mid_progress_percent + i / total_episodes * (max_progress_percent - mid_progress_percent))

    def analyze_episode_details(self):

        self.log_meta.episode_stats.episode_count = len(self.episodes)

        total_success_steps = 0
        total_success_distance = 0.0
        total_percent_complete = 0.0

        reward_list = []

        for e in self.episodes:
            total_percent_complete += e.percent_complete
            reward_list.append(e.total_reward)

            if e.lap_complete:
                self.log_meta.episode_stats.success_count += 1

                total_success_steps += e.step_count
                total_success_distance += e.distance_travelled

                if self.log_meta.episode_stats.best_steps == 0 or e.step_count < self.log_meta.episode_stats.best_steps:
                    self.log_meta.episode_stats.best_steps = e.step_count

                if self.log_meta.episode_stats.worst_steps < e.step_count:
                    self.log_meta.episode_stats.worst_steps = e.step_count

                if self.log_meta.episode_stats.best_distance == 0.0 or e.distance_travelled < self.log_meta.episode_stats.best_distance:
                    self.log_meta.episode_stats.best_distance = e.distance_travelled

                if self.log_meta.episode_stats.worst_distance < e.distance_travelled:
                    self.log_meta.episode_stats.worst_distance = e.distance_travelled

        if reward_list:
            r = np.array(reward_list)
            self.log_meta.episode_stats.best_reward = np.max(r)
            self.log_meta.episode_stats.average_reward = np.mean(r)
            self.log_meta.episode_stats.worst_reward = np.min(r)

        if self.log_meta.episode_stats.success_count > 0:
            self.log_meta.episode_stats.average_steps = int(
                round(total_success_steps / self.log_meta.episode_stats.success_count))
            self.log_meta.episode_stats.average_distance = total_success_distance / self.log_meta.episode_stats.success_count

        if self.log_meta.episode_stats.episode_count > 0:
            self.log_meta.episode_stats.average_percent_complete = total_percent_complete / self.log_meta.episode_stats.episode_count

    def divide_episodes_into_quarters(self, please_wait :PleaseWait, min_progress_percent, max_progress_percent):
        total_iterations = self.episodes[-1].iteration + 1

        if total_iterations < 4:
            self.divide_episodes_into_quarters_ignoring_iteration(please_wait, min_progress_percent, max_progress_percent)
        else:
            for e in self.episodes:
                please_wait.set_progress(min_progress_percent + e.iteration / total_iterations * (max_progress_percent - min_progress_percent))

                if e.iteration <= round(total_iterations * 0.25) - 1:
                    e.set_quarter(1)
                elif e.iteration <= round(total_iterations * 0.5) - 1:
                    e.set_quarter(2)
                elif e.iteration <= round(total_iterations * 0.75) - 1:
                    e.set_quarter(3)
                else:
                    e.set_quarter(4)

    def divide_episodes_into_quarters_ignoring_iteration(self, please_wait :PleaseWait, min_progress_percent, max_progress_percent):
        e: Episode = None

        total_episodes = len(self.episodes)

        for e in self.episodes:
            please_wait.set_progress(
                min_progress_percent + e.id / total_episodes * (max_progress_percent - min_progress_percent))

            if e.id <= round(total_episodes * 0.25) - 1:
                e.set_quarter(1)
            elif e.id <= round(total_episodes * 0.5) - 1:
                e.set_quarter(2)
            elif e.id <= round(total_episodes * 0.75) - 1:
                e.set_quarter(3)
            else:
                e.set_quarter(4)


def refresh_all_log_meta(please_wait):
    please_wait.start("Refreshing")
    log_files = []
    for f in os.listdir(os.curdir):
        if f.endswith(LOG_FILE_SUFFIX):
            log_files.append(f)
    import_new_logs(log_files, please_wait)


def import_new_logs(log_files, please_wait):
    please_wait.start("Importing")
    total_count = len(log_files)
    for i, f in enumerate(log_files):
        log = Log()
        log.parse(f, please_wait, i / total_count * 100, (i+1) / total_count * 100)
        log.save()

def get_model_info_for_open_model_dialog(track):
    model_names = []
    model_files = {}
    for f in os.listdir(os.curdir):
        if f.endswith(META_FILE_SUFFIX):
            log = Log()
            log.load_meta(f)

            if log.log_meta.world_name == track.world_name:
                model_name = log.log_meta.model_name
                model_names.append(model_name)
                model_files[model_name] = f
    return model_files, model_names

def get_possible_new_model_log_files():
    new_log_files = []

    all_files = os.listdir(os.curdir)
    for f in all_files:
        if f.endswith(LOG_FILE_SUFFIX):
            expected_meta = f + META_FILE_SUFFIX
            if not expected_meta in all_files:
                new_log_files.append(f)

    return new_log_files
