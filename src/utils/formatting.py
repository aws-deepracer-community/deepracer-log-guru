def get_pretty_small_float(number, max_value, decimal_places):
    assert 0 <= decimal_places <= 1

    if max_value >= 10 and abs(round(number, decimal_places)) < 10:
        prepend = " "
    else:
        prepend = ""

    full_str = prepend + str(round(number, decimal_places))

    if full_str.count(".") == 1 and decimal_places == 0:
        return full_str[0:-2]
    elif full_str.endswith(".0") and decimal_places == 1:
        return full_str[0:-2] + "  "
    elif full_str.count(".") == 0 and decimal_places == 1:
        return full_str + "  "
    else:
        return full_str


def get_pretty_large_integer(number):
    return "{:,}".format(round(number))


def get_pretty_large_float(number):
    return "{:,}".format(number)


def get_pretty_whole_percentage(number):
    return str(round(number)) + " %"
