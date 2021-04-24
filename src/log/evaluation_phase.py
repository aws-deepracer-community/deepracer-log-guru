#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import numpy as np


class EvaluationPhase:
    #
    # PUBLIC interface (this whole class is basically just a data structure, so it's all public)
    #

    def __init__(self, rewards, progresses):
        assert len(rewards) == len(progresses)

        self.length = len(rewards)
        self.rewards = np.array(rewards)
        self.progresses = np.array(progresses)
