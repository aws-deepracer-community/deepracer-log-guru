#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import inspect


def enforce(self_instance):
    class_name = str(type(self_instance)).split(".")[-1][:-2]
    # Note that inspect is considered VERY slow, but not an issue since this is a fatal end to the program
    # Keeping it simple and avoiding a more complex import for no particularly good reason
    stack = inspect.stack()
    method_name = stack[1][3]
    called_from = stack[2][3]
    print("ERROR - Abstract method " + str(class_name) + "." + method_name +
          "() not overridden when called from " + called_from + "()")
    exit(1)
