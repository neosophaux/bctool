import re
import io

from ..classutils import AccessFlags
from ..opcodes import DexOpcodes

class MethodReader(object):
    def __init__(self, src):
        self._src = src
        self.header = re.match(
            "^\\.method(.*)\\s[A-Za-z_]+\\((.*)\\)(.+)$",
            self._src[0]
        )

    def get_ret_type(self):
        return self.header[3]

    def get_params(self):
        if len(self.header[2]) == 0:
            return []

        p_str = io.StringIO(self.header[2])
        p_lst = []

        while True:
            c = p_str.read(1)

            if len(c) == 0:
                break;

            if c == '[':
                if len(p_lst) == 0:
                    p_lst.append('[')

                    continue

                if p_lst[-1][0] != '[':
                    p_lst.append('[')

                    continue

                p_lst[-1] += '['

                continue

            if c == b'L':
                src_str = p_str.getvalue()
                type_end = src_str.find(';', p_str.tell())

                _type = src_str[p_str.tell() - 1:type_end + 1]

                if p_lst[-1][-1] == '[':
                    p_lst[-1] += _type
                    p_str.read(len(_type) - 1)
                else:
                    p_lst.append(_type)
                    p_str.read(len(_type) - 1)

                continue

            if len(p_lst) > 0 and p_lst[-1][-1] == '[':
                p_lst[-1] += c
            else:
                p_lst.append(c)

        p_str.close()

        return p_lst

    def get_access_flags(self):
        return self.header[1].strip().split(' ')

    def is_native(self):
        return AccessFlags.NATIVE in self.get_access_flags()

    def is_abstract(self):
        return AccessFlags.ABSTRACT in self.get_access_flags()

    def get_instructions(self):
        if self.is_abstract() or self.is_native():
            return []

        def generator():
            for inst in self._next_instruction():
                yield DexOpcodes.dxcode_from_inst(inst)

        return list(generator())

    def _next_instruction(self):
        for line in self._src:
            if re.match("^(\\.|:|})", line):
                continue
            
            inst_match = re.match("^(?:[a-z]+(?:-\\w+|\\/\\w+)*)(.*$)", line)
            instruction = instruction.replace(inst_match[1], '').strip()

            if DexOpcodes.get_opcode(instruction) != -1:
                yield instruction