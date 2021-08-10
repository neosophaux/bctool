import sys
import os
import json

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

def get_fields(tag):
    marker = get_marker_ln(tag)
    marker_next = next_marker(from_pos = marker)
    fields = list(map(str.strip, src[marker + 1:marker_next]))
    fields = [f for f in fields if len(f) > 0]
    field_indexes = []

    for idx, field in enumerate(fields):
        if field == '':
            continue

        if field == '.end field':
            header = 0

            for _idx, line in enumerate(fields[:idx][::-1]):
                if line.startswith('.field'):
                    header = (idx - _idx) - 1

                    field_indexes.pop(field_indexes.index(header))
                    break

                field_indexes.pop(field_indexes.index((idx - _idx) - 1))
            field_indexes.append((header, idx))

            continue

        field_indexes.append(idx)

    for field_index in field_indexes:
        if isinstance(field_index, tuple):
            yield fields[field_index[0]:field_index[1] + 1]
        else:
            yield fields[field_index]

with open(sys.argv[1], 'r') as f:
    src = f.readlines()

print(json.dumps(list(get_fields('# instance fields')), indent = 4))