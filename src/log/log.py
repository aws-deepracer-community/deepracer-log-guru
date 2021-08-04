#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import numpy as np
import os
import json

import src.log.parse as parse

from src.log.evaluation_phase import EvaluationPhase
from src.log.log_meta import LogMeta

from src.episode.episode import Episode
from src.personalize.configuration.analysis import TIME_BEFORE_FIRST_STEP
from src.ui.please_wait import PleaseWait
from src.tracks.track import Track

from src.utils.discount_factors import discount_factors

META_FILE_SUFFIX = ".meta.json"
LOG_FILE_SUFFIX = ".log"


class Log:
    #
    # PUBLIC interface
    #

    def load_meta(self, meta_file_name: str):
        self._meta_file_name = meta_file_name
        with open(os.path.join(self._log_directory, meta_file_name), 'rb') as file:
            received_json = json.load(file)
            self._log_meta.set_from_json(received_json)

    def load_all(self, meta_file_name, please_wait: PleaseWait, track: Track,
                 calculate_new_reward=False, calculate_alternate_discount_factors=False):
        please_wait.start("Loading")
        self.load_meta(meta_file_name)
        self._log_file_name = meta_file_name[:-len(META_FILE_SUFFIX)]
        discount_factors.reset_for_log(self._log_meta.hyper.discount_factor)
        please_wait.set_progress(2)
        self._parse_episode_events(please_wait, self._log_meta.action_space.is_continuous(),
                                   2, 50, 95, True, track,
                                   calculate_new_reward, calculate_alternate_discount_factors)
        self._divide_episodes_into_quarters(please_wait, 95, 100)
        please_wait.set_progress(100)
        please_wait.stop(0.3)

    def parse(self, log_file_name, please_wait: PleaseWait, min_progress_percent: float, max_progress_percent: float):
        self._log_file_name = log_file_name
        self._meta_file_name = log_file_name + META_FILE_SUFFIX

        self._parse_intro_events()
        self._parse_episode_events(
            please_wait,
            self._log_meta.action_space.is_continuous(),
            min_progress_percent,
            min_progress_percent + 0.9 * (max_progress_percent - min_progress_percent),
            max_progress_percent, False)

        self._analyze_episode_details()

    def save(self):
        with open(os.path.join(self._log_directory, self._meta_file_name), "w+") as meta_file:
            log_json = self._log_meta.get_as_json()
            json.dump(log_json, meta_file, indent=2)

    def get_meta_file_name(self):
        return self._meta_file_name

    def get_log_file_name(self):
        return self._log_file_name

    def get_evaluation_phases(self):
        return self._evaluation_phases

    def get_log_meta(self):
        return self._log_meta

    def get_episodes(self):
        return self._episodes

    #
    # PRIVATE implementation
    #

    def __init__(self, log_directory: str):
        self._log_meta = LogMeta()
        self._episodes = []
        self._evaluation_phases = []
        self._log_file_name = ""
        self._meta_file_name = ""
        self._log_directory = log_directory

    def _parse_intro_events(self):
        with open(os.path.join(self._log_directory, self._log_file_name), "r") as file:
            for line_of_text in file:
                if line_of_text.startswith(parse.EPISODE_STARTS_WITH):
                    break
                else:
                    parse.parse_intro_event(line_of_text, self._log_meta)

    def _parse_episode_events(self, please_wait: PleaseWait, is_continuous_action_space: bool,
                              min_progress_percent: float, mid_progress_percent: float, max_progress_percent: float,
                              do_full_analysis: bool, track: Track = None,
                              calculate_new_reward=False, calculate_alternate_discount_factors=False):
        episode_events = []
        episode_iterations = []
        episode_object_locations = []
        saved_events = []
        intro = True
        saved_debug = ""
        evaluation_rewards = []
        saved_object_locations = None
        iteration_id = 0

        file_size = os.path.getsize(os.path.join(self._log_directory, self._log_file_name))
        file_amount_read = 0

        with open(os.path.join(self._log_directory, self._log_file_name), "r") as file:
            for line_of_text in file:
                if line_of_text.startswith(parse.EPISODE_STARTS_WITH):
                    intro = False
                    parse.parse_episode_event(line_of_text, episode_events, episode_object_locations,
                                              saved_events, saved_debug, saved_object_locations,
                                              is_continuous_action_space)
                    saved_debug = ""
                    saved_object_locations = None
                elif parse.EPISODE_STARTS_WITH in line_of_text and (len(line_of_text) > 1000 or parse.SENT_SIGTERM in line_of_text):
                    end_of_str = line_of_text[line_of_text.find(parse.EPISODE_STARTS_WITH):]
                    intro = False
                    parse.parse_episode_event(end_of_str, episode_events, episode_object_locations,
                                              saved_events, saved_debug, saved_object_locations,
                                              is_continuous_action_space)
                    saved_debug = ""
                    saved_object_locations = None
                elif not intro:
                    evaluation_reward = parse.parse_evaluation_reward_info(line_of_text)
                    evaluation_progresses = parse.parse_evaluation_progress_info(line_of_text)
                    object_locations = parse.parse_object_locations(line_of_text)

                    if evaluation_reward is not None:
                        evaluation_rewards.append(evaluation_reward)
                    elif evaluation_progresses is not None:
                        # Rare case in which final reward is missing from log file for some reason
                        if len(evaluation_progresses) == len(evaluation_rewards) + 1:
                            evaluation_progresses = evaluation_progresses[:-1]
                        assert len(evaluation_progresses) == len(evaluation_rewards)
                        self._evaluation_phases.append(EvaluationPhase(evaluation_rewards, evaluation_progresses))
                        evaluation_rewards = []
                        while len(episode_events) - 1 > len(episode_iterations):  # Minus 1 avoids counting next (empty) one
                            episode_iterations.append(iteration_id)
                        iteration_id += 1
                    elif line_of_text.startswith(parse.STILL_EVALUATING):
                        saved_debug = ""  # Make sure debug info doesn't include any output from evaluation phase
                        saved_object_locations = None
                    elif object_locations:
                        saved_object_locations = object_locations
                    else:
                        saved_debug += line_of_text
                else:
                    object_locations = parse.parse_object_locations(line_of_text)
                    if object_locations:
                        saved_object_locations = object_locations
                        intro = False

                file_amount_read += len(line_of_text)
                percent_read = file_amount_read / file_size * 100
                scaled_percent_read = (mid_progress_percent - min_progress_percent) / 100 * percent_read
                please_wait.set_progress(min_progress_percent + scaled_percent_read)

        if saved_events:
            episode_events = episode_events[:-1]

        last_episode = episode_events[-1]
        if len(last_episode) == 0 or not last_episode[-1].job_completed:
            episode_events = episode_events[:-1]

        total_episodes = len(episode_events)

        while len(episode_events) > len(episode_iterations):
            episode_iterations.append(iteration_id)

        for i, e in enumerate(episode_events):
            self._episodes.append(Episode(i, episode_iterations[i], e, episode_object_locations[i],
                                          self._log_meta.action_space, do_full_analysis, track,
                                          calculate_new_reward, calculate_alternate_discount_factors))
            please_wait.set_progress(
                mid_progress_percent + i / total_episodes * (max_progress_percent - mid_progress_percent))

    def _analyze_episode_details(self):
        self._log_meta.episode_stats.episode_count = len(self._episodes)

        total_success_steps = 0
        total_success_time = 0
        total_success_distance = 0.0
        total_percent_complete = 0.0

        reward_list = []

        for e in self._episodes:
            total_percent_complete += e.percent_complete
            reward_list.append(e.total_reward)

            if e.lap_complete:
                self._log_meta.episode_stats.success_count += 1

                raw_time_taken = e.time_taken - TIME_BEFORE_FIRST_STEP
                total_success_steps += e.step_count
                total_success_time += raw_time_taken
                total_success_distance += e.distance_travelled

                if self._log_meta.episode_stats.best_steps == 0 or \
                        e.step_count < self._log_meta.episode_stats.best_steps:
                    self._log_meta.episode_stats.best_steps = e.step_count
                    self._log_meta.episode_stats.best_time = raw_time_taken

                if self._log_meta.episode_stats.worst_steps < e.step_count:
                    self._log_meta.episode_stats.worst_steps = e.step_count
                    self._log_meta.episode_stats.worst_time = raw_time_taken

                if self._log_meta.episode_stats.best_distance == 0.0 or \
                        e.distance_travelled < self._log_meta.episode_stats.best_distance:
                    self._log_meta.episode_stats.best_distance = e.distance_travelled

                if self._log_meta.episode_stats.worst_distance < e.distance_travelled:
                    self._log_meta.episode_stats.worst_distance = e.distance_travelled

        if reward_list:
            r = np.array(reward_list)
            self._log_meta.episode_stats.best_reward = np.max(r)
            self._log_meta.episode_stats.average_reward = np.mean(r)
            self._log_meta.episode_stats.worst_reward = np.min(r)

        if self._log_meta.episode_stats.success_count > 0:
            self._log_meta.episode_stats.average_steps = int(
                round(total_success_steps / self._log_meta.episode_stats.success_count))
            self._log_meta.episode_stats.average_time = total_success_time / self._log_meta.episode_stats.success_count
            self._log_meta.episode_stats.average_distance = \
                total_success_distance / self._log_meta.episode_stats.success_count

        if self._log_meta.episode_stats.episode_count > 0:
            self._log_meta.episode_stats.average_percent_complete = \
                total_percent_complete / self._log_meta.episode_stats.episode_count

        training_start_time = self._episodes[0].events[0].time
        training_end_time = self._episodes[-1].events[-1].time
        self._log_meta.episode_stats.training_minutes = int(round((training_end_time - training_start_time) / 60))

    def _divide_episodes_into_quarters(self, please_wait: PleaseWait,
                                       min_progress_percent: float, max_progress_percent: float):
        total_iterations = self._episodes[-1].iteration + 1

        if total_iterations < 4:
            self._divide_episodes_into_quarters_ignoring_iteration(please_wait,
                                                                   min_progress_percent, max_progress_percent)
        else:
            for e in self._episodes:
                please_wait.set_progress(min_progress_percent +
                                         e.iteration / total_iterations * (max_progress_percent - min_progress_percent))

                if e.iteration <= round(total_iterations * 0.25) - 1:
                    e.set_quarter(1)
                elif e.iteration <= round(total_iterations * 0.5) - 1:
                    e.set_quarter(2)
                elif e.iteration <= round(total_iterations * 0.75) - 1:
                    e.set_quarter(3)
                else:
                    e.set_quarter(4)

    def _divide_episodes_into_quarters_ignoring_iteration(self, please_wait: PleaseWait,
                                                          min_progress_percent: float,
                                                          max_progress_percent: float):
        total_episodes = len(self._episodes)
        e: Episode
        for e in self._episodes:
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
