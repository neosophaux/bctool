import sys
import os
import json
import re

src = None

def get_marker_ln(tag):
    for ln, line in enumerate(src):
        if line == tag + os.linesep:
            return ln

    return -1

def next_marker(from_pos = 0):
    for ln, line in enumerate(src[from_pos + 1:]):
        if line[0] == '#':
            return ln + from_pos

    return None

def get_methods(tag):
    marker = get_marker_ln(tag)
    marker_next = next_marker(from_pos = marker)

    for line in src[marker + 1:marker_next]:
        match = re.match("\\.method.*\\s[A-Za-z0-9_<>]+\\(.*\\).+$", line)

        if match is not None:
            yield match[0]

with open(sys.argv[1], 'r') as f:
    src = f.readlines()

print(json.dumps(list(get_methods('# virtual methods')), indent = 4))