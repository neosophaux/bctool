#     ____            ________              
#    / __ )____ _____/ / ____/___ _________
#   / __  / __ `/ __  / /   / __ `/ ___/ _ \
#  / /_/ / /_/ / /_/ / /___/ /_/ (__  )  __/
# /_____/\__,_/\__,_/\____/\__,_/____/\___/
#

import re

from .annotation_reader import AnnotationReader

class FieldReader(object):
    def __init__(self, field):
        if isinstance(field, list):
            self._field_hdr = field[0]
        else:
            self._field_hdr = field

        self._field = field

        self._header_parsed = re.match("\\.field(.*)\\s([A-Za-z0-9_]+):(.*)", self._field_hdr)
        self._type = re.sub("\\s=\\s.*", '', self.header_parsed[3])

    @property
    def flags(self):
        return self._header_parsed[1].strip()

    @property
    def name(self):
        return self._header_parsed[2]

    @property
    def type(self):
        return self._type.strip()

    def get_constant(self):
        return re.search("\\s=\\s(.*)", self.header_parsed[3])[1]

    # this should return AnnotationReader instances
    def get_annotations(self):
        if not isinstance(self._field, list):
            return []

        annotations = []

        for idx, line in enumerate(self._field):
            if idx == 0 or idx == len(self._field) - 1:
                continue # skip the header or footer

            if len(line) == 0:
                continue

            # honestly... why didn't i just fetch all the fields in
            # ClassReader.get_fields this way?? oh well, i struggled
            # too much getting that to work to rewrite it.
            if line.startswith('.annotation'):
                annotations.append(idx)

                continue

            if line == '.end annotation':
                annotations[-1] = (annotations[-1], idx + 1)

        def generator():
            for annotation in annotations:
                src = [line for line in field[annotation[0]:annotation[1]] if len(line)]

                yield AnnotationReader(src)

        return list(generator())