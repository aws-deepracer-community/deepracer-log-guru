#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import inspect


def enforce():
    caller = inspect.stack()[1][3]
    print("ERROR - Abstract Method has not been overridden in function: ", caller)
    exit(1)
