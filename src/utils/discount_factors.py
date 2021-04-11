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

    def get_discounted_future_rewards(self, rewards: np.ndarray, multi_discount_factor: bool):
        look_ahead = min(self._max_steps, len(rewards))
        if multi_discount_factor:
            discounted_future_rewards = []
            for m in self._multipliers:
                discounted_future_rewards.append(np.sum(np.multiply(rewards[:look_ahead], m[:look_ahead])))
            return discounted_future_rewards
        else:
            m = self._multipliers[0]
            return np.sum(np.multiply(rewards[:look_ahead], m[:look_ahead]))

    def print_for_debug(self):
        for i, m in enumerate(self._multipliers):
            print(self._discount_factors[i], "->", m)

    def get_weights_plot_data(self, index: int):
        plot_x = np.arange(self._max_steps)
        plot_y = self._multipliers[index]
        return plot_x, plot_y

discount_factors = DiscountFactors()


# discount_factors.print_for_debug()
#
# print("------------")
# print(discount_factors.get_discounted_future_rewards(np.array([1, 2, 3])))
# print(discount_factors.get_discounted_future_rewards(np.array([3, 2, 1])))
