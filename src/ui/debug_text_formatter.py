

def get_formatted_debug(debug: str, max_lines, max_length):
    if max_length == 0 or max_lines == 0 or not debug:
        if debug:
            return "..."
        else:
            return ""

    formatted = ""
    lines = debug.split("\n")
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

# test="one\ntwo\nthree\nfour\nfive"

# print(get_formatted_debug(test, 3, 3))


