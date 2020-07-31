import pickle
import numpy as np
import os


import src.log.parse as parse

from src.episode.episode import Episode
from src.log.log_meta import LogMeta


META_FILE_SUFFIX = ".meta"
LOG_FILE_SUFFIX = ".log"


class Log:
    def __init__(self):
        self.log_meta = LogMeta()
        self.episodes = []
        self.log_file_name = ""
        self.meta_file_name = ""

    def load_meta(self, meta_file_name):
        self.meta_file_name = meta_file_name
        with open(meta_file_name, 'rb') as file:
            self.log_meta = pickle.load(file)

        # TODO assert log_info is the of the correct LogInfo type

    def load_all(self, meta_file_name):
        self.load_meta(meta_file_name)
        self.log_file_name = meta_file_name[:-len(META_FILE_SUFFIX)]
        self.parse_episode_events()

    def parse(self, log_file_name):
        self.log_file_name = log_file_name
        self.meta_file_name = log_file_name + META_FILE_SUFFIX

        self.parse_intro_events()
        self.parse_episode_events()

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

    def parse_episode_events(self):
        episode_events = []
        saved_events = []
        intro = True
        saved_debug = ""
        evaluation_rewards = []

        with open(self.log_file_name, "r") as file:
            for str in file:
                if str.startswith(parse.EPISODE_STARTS_WITH):
                    intro = False
                    parse.parse_episode_event(str, episode_events, saved_events, saved_debug)
                    saved_debug = ""
                elif not intro:
                    evaluation_reward = parse.parse_evaluation_reward_info(str)
                    evaluation_count, evaluation_progresses = parse.parse_evaluation_progress_info(str)

                    if evaluation_reward:
                        evaluation_rewards.append(evaluation_reward)
                    elif evaluation_count and evaluation_progresses:
                        assert evaluation_count == len(evaluation_rewards)
                        # for i in range(0, evaluation_count):
                        #    print(evaluation_rewards[i], evaluation_progresses[i])
                        # print("-------------------------")
                        evaluation_rewards = []
                    else:
                        saved_debug += str

        assert not saved_events

        for i, e in enumerate(episode_events[:-1]):
            iteration = i // self.log_meta.hyper.episodes_between_training
            self.episodes.append(Episode(i, iteration, e))


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

def refresh_all_log_meta():
    for f in os.listdir(os.curdir):
        if f.endswith(LOG_FILE_SUFFIX):
            log = Log()
            log.parse(f)
            log.save()

def import_new_logs(log_files):
    for f in log_files:
        log = Log()
        log.parse(f)
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
