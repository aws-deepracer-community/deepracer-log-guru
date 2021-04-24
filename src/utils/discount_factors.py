#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import numpy as np

from src.personalize.configuration.analysis import DISCOUNT_FACTORS, DISCOUNT_FACTOR_MAX_STEPS


class DiscountFactors:
    def __init__(self):
        self._multipliers = []
        self._discount_factors = DISCOUNT_FACTORS
        self._max_steps = DISCOUNT_FACTOR_MAX_STEPS

        self._prepare_multipliers()

    def get_discount_factor(self, index: int):
        return self._discount_factors[index]

    def get_number_of_discount_factors(self):
        return len(self._discount_factors)

    def reset_for_log(self, training_discount_factor):
        if self._discount_factors[0] == training_discount_factor:
            return

        self._discount_factors = [training_discount_factor]
        for df in DISCOUNT_FACTORS:
            if df != training_discount_factor:
                self._discount_factors.append(df)
        self._prepare_multipliers()

    def _prepare_multipliers(self):
        self._multipliers = []
        for df in self._discount_factors:
            assert 0.0 < df <= 1.0
            multiplier = []
            factor = 1.0
            for i in range(self._max_steps):
                multiplier.append(factor)
                factor *= df
            self._multipliers.append(np.array(multiplier))

    def get_discounted_future_rewards(self, rewards: np.ndarray, multi_discount_factor: bool, force_list: bool):
        look_ahead = min(self._max_steps, len(rewards))
        if multi_discount_factor:
            discounted_future_rewards = []
            for m in self._multipliers:
                discounted_future_rewards.append(np.sum(np.multiply(rewards[:look_ahead], m[:look_ahead])))
            return discounted_future_rewards
        else:
            m = self._multipliers[0]
            value = np.sum(np.multiply(rewards[:look_ahead], m[:look_ahead]))
            if force_list:
                return [value]
            else:
                return value

    def print_for_debug(self):
        for i, m in enumerate(self._multipliers):
            print(self._discount_factors[i], "->", m)

    def get_weights_plot_data(self, index: int, zoom_level: int):
        steps = self._get_steps_for_plot_zoom_level(zoom_level)
        plot_x = np.arange(steps)
        plot_y = self._multipliers[index][:steps]
        return plot_x, plot_y

    def get_time_until_death_plot_data(self, index: int, zoom_level: int, bonus_level: int):
        assert bonus_level >= 1
        steps = self._get_steps_for_plot_zoom_level(zoom_level)
        plot_x = np.arange(steps)
        plot_y = []
        for i in plot_x:
            future_reward = np.sum(self._multipliers[index][:i + 1])
            future_reward += (bonus_level - 1) * self._multipliers[index][i]
            plot_y.append(future_reward)

        return plot_x, plot_y

    def _get_steps_for_plot_zoom_level(self, zoom_level: int):
        if zoom_level <= 0:
            return self._max_steps

        steps = self._max_steps
        for i in range(zoom_level):
            if steps > 20:
                steps /= 2
            elif steps > 4:
                steps -= 2

        return int(steps + 1)


discount_factors = DiscountFactors()


# discount_factors.print_for_debug()
#
# print("------------")
# print(discount_factors.get_discounted_future_rewards(np.array([1, 2, 3])))
# print(discount_factors.get_discounted_future_rewards(np.array([3, 2, 1])))
