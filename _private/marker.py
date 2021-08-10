#     ____            ________              
#    / __ )____ _____/ / ____/___ _________
#   / __  / __ `/ __  / /   / __ `/ ___/ _ \
#  / /_/ / /_/ / /_/ / /___/ /_/ (__  )  __/
# /_____/\__,_/\__,_/\____/\__,_/____/\___/
#

import io
import os
import random

from . import utils, classutils

class Marker(object):
    _marker_class_src = [
        ".class public interface abstract annotation %s",
        ".super Ljava/lang/Object;",
        "",
        ".implements Ljava/lang/annotation/Annotation;",
        "",
        ".annotation runtime Ljava/lang/annotation/Retention;",
        utils.pad("value = .enum Ljava/lang/annotation/RetentionPolicy;->RUNTIME:Ljava/lang/annotation/RetentionPolicy;"),
        ".end annotation",
        "",
        ".annotation runtime Ljava/lang/annotation/Target;",
        utils.pad("value = .enum Ljava/lang/annotation/ElementType;->TYPE:Ljava/lang/annotation/ElementType;"),
        ".end annotation",
        "",
        "",
        "# name of the method containing our sprinkles",
        ".method public abstract a()Ljava/lang/String;",
        ".end method",
        "",
        "# the number of sprinkles the marked class holds",
        ".method public abstract b()I",
        ".end method",
        "",
        "# the offset the last sprinkle of the marked class",
        ".method public abstract c()I",
        ".end method",
        "",
        "# determines if the sprinkles are gzip-encoded",
        ".method public abstract d()Z",
        ".end method"
    ]

    def __init__(self):
        self.smali = None

    def mark_target(self, target):
        return self._build(target)

    def write(self, clazz, data):
        header = data['header']
        body = data['body']
        footer = data['footer']

        written = 0

        written += clazz.write(header['type'])
        written += clazz.write(' ')
        written += clazz.write(header['retention'])
        written += clazz.write(' ')
        written += clazz.write(header['classpath'])
        written += clazz.write('\n')

        for k, v in body.items():
            if type(v) is int:
                v = '0x%x' % v
            elif type(v) is bool:
                v = str(v).lower() 
            elif type(v) is str:
                v = '"' + v + '"'
            elif type(v) is None:
                v = 'null'

            written += clazz.write(utils.pad(k + ' = ' + str(v)))
            written += clazz.write('\n')

        written += clazz.write(footer)
        written += clazz.write('\n\n')

        return written

    @classmethod
    def init(cls, instance, args):
        class_name, class_file = cls._gen_class_meta(args)
        
        cls._marker_class_src[0] = (cls._marker_class_src[0] 
                                        % class_name)

        instance.smali = classutils.SmaliClass(cls._marker_class_src)

        # uncomment in production release
        with open(class_file, 'w') as marker_class:
            for line in Marker._marker_class_src:
                marker_class.write(line)

        print("[ + ] Marker created as '%s'." % class_name)

    @staticmethod
    def _gen_class_meta(args):
        classes = list(utils.qual_classlist(os.path.join(args.gg_src, 'smali'),
                                                recurse = True))
        meta = {
            'class_name': '',
            'class_file': ''
        }

        clazz = random.choice(classes)

        while '$' in clazz:
            clazz = random.choice(classes)
        
        subclasses = list(classutils.innerclasses_of(clazz))
        names = []

        for subclass in subclasses:
            if len(subclass.name) <= utils.MAX_FILENAME_THRESHOLD:
                names.append(subclass.name)

        next_prgd = classutils.next_proguard_name(names)

        while next_prgd in names:
            names.append(next_prgd)

            next_prgd = classutils.next_proguard_name(names)

        meta['class_file'] = '%s$%s.smali' % (clazz[:clazz.rfind('.smali')],
                                                    next_prgd)
        meta['class_name'] = classutils.fs2bin_cp(meta['class_file'])

        return tuple(meta.values())

    def _build(self, target):
        return {
            'header': {
                'type': '.annotation',
                'retention': 'runtime',
                'classpath': self.smali.classpath
            },
            'body': {
                'a': target.chosen_name,
                'b': 0,
                'c': 0,
                'd': False
            },
            'footer': '.end annotation'
        }