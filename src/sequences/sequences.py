#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import json

from src.sequences.sequence import Sequence

_FILENAME = "DRG_sequences.json"


class Sequences:
    def __init__(self):
        self._sequences = dict()
        self._modified = False

    def add(self, sequence: Sequence):
        if sequence.is_valid():
            key = sequence.get_simple_key()
            if key not in self._sequences:
                self._sequences[key] = sequence
                self._modified = True
            elif sequence.get_length() > self._sequences[key].get_length():
                self._sequences[key] = sequence
                self._modified = True

            inverted_key = sequence.get_simple_inverted_key()
            if inverted_key not in self._sequences:
                self._sequences[inverted_key] = sequence.build_inverted_copy()
                self._modified = True
            elif sequence.get_length() > self._sequences[inverted_key].get_length():
                self._sequences[inverted_key] = sequence.build_inverted_copy()
                self._modified = True

    def add_sequences(self, sequences):
        for s in sequences.get_all():
            self.add(s)

    def print_debug(self):
        print("Sequences length = ", len(self._sequences))
        for s in self.get_all():
            s.print_debug()

    def get_all(self):
        return self._sequences.values()

    def get_matches(self, initial_track_speed, initial_slide, action_speed, action_steering_angle):
        result = []
        for s in self.get_all():
            if s.matches(initial_track_speed, initial_slide, action_speed, action_steering_angle):
                add_on_key = s.get_simple_key_for_add_on()
                if add_on_key in self._sequences:
                    s.set_add_on(self._sequences[add_on_key])
                else:
                    s.set_add_on(None)
                result.append(s)
        return result

    def get_as_json(self):
        sequences_json = []
        for s in self._sequences.values():
            sequences_json.append(s.get_as_json())

        new_json = dict()
        new_json["sequences"] = sequences_json
        return new_json

    def set_from_json(self, received_json):
        self._sequences = dict()
        for s in received_json["sequences"]:
            new_sequence = Sequence()
            new_sequence.set_from_json(s)
            self.add(new_sequence)

    def load(self):
        try:
            with open(_FILENAME, "r") as infile:
                self.set_from_json(json.load(infile))
        except FileNotFoundError:
            pass
        self._modified = False

    def save(self):
        if self._modified:
            with open(_FILENAME, "w+") as outfile:
                json.dump(self.get_as_json(), outfile)
            self._modified = False
