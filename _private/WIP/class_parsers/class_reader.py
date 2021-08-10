import os

from enum import Enum as enum

from .method_reader import MethodReader
from .field_reder import FieldReader
from .annotation_reader import AnnotationReader

class SmaliTags(enum):
    INTERFACES = (0x00, '# interfaces')
    ANNOTATIONS = (0x01, '# annotations')
    STATIC_FIELDS = (0x02, '# static fields')
    INSTANCE_FIELDS = (0x03, '# instance fields')
    DIRECT_METHODS = (0x05, '# direct methods')
    VIRTUAL_METHODS = (0x06, '# virtual methods')

    def __init__(self, idx, tag):
        self.id = tag

# honestly i should have just subclassed the list class, lol
class ClassReader(object):
    def __init__(self, clazz):
        self._src = clazz.readlines()

    def get_marker_ln(self, tag):
        for ln, line in enumerate(self._src):
            if line == tag + os.linesep:
                return ln

        return -1

    def next_marker(self, from_pos = 0):
        for ln, line in enumerate(self._src[from_pos + 1:]):
            if line[0] == '#':
                return ln + from_pos

        return None

    def get_methods(self):
        return {
            'direct_methods': self.get_direct_methods(),
            'virtual_methods': self.get_virtual_methods()
        }

    def get_direct_methods(self):
        return list(self._get_methods_for(SmaliTags.DIRECT_METHODS))

    def get_virtual_methods(self):
        return list(self._get_methods_for(SmaliTags.VIRTUAL_METHODS))

    def _get_methods_for(self, tag):
        marker = get_marker_ln(tag)
        marker_next = next_marker(from_pos = marker)

        for line in self._src[marker + 1:marker_next]:
            match = re.match("\\.method.*\\s[A-Za-z0-9_<>]+\\(.*\\).+$", line)

            if match is not None:
                yield match[0]

    def get_fields(self):
        return {
            'static_fields': self.get_static_fields(),
            'instance_fields': self.get_instance_fields()
        }

    def get_static_fields(self):
        return list(self._get_fields_for(SmaliTags.STATIC_FIELDS))

    def get_instance_fields(self):
        return list(self._get_fields_for(SmaliTags.INSTANCE_FIELDS))

    # this was incredibly complicated.
    # some of the yielded items may be a list, in case the field definition
    # spans over multiple lines
    def _get_fields_for(self, tag):
        if self.get_marker_ln(tag) == -1:
            return []

        marker = get_marker_ln(tag)
        marker_next = next_marker(from_pos = marker)

        fields = list(map(str.strip, self._src[marker + 1:marker_next]))
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

    def read_method(self, method_sig):
        start = None
        end = None

        for ln, line in enumerate(self._src):
            if line.startswith('.method') and method_sig in line:
                start = ln

                for _ln, _line in enumerate(self._src):
                    _ln += start

                    if line == '.end method':
                        end = _ln

        if start == None:
            raise Exception("method signature %s not found in class %s"
                            % (method_sig, self._src[0][self._src[0].find('L'):]))

        input(self._src[start:end])

        return MethodReader(self._src[start:end])

    def __add__(self, other):
        for item in other:
            if not isinstance(item, str):
                raise ValueError("list must contain str or str-like objects only.")

        return self._src.__add__(other)

    def __contains__(self, key):
        return self._src.__contains__(key)

    def __delitem__(self, key):
        self._src.__delitem__(key)

    def __eq__(self, other):
        for idx, item in enumerate(other):
            if not isinstance(item, str):
                other.pop(idx)
        
        return self._src.__eq__(other)

    def __ge__(self, other):
        for idx, item in enumerate(other):
            if not isinstance(item, str):
                other.pop(idx)
        
        return self._src.__ge__(other)

    def __getattribute__(self, name):
        return self._src.__getattribute__(name)

    def __getitem__(self, key):
        return self._src.__getitem__(key)

    def __gt__(self, other):
        for idx, item in enumerate(other):
            if not isinstance(item, str):
                other.pop(idx)
        
        return self._src.__gt__(other)

    def __iadd__(self, other):
        for item in other:
            if not isinstance(item, str):
                raise ValueError("list must contain str or str-like objects only.")

        return self._src.__iadd__(other)

    def __imul__(self, other):
        for item in other:
            if not isinstance(item, str):
                raise ValueError("list must contain str or str-like objects only.")

        return self._src.__imul__(other)

    def __iter__(self):
        for item in self._src:
            yield item

    def __le__(self, other):
        for idx, item in enumerate(other):
            if not isinstance(item, str):
                other.pop(idx)

        return self._src.__le__(other)

    def __len__(self):
        return self._src.__len__()

    def __lt__(self, other):
        for idx, item in enumerate(other):
            if not isinstance(item, str):
                other.pop(idx)
        
        return self._src.__lt__(other)

    def __mul__(self, other):
        for item in other:
            if not isinstance(item, str):
                raise ValueError("list must contain str or str-like objects only.")

        return self._src.__mul__(other)

    def __ne__(self, other):
        for idx, item in enumerate(other):
            if not isinstance(item, str):
                other.pop(idx)

        return self._src.__ne__(other)

    def __repr__(self):
        return self._src.__repr__()

    def __reversed__(self):
        return self._src.__reversed__()

    def __rmul__(self, other):
        for item in other:
            if not isinstance(item, str):
                raise ValueError("list must contain str or str-like objects only.")

        return self._src.__rmul__(other)

    def __setitem__(self, key, val):
        if not isinstance(val, str):
            raise TypeError("value must be a str or str-like object.")

        return self._src.__setitem__(key, val)

    def __sizeof__(self):
        return self._src.__sizeof__()

    def append(self, item):
        if not isinstance(item, str):
            raise TypeError("value must be a str or str-like object.")

        self._src.append(item)

    def clear(self):
        self._src.clear()

    def copy(self):
        return self._src.copy()

    def count(self, val):
        return self._src.count(val)

    def extend(self, iterable):
        _iterable = list(iterable)

        for item in _iterable:
            if not isinstance(item, str):
                raise ValueError("iterable must contain str or str-like objects only.")

        self._src.extend(_iterable)

    def index(self, val, start = 0, stop = 9223372036854775807):
        return self._src.index(val, start = start, stop = stop)

    def insert(self, idx, val):
        if not isinstance(val, str):
            raise TypeError("value must be a str or str-like object.")

        self._src.insert(idx, val)

    def pop(self, idx):
        return self._src.pop(idx)

    def remove(self, val):
        self._src.remove(val)

    def reverse(self):
        self._src.reverse()

    def sort(self, *, key = None, reverse = False):
        return self._src.sort(key = key, reverse = reverse)