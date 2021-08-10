# usage: python3 annotations_processor.py /path/to/smali/folder

import os
import re
import json
import sys

ANNOTATION_HDR_RGX = re.compile("^.annotation\\s+(build|system|runtime)"
                                    "\\s+(L.*;)")

def process_annotation_body(annotation, body):
    lines = list(map(lambda l: 
                    l.replace(',', '').strip(), body))

    for ln, line in enumerate(lines):
        if ' = ' in line:
            parts = line.split(' = ')

            key = parts[0]
            val = parts[1]

            annotation['values'][key] = []

            if val == '{':
                arr_begin = lines[ln + 1:]

                for item in arr_begin:
                    if item == '}':
                        break

                    annotation['values'][key].append(item)
            else:
                annotation['values'][key].append(val)

    return annotation

def get_annotations(src):
    locations = []

    for ln, line in enumerate(src):
        match = ANNOTATION_HDR_RGX.search(line)

        if match is not None:
            locations.append([ln + 1, 0, {
                    'visibility': match[1],
                    'type': match[2],
                    'values': {}
                }])

            continue

        if line == '.end annotation\n':
            locations[-1][1] = ln

    for location in locations:
        body = src[location[0]:location[1]]
        
        yield process_annotation_body(location[2], body)

for parent, _, files in os.walk(sys.argv[1]):
    for file in files:
        if file.endswith('.smali'):
            with open(os.path.join(parent, file), 'r') as clazz:
                for annotation in get_annotations(clazz.readlines()):
                    print(json.dumps(annotation, indent = 4))