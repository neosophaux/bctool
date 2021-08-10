#     ____            ________              
#    / __ )____ _____/ / ____/___ _________
#   / __  / __ `/ __  / /   / __ `/ ___/ _ \
#  / /_/ / /_/ / /_/ / /___/ /_/ (__  )  __/
# /_____/\__,_/\__,_/\____/\__,_/____/\___/
#

import re
import os

from io import SEEK_END, SEEK_SET
from . import classutils, utils

class Target(object):
    def __init__(self, clazz, marker):
        self.fileobj = clazz
        self.lines = clazz.readlines()
        self.smali = classutils.SmaliClass(self.lines)
        self.chosen_name = self.smali.next_method
        self._marker = marker.mark_target(self)

    @property
    def marker(self):
        return self._marker

    # unfortunately i had to obsolete this :(

    # optimal way of checking if the class contains any methods
    # other than the constructors.
    #def is_empty_class(self):
    #    for method in self.methods:
    #        if method == '<init>' or method == '<clinit>':
    #            continue
    #        else:
    #            return False
    #    return True

    def write(what):
        self.seek(0, SEEK_END)
        self.fileobj.write(what.encode('utf-8'))

    def write_at(what, offset):
        self.seek(offset, SEEK_SET)
        self.fileobj.write(what.encode('utf-8'))

def remaining(buf):
    return (len(buf.getvalue()) - buf.tell()) 

class Sprinkler(object):
    def __init__(self, opts):
        self.sprinkle_size = opts['size']
        self.opts = opts

    def _write_header(self, hdr, clazz):
        signature = hdr['signature']
        written = 0

        written += clazz.write(hdr['type'])
        written += clazz.write(' ')

        for flag in hdr['access_flags']:
            written += clazz.write(flag)
            written += clazz.write(' ')

        written += clazz.write(signature['name'])
        written += clazz.write('(')

        for param in signature['params']:
            written += clazz.write(param)

        written += clazz.write(')')
        written += clazz.write(signature['return_type'])

        return written

    def write(self, clazz, data):
        notes = data['notes']
        header = data['header']
        body = data['body']

        written = 0

        for line in notes:
            written += clazz.write(line)
            written += clazz.write('\n')

        written += self._write_header(header, clazz)
        written += clazz.write('\n')

        written += clazz.write(utils.pad(".locals %d" % data['locals']))
        written += clazz.write('\n')
        written += clazz.write(utils.pad(".prologue"))
        written += clazz.write('\n')

        for line in body:
            written += clazz.write(line)
            written += clazz.write('\n')

        written += clazz.write(data['footer'])

    def _recalc_sprinkle_sz(self, buf):
        if ((remaining(buf) - self.sprinkle_size) 
                        < self.sprinkle_size):
            self.sprinkle_size = remaining(buf) - self.sprinkle_size
        else:
            self.sprinkle_size = self.opts['size']

    def _build_payload(self, target, instructions):
        inst_sz = 16 if self.sprinkle_size > 7 else 4
        template = {
            'notes': [
                "# make sure you decompile and recompile the",
                "# apk with apktool."
            ],
            'header': {
                'type': '.method',
                'access_flags': [
                    classutils.AccessFlags.PUBLIC,
                    classutils.AccessFlags.STATIC
                ],
                'signature': {
                    'name': target.chosen_name,
                    'params': [],
                    'return_type': '[I'
                }
            },
            'locals': 3,
            'body': [
                '',
                utils.pad("const/%d v0, 0x%s") % (inst_sz, self.sprinkle_size),
                '',
                utils.pad("new-array v0, v0, [I"),
                ''
            ],
            'footer': ".end method"
        }

        for instruction in instructions:
            template['body'].append(instruction)
            template['body'].append('')

        template['body'].append(utils.pad("return-object v0"))

        return {
            'marker': target.marker,
            'payload': template,
            'classpath': target.smali.classpath
        }

    def sprinkle(self, target, buf):
        self._recalc_sprinkle_sz(buf)
        load = []

        target.marker['body']['b'] = self.sprinkle_size
        target.marker['body']['c'] = buf.tell() + self.sprinkle_size
        target.marker['body']['d'] = utils.is_gzipped(buf)

        for i in range(self.sprinkle_size):
            char = ord(buf.read(1))
            inst_sz = 16 if char > 7 else 4
            idx_inst_sz = 16 if i > 7 else 4

            load.extend([
                utils.pad("const/%d v1, 0x%x" % (inst_sz, char)),
                utils.pad("const/%d v2, 0x%x" % (idx_inst_sz, i)),
                utils.pad("aput v1, v0, v2")
            ])

        return self._build_payload(target, load)