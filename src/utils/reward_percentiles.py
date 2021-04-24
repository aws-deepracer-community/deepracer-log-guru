#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.episode.episode import Episode
import numpy as np


class RewardPercentiles:

    def __init__(self, episodes: list[Episode], calculate_new_reward: bool):
        percents = np.arange(100)

        all_rewards = episodes[0].rewards
        for e in episodes[1:]:
            all_rewards += e.rewards
        self._reward_percentiles = np.percentile(np.array(all_rewards), percents)

        all_new_rewards = episodes[0].new_rewards
        if calculate_new_reward:
            for e in episodes[1:]:
                all_new_rewards += e.new_rewards
            self._new_reward_percentiles = np.percentile(np.array(all_new_rewards), percents)
        else:
            self._new_reward_percentiles = None

        all_new_discounted_future_rewards = episodes[0].new_discounted_future_rewards
        if calculate_new_reward:
            for e in episodes[1:]:
                all_new_discounted_future_rewards += e.new_discounted_future_rewards
            self._new_discounted_future_reward_percentiles = np.percentile(np.array(all_new_discounted_future_rewards),
                                                                           percents)
        else:
            self._new_discounted_future_reward_percentiles = None

        self._discounted_future_reward_percentiles = []
        for i in range(len(episodes[0].discounted_future_rewards)):
            all_discounted_future_rewards = episodes[0].discounted_future_rewards[i]
            for e in episodes[1:]:
                all_discounted_future_rewards += e.discounted_future_rewards[i]
            self._discounted_future_reward_percentiles.append(
                np.percentile(np.array(all_discounted_future_rewards), percents))

    def get_reward_percentile(self, reward):
        return np.searchsorted(self._reward_percentiles, reward)

    def get_new_reward_percentile(self, new_reward):
        return np.searchsorted(self._new_reward_percentiles, new_reward)

    def get_new_discounted_future_reward_percentile(self, new_discounted_future_reward):
        return np.searchsorted(self._new_discounted_future_reward_percentiles, new_discounted_future_reward)

    def get_discounted_future_reward_percentile(self, discounted_future_reward, discount_factor_index):
        return np.searchsorted(self._discounted_future_reward_percentiles[discount_factor_index],
                               discounted_future_reward)
