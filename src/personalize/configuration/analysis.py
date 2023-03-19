#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.personalize.reward_functions.follow_centre_line import reward_function

NEW_REWARD_FUNCTION = reward_function

DISCOUNT_FACTORS = [0.999, 0.99, 0.97, 0.95, 0.9]
DISCOUNT_FACTOR_MAX_STEPS = 300

TIME_BEFORE_FIRST_STEP = 0.2
