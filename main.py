# TODO: right now, this only supports single character signals

import os

SIGNAL_DATE = "="
SIGNAL_COMMENT = "/"

# an open/close signal is a signal that applies a tag to the following text
# first a signal opens a tag, then while open prints a bunch of lines, then closes the tag
SIGNALS_OPEN_CLOSE = [SIGNAL_COMMENT, SIGNAL_DATE]

SIGNAL_URL = "*"
SIGNAL_PERSONAL_COMMENT = "-"
SIGNALS_SINGLE_LINE = [SIGNAL_URL, SIGNAL_PERSONAL_COMMENT]

SIGNAL_TAGS = {
    SIGNAL_DATE : "h2",
    SIGNAL_COMMENT : "i",
    SIGNAL_URL : "h4",
    SIGNAL_PERSONAL_COMMENT : "p"
}


# returns a string which is a tag associated with this combination
# is_opening : boolean; signal : char
def get_tag(signal, is_open_tag = True):
    output_tag = ""
    if is_open_tag:
        output_tag += "<" + SIGNAL_TAGS.get(signal) + ">"
    else:
        output_tag += "</" + SIGNAL_TAGS.get(signal) + ">"

    return output_tag


# Note: the way this is currently written, text MUST be inside a signal to be written at all
# Is this the correct design choice?
def convert_log(input_file_path, output_file_path):
    input_file = open(input_file_path, "r")
    output_file = open(output_file_path, "w")
    is_signal_open = False

    for line in input_file:
        first_char = line[0]
        current_line = ""

        # If the first char of the current line is a signal, and it is currently not open,
        # then set it to open and write down its html tag
        # If it is already open, then set it to not open, and close the tag

        if is_signal_open:
            if first_char in SIGNALS_OPEN_CLOSE:
                is_signal_open = False
                current_line += get_tag(first_char, False)
            else:
                current_line = line + "<br>"
        else:
            if first_char in SIGNALS_SINGLE_LINE:
                current_line += get_tag(first_char)
                # get everything after the space (which occurs after the signal)
                content = line[line.index(" ") + 1:]

                if first_char == SIGNAL_URL:
                    url_and_summary = content.split(' ', 1)
                    current_line += "<a href=" + url_and_summary[0] + ">" + url_and_summary[0] + "</a>"
                    if len(url_and_summary) > 1:
                        current_line += " " + url_and_summary[1] + ""
                else:
                    current_line += content

                current_line += get_tag(first_char, False)
            elif first_char in SIGNALS_OPEN_CLOSE:
                is_signal_open = True
                current_line += get_tag(first_char)

        output_file.write(current_line)

    output_file.close()
    input_file.close()


path = "./tests"
input_file_path = path + "/test-log.txt"
output_file_path = path + "/test-output.html"
convert_log(input_file_path, output_file_path)
