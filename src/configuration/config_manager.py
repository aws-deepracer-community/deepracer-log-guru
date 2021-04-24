#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import json
import os

_FILENAME = "DRG_config.json"

_KEY_LOG_DIRECTORY = "log_directory"
_KEY_LAST_OPEN_TRACK = "last_open_track"
_KEY_CALCULATE_ALTERNATE_DISCOUNT_FACTORS = "calculate_alternate_discount_factors"
_KEY_CALCULATE_NEW_REWARD = "calculate_new_reward"


class ConfigManager:
    def __init__(self):
        config_exists = os.path.isfile(_FILENAME)
        if config_exists:
            with open(_FILENAME, "r") as infile:
                self._configuration_dictionary = json.load(infile)
        else:
            self._configuration_dictionary = {}

        self._ensure_field_set(_KEY_LOG_DIRECTORY, ".")
        self._ensure_field_set(_KEY_LAST_OPEN_TRACK, "reinvent_base")
        self._ensure_field_set(_KEY_CALCULATE_ALTERNATE_DISCOUNT_FACTORS, False)
        self._ensure_field_set(_KEY_CALCULATE_NEW_REWARD, False)

        if not config_exists:
            self._save()

    def _ensure_field_set(self, key, default):
        if key not in self._configuration_dictionary:
            self._configuration_dictionary[key] = default

    def _save(self):
        with open(_FILENAME, "w+") as outfile:
            json.dump(self._configuration_dictionary, outfile, indent=2)

    def get_log_directory(self):
        return self._configuration_dictionary[_KEY_LOG_DIRECTORY]

    def get_last_open_track(self):
        return self._configuration_dictionary[_KEY_LAST_OPEN_TRACK]

    def get_calculate_new_reward(self):
        return self._configuration_dictionary[_KEY_CALCULATE_NEW_REWARD]

    def get_calculate_alternate_discount_factors(self):
        return self._configuration_dictionary[_KEY_CALCULATE_ALTERNATE_DISCOUNT_FACTORS]

    def set_log_directory(self, value):
        self._configuration_dictionary[_KEY_LOG_DIRECTORY] = value
        self._save()

    def set_last_open_track(self, value):
        self._configuration_dictionary[_KEY_LAST_OPEN_TRACK] = value
        self._save()

    def set_calculate_new_reward(self, value):
        self._configuration_dictionary[_KEY_CALCULATE_NEW_REWARD] = value
        self._save()

    def set_calculate_alternate_discount_factors(self, value):
        self._configuration_dictionary[_KEY_CALCULATE_ALTERNATE_DISCOUNT_FACTORS] = value
        self._save()