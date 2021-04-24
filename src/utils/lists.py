#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

# Ugly but using * operator gives a list of the same list (by reference) instead of unique lists
def get_list_of_empty_lists(size):
    new_list = []
    for i in range(0, size):
        new_list.append([])
    return new_list