import re
import io

def get_params(hdr):
    if len(hdr) == 0:
        return []

    p_str = io.StringIO(hdr)
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

        if c == 'L':
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

params = 'ZZZZZZZZIBCDJ[[[FFFFCC[[[[BBF[[VVVVVVFFF[[CCC[[[[[[[[CSSSSSSZZZSSCB'

print(get_params(params))