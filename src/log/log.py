#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import re

import numpy as np
import os
import json
import tarfile
from typing import Union

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
CONSOLE_LOG_SUFFIX = ".gz"

AWS_UID_REG_EX = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z', re.I)
TRAINING_FILE_REG_EXP = re.compile("-training_job_........*_logs.*")


# Bit of fudge, there's a funny typing behaviour in Python, basically other files like log_utils.py won't match
# Enum properly if they call LogMeta() directly, but work fine if they call this wrapper

def make_new_log_meta():
    return LogMeta()


class Log:
    #
    # PUBLIC interface
    #

    def load_meta(self, meta_file_name: str):
        self._meta_file_name = meta_file_name
        with open(os.path.join(self._log_directory, meta_file_name), 'rb') as file:
            received_json = json.load(file)
            self._log_meta.set_from_json(received_json)

    def load_all(self, meta_file_names: Union[str, list], please_wait: PleaseWait, track: Track,
                 calculate_new_reward=False, calculate_alternate_discount_factors=False):
        please_wait.start("Loading")

        if isinstance(meta_file_names, list):
            multi_evaluation_phases = []
            multi_log_meta = []
            progress_start = 0
            progress_per_log = 95 / len(meta_file_names)
            episodes_by_iteration = {}
            for meta_file in meta_file_names:
                self._load_all_single_episode(meta_file, please_wait, track, calculate_new_reward,
                                              calculate_alternate_discount_factors, progress_start, progress_start + progress_per_log)
                multi_evaluation_phases.append(self._evaluation_phases)
                multi_log_meta.append(self._log_meta)
                for e in self._episodes:
                    i = e.iteration
                    if i in episodes_by_iteration:
                        episodes_by_iteration[i].append(e)
                    else:
                        episodes_by_iteration[i] = [e]
                self._evaluation_phases = []
                self._episodes = []
                self._log_meta = LogMeta()
                progress_start += progress_per_log
            iteration_ids = list(episodes_by_iteration)
            iteration_ids.sort()
            for i in iteration_ids:
                self._episodes += episodes_by_iteration[i]
            for new_id, e in enumerate(self._episodes):
                e.id = new_id
            for e in multi_evaluation_phases:
                if len(e) > 0:
                    assert(len(self._evaluation_phases)) == 0
                    self._evaluation_phases = e
            self._log_meta.merge_from_multi_logs(multi_log_meta)
        else:
            self._load_all_single_episode(meta_file_names, please_wait, track, calculate_new_reward,
                                          calculate_alternate_discount_factors, 0, 95)

        self._divide_episodes_into_quarters(please_wait, 95, 100)
        please_wait.set_progress(100)
        please_wait.stop(0.3)

    def _load_all_single_episode(self, meta_file_name: str, please_wait: PleaseWait, track: Track,
                                 calculate_new_reward, calculate_alternate_discount_factors, progress_start, progress_finish):
        self.load_meta(meta_file_name)
        self._log_file_name = meta_file_name[:-len(META_FILE_SUFFIX)]
        discount_factors.reset_for_log(self._log_meta.discount_factor.get())

        if track is not None:
            assert track.has_world_name(self._log_meta.track_name.get())

        progress_middle = (progress_finish - progress_start) / 2 + progress_start

        if self._log_file_name.endswith(CONSOLE_LOG_SUFFIX):
            with tarfile.open(os.path.join(self._log_directory, self._log_file_name), "r") as tar:
                for member in tar:
                    if "/logs/training" in member.name and member.name.endswith("-robomaker.log"):
                        binary_io = tar.extractfile(member)
                        self._parse_episode_events(
                            binary_io, True,
                            please_wait,
                            progress_start, progress_middle, progress_finish, True, False, member.size, track,
                            calculate_new_reward, calculate_alternate_discount_factors)
        else:
            with open(os.path.join(self._log_directory, self._log_file_name), "r") as file_io:
                self._parse_episode_events(
                    file_io, False,
                    please_wait,
                    progress_start, progress_middle, progress_finish, True, False, 0, track,
                    calculate_new_reward, calculate_alternate_discount_factors)

    def parse(self, log_file_name, please_wait: PleaseWait, min_progress_percent: float, max_progress_percent: float):
        self._log_file_name = log_file_name
        self._meta_file_name = log_file_name + META_FILE_SUFFIX

        # TODO - Extract correct model name
        # TODO - Move this common file handling logic into _parse_episode_events()
        if self._log_file_name.endswith(CONSOLE_LOG_SUFFIX):
            with tarfile.open(os.path.join(self._log_directory, self._log_file_name), "r") as tar:
                for member in tar:
                    if "/logs/training" in member.name and member.name.endswith("-robomaker.log"):
                        binary_io = tar.extractfile(member)
                        self._parse_episode_events(
                            binary_io, True,
                            please_wait,
                            min_progress_percent,
                            min_progress_percent + 0.9 * (max_progress_percent - min_progress_percent),
                            max_progress_percent, False, True, member.size)
        else:
            with open(os.path.join(self._log_directory, self._log_file_name), "r") as file_io:
                self._parse_episode_events(
                    file_io, False,
                    please_wait,
                    min_progress_percent,
                    min_progress_percent + 0.9 * (max_progress_percent - min_progress_percent),
                    max_progress_percent, False, True, 0)

        self._analyze_episode_details()

    def save(self, log_directory_override_for_testing: str = None):
        if log_directory_override_for_testing is not None:
            log_directory = log_directory_override_for_testing
        else:
            log_directory = self._log_directory
        with open(os.path.join(log_directory, self._meta_file_name), "w+") as meta_file:
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

    # def _parse_intro_events(self, file_io, is_binary: bool):
    #     for line_of_text in file_io:
    #         if is_binary:
    #             line_of_text = line_of_text.decode()
    #         if line_of_text.startswith(parse.EPISODE_STARTS_WITH):
    #             break
    #         else:
    #             parse.parse_intro_event(line_of_text, self._log_meta)

    def _parse_episode_events(self, file_io, is_binary: bool, please_wait: PleaseWait,
                              min_progress_percent: float, mid_progress_percent: float, max_progress_percent: float,
                              do_full_analysis: bool, parse_intro: bool, file_size_override: int, track: Track = None,
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

        log_file_path = os.path.join(self._log_directory, self._log_file_name)
        self._log_meta.set_file_os_stats(os.stat(log_file_path))
        self._log_meta.file_name.set(self._log_file_name)

        # TODO - This fudge goes away when all the file handling is re-located into here ...
        if file_size_override > 0:
            file_size = file_size_override
        else:
            file_size = os.path.getsize(log_file_path)

        file_amount_read = 0

        for line_of_text in file_io:
            if is_binary:
                line_of_text = line_of_text.decode()

            if line_of_text.startswith(parse.EPISODE_STARTS_WITH):
                intro = False
                parse.parse_episode_event(line_of_text, episode_events, episode_object_locations,
                                          saved_events, saved_debug, saved_object_locations,
                                          self._log_meta.action_space.is_continuous())
                saved_debug = ""
                saved_object_locations = None
            elif parse.EPISODE_STARTS_WITH in line_of_text and (len(line_of_text) > 1000 or parse.SENT_SIGTERM in line_of_text):
                end_of_str = line_of_text[line_of_text.find(parse.EPISODE_STARTS_WITH):]
                intro = False
                parse.parse_episode_event(end_of_str, episode_events, episode_object_locations,
                                          saved_events, saved_debug, saved_object_locations,
                                          self._log_meta.action_space.is_continuous())
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
                if parse_intro:
                    parse.parse_intro_event(line_of_text, self._log_meta)

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

        # Multi-worker training doesn't have evaluations between each iteration, so calculate iteration breakdown
        if self._log_meta.worker_id.get() > 0 and iteration_id == 0:
            episodes_per_iteration = int(self._log_meta.episodes_per_training_iteration.get() / self._log_meta.workers.get())
            for i in range(0, len(episode_events)):
                episode_iterations.append(int(i / episodes_per_iteration))
        else:
            while len(episode_events) > len(episode_iterations):
                episode_iterations.append(iteration_id)

        for i, e in enumerate(episode_events):
            self._episodes.append(Episode(i, episode_iterations[i], e, episode_object_locations[i],
                                          self._log_meta.action_space, do_full_analysis, track,
                                          calculate_new_reward, calculate_alternate_discount_factors))
            please_wait.set_progress(
                mid_progress_percent + i / total_episodes * (max_progress_percent - mid_progress_percent))

        # Override AWS id with better model name from filename if possible
        if self._log_meta.model_name.get() and AWS_UID_REG_EX.match(self._log_meta.model_name.get()):
            if TRAINING_FILE_REG_EXP.search(self._log_file_name):
                self._log_meta.model_name.set(TRAINING_FILE_REG_EXP.sub("", self._log_file_name))
            else:
                self._log_meta.model_name.set(re.sub("\\..*", "", self._log_file_name))

    def _analyze_episode_details(self):
        total_success_steps = 0
        total_success_time = 0
        total_success_distance = 0.0
        total_percent_complete = 0.0

        reward_list = []

        if len(self._episodes) == 0:
            self._log_meta.iteration_count.set(0)
        else:
            self._log_meta.iteration_count.set(self._episodes[-1].iteration + 1)

        self._log_meta.episode_count.set(len(self._episodes))
        self._log_meta.success_count.set(0)

        self._log_meta.best_steps.set(0)
        self._log_meta.average_steps.set(0)
        self._log_meta.worst_steps.set(0)

        self._log_meta.best_time.set(0.0)
        self._log_meta.average_time.set(0.0)
        self._log_meta.worst_time.set(0.0)

        self._log_meta.best_distance.set(0.0)
        self._log_meta.average_distance.set(0.0)
        self._log_meta.worst_distance.set(0.0)

        for e in self._episodes:
            total_percent_complete += e.percent_complete
            reward_list.append(e.total_reward)

            if e.lap_complete:
                self._log_meta.success_count.set(self._log_meta.success_count.get() + 1)

                raw_time_taken = e.time_taken - TIME_BEFORE_FIRST_STEP
                total_success_steps += e.step_count
                total_success_time += raw_time_taken
                total_success_distance += e.distance_travelled

                if self._log_meta.best_steps.get() == 0 or \
                        e.step_count < self._log_meta.best_steps.get():
                    self._log_meta.best_steps.set(e.step_count)
                    self._log_meta.best_time.set(raw_time_taken)

                if self._log_meta.worst_steps.get() < e.step_count:
                    self._log_meta.worst_steps.set(e.step_count)
                    self._log_meta.worst_time.set(raw_time_taken)

                if self._log_meta.best_distance.get() == 0.0 or \
                        e.distance_travelled < self._log_meta.best_distance.get():
                    self._log_meta.best_distance.set(e.distance_travelled)

                if self._log_meta.worst_distance.get() < e.distance_travelled:
                    self._log_meta.worst_distance.set(e.distance_travelled)

        if reward_list:
            r = np.array(reward_list)
            self._log_meta.best_reward.set(np.max(r))
            self._log_meta.average_reward.set(np.mean(r))
            self._log_meta.worst_reward.set(np.min(r))

        if self._log_meta.success_count.get() > 0:
            self._log_meta.average_steps.set(int(round(total_success_steps / self._log_meta.success_count.get())))
            self._log_meta.average_time.set(total_success_time / self._log_meta.success_count.get())
            self._log_meta.average_distance.set(total_success_distance / self._log_meta.success_count.get())

        if self._log_meta.episode_count.get() > 0:
            self._log_meta.average_percent_complete.set(
                total_percent_complete / self._log_meta.episode_count.get())

    def _divide_episodes_into_quarters(self, please_wait: PleaseWait,
                                       min_progress_percent: float, max_progress_percent: float):
        total_iterations = self._episodes[-1].iteration + 1

        if total_iterations < 8:
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
