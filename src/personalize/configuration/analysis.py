

from src.personalize.reward_functions.prevent_zig_zag import reward_function
NEW_REWARD_FUNCTION = reward_function

DISCOUNT_FACTORS = [0.999, 0.99, 0.97, 0.95, 0.9]
DISCOUNT_FACTOR_MAX_STEPS = 300