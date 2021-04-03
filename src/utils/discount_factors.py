import numpy as np

from src.configuration.personal_configuration import DISCOUNT_FACTORS, DISCOUNT_FACTOR_MAX_STEPS


class DiscountFactors:
    def __init__(self):
        self._multipliers = []
        self._discount_factors = DISCOUNT_FACTORS
        self._max_steps = DISCOUNT_FACTOR_MAX_STEPS

        self._prepare_multipliers()

        self._calls_since_gc = 0

    def _prepare_multipliers(self):
        for df in self._discount_factors:
            assert 0.0 < df <= 1.0
            multiplier = []
            factor = 1.0
            for i in range(self._max_steps):
                multiplier.append(factor)
                factor *= df
            self._multipliers.append(np.array(multiplier))

    def get_discounted_future_rewards(self, rewards: np.ndarray):
        discounted_future_rewards = []
        look_ahead = min(self._max_steps, len(rewards))
        for m in self._multipliers:
            discounted_future_rewards.append(np.sum(np.multiply(rewards[:look_ahead], m[:look_ahead])))
        return discounted_future_rewards

    def print_for_debug(self):
        for i, m in enumerate(self._multipliers):
            print(self._discount_factors[i], "->", m)


discount_factors = DiscountFactors()


# discount_factors.print_for_debug()
#
# print("------------")
# print(discount_factors.get_discounted_future_rewards(np.array([1, 2, 3])))
# print(discount_factors.get_discounted_future_rewards(np.array([3, 2, 1])))
