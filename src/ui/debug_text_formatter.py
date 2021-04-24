#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

def get_formatted_debug(debug: str, max_lines, max_length, fields: list):
    if max_length == 0 or max_lines == 0 or not debug:
        if debug:
            return "..."
        else:
            return ""

    if fields is not None and len(fields) > 0:
        prepared_debug = ""
        for line in debug.split("\n"):
            prepared_debug += _extract_named_fields(line, fields)
    else:
        prepared_debug = debug

    formatted = ""
    lines = prepared_debug.split("\n")
    for line in lines[0:min(len(lines), max_lines)]:
        if formatted:
            formatted += "\n"
        if len(line) > max_length:
            formatted += line[0:max_length] + " ..."
        else:
            formatted += line

    if max_lines < len(lines):
        formatted += "\n..."

    return formatted


def _extract_named_fields(debug: str, fieldnames: list):
    try:
        dictionary = eval(debug)
    except:
        return ""

    result = ""
    for f in fieldnames:
        try:
            value = str(dictionary[f])
            if result:
                result += "\n"
            result += f + " = " + value
        except:
            pass

    return result


# test="one\ntwo\nthree\nfour\nfive"

# print(get_formatted_debug(test, 3, 3))

# test = "{'all_wheels_on_track': True, 'x': 3.4966725287629434, 'y': 0.7091793617646284}"

# print("-------")
# print(get_formatted_debug(test, 5, 21, ["x", "crap", "y", "all_wheels_on_track"]))
# print("-------")
