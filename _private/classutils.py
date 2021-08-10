#     ____            ________              
#    / __ )____ _____/ / ____/___ _________
#   / __  / __ `/ __  / /   / __ `/ ___/ _ \
#  / /_/ / /_/ / /_/ / /___/ /_/ (__  )  __/
# /_____/\__,_/\__,_/\____/\__,_/____/\___/
#

import re
import os
import io

from . import utils
from .opcodes import DexOpcodes, ReferenceType

class AccessFlags():
    ABSTRACT = 'abstract'
    ANNOTATION = 'annotation'
    BRIDGE = 'bridge'
    ENUM = 'enum'
    FINAL = 'final'
    INTERFACE = 'interface'
    MANDATED = 'mandated'
    MODULE = 'module'
    NATIVE = 'native'
    PRIVATE = 'private'
    PROTECTED = 'protected'
    PUBLIC = 'public'
    STATIC = 'static'
    STRICT = 'strict'
    SUPER = 'super'
    SYNCHRONIZED = 'synchronized'
    SYNTHETIC = 'synthetic'
    TRANSIENT = 'transient'
    VARARGS = 'varargs'
    VOLATILE = 'volatile'

def fs2bin_cp(classpath):
    cp = classpath[classpath.find(
                    'smali' + os.path.sep) + (len(os.path.sep) + 5):][:-6]
    cp = 'L' + cp
    cp += ';'

    return cp

def bin2fs_cp(root, classpath):
    cp = classpath[1:-1]
    cp += '.smali'

    return os.path.join(root, cp)

# generates the next 'proguarded' name from a list of existing
# proguarded names. epic.
def next_proguard_name(defined):
    if len(defined) == 0:
        return 'a'

    families = []

    for name in sorted(set(defined)):
        if len(families) == 0:
            families.append([name])

            continue

        if name[0] == families[-1][0][0]:
            families[-1].append(name)
        else:
            families[-1] = sorted(families[-1])

            families.append([name])

    if families[-1][0] < 'z':
        if families[-1][0] == 'Z':
            return 'a'

        family = families[-1]
        member = family[-1]
        modifier = member[-1]

        return member[:-1] + chr(ord(modifier) + 1)

    _families = []

    for family in families:
        _families.extend(family)

    namesz = 2
    longest = len(sorted(_families, key = len)[-1])
    single_families = []

    if longest == 1:
        single_families = families

    while namesz <= longest:
        for family in families:
            if len(family) == 1:
                single_families.append(family)

                if family[0] == 'z':
                    namesz += 1

                continue

            for member in family:
                if len(member) > namesz or len(member) < namesz:
                    continue

                if member[-1] == 'z' or member[-1] == 'Z':
                    break

                return member[:-1] + chr(ord(member[-1]) + 1)

            if family[0] == 'z' or family[0] == 'Z':
                namesz += 1

    family = single_families[0]

    return family[0] + chr(ord(family[0]) + 1)

def innerclasses_of(fs_classpath):
    filename = os.path.basename(fs_classpath)
    parent = os.path.dirname(fs_classpath)
    classname = filename.replace('.smali', '').split('$')[0] + '$'

    for file in utils.classlist(parent):
        if file != filename and file.startswith(classname):
            subclass_fileobj = open(os.path.join(parent, file)) # dont forget to close this.
            subclass = SmaliClass(subclass_fileobj.readlines())

            # this is sorta redundant but i wanna make use of all the
            # awesome code i wrote, lol
            if subclass.is_inner():
                yield subclass

            subclass_fileobj.close()

class SmaliClass(object):
    # Determines the maximum name length of a method for it to qualify
    # as a candidate to base the payload's method name off of.
    # I recommend leaving this as is to keep things inconspicuous.
    _qual_mth_name_len = 2

    _method_name_rgx = re.compile("\\.method.*\\s([A-Za-z_]{1,%d})\\(.*\\).+$"
                                    % _qual_mth_name_len)
    _class_hdr_rgx =   re.compile("^\\.class\\s*(.*)\\s+(L.*;)")
    _annoation_rgx =   re.compile("^.annotation\\s+(build|system|runtime)"
                                    "\\s+(L.*;)")

    def __init__(self, class_src):
        self._class_hdr = SmaliClass._class_hdr_rgx.match(class_src[0])
        self._access_flags = self._class_hdr[1].split()
        self._bin_name = self._class_hdr[2]
        self._class_name = self._get_real_name()
        self._annotations = list(self._get_annotations(class_src))
        self._methods = list(self._get_methods(class_src))
        self._next_method = next_proguard_name(self._methods)
        self._class_src = class_src

    @property
    def access_flags(self):
        return self._access_flags

    @property
    def classpath(self):
        return self._bin_name
    
    @property
    def methods(self):
        return self._methods

    @property
    def name(self):
        return self._class_name
    
    @property
    def next_method(self):
        return self._next_method

    def has_inner_spec(self):
        for annotation in self._annotations:
            if annotation['type'] == 'Ldalvik/annotation/InnerClass;':
                return True

        return False

    # first check if the InnerClass annotation exists.
    # if False, check if the inner class delimiter '$'
    # exists within the class' binary name and make
    # sure it is not the actual name of the class
    # itself. big brain time bois.
    def is_inner(self):
        if not self.has_inner_spec():
            return self._bin_name.rfind('$') + 2 != len(self._bin_name)

    def is_anon(self):
        for annotation in self._annotations:
            if annotation['type'] == 'Ldalvik/annotation/InnerClass;':
                return (annotation['values']['name'] == 'null')

        return False

    # hmm... i should expand on this more so that the type is replaced
    # everywhere.. including the manifest xml, binary resources, and
    # references to it throughout the code. but this should suffice
    # for it's one and only use.
    def new_type(self, t):
        for idx, line in enumerate(self._class_src):
            self._class_src[idx] = line.replace(self._bin_name, t)

        self._bin_name = t
        self._class_name = self._get_real_name()

    @classmethod
    def iter_dir(cls, path, recurse = False):
        for file in utils.classlist(path, recursive = recurse):
            fileobj = open(os.path.join(path, file), 'r')

            yield cls(fileobj.readlines())

            fileobj.close()

    def _get_real_name(self):
        return self._bin_name.split('$')[-1]

    def _process_annotation_body(self, annotation, body):
        lines = list(map(lambda l: l.replace(',', '').strip(), body))

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

    def _get_annotations(self, src):
        locations = []

        for ln, line in enumerate(src):
            match = SmaliClass._annoation_rgx.search(line)

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
            
            yield self._process_annotation_body(location[2], body)

    def _get_methods(self, src):
        for line in src:
            match = SmaliClass._method_name_rgx.search(line)

            if match is not None and self._valid_method(match[1]):
                yield match[1]

    def _valid_method(self, name):
        return (len(name) <= SmaliClass._qual_mth_name_len)