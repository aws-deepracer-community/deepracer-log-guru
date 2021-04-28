#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import copy

from src.sequences.sequence import Sequence


class Sequences:
    def __init__(self):
        self._sequences = dict()

    def add(self, sequence: Sequence):
        if sequence.is_valid():
            key = sequence.get_simple_key()
            if key not in self._sequences:
                self._sequences[key] = sequence
            elif sequence.get_length() > self._sequences[key].get_length():
                self._sequences[key] = sequence

            inverted_key = sequence.get_simple_inverted_key()
            if inverted_key not in self._sequences:
                self._sequences[inverted_key] = sequence.build_inverted_copy()
            elif sequence.get_length() > self._sequences[inverted_key].get_length():
                self._sequences[inverted_key] = sequence.build_inverted_copy()

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

