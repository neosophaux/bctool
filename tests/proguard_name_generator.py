# usage: python3 proguard_name_generator.py

import random
import string

MAX_SAMPLE_SIZE = 2

def generate_sample(size, count):
    source = string.ascii_lowercase
    sample = list(source)

    for i in range(count):
        complete = False

        while not complete:
            selection = ''.join(random.choices(
                                source, k = random.randint(1, size)))

            if selection in sample:
                continue

            sample.append(selection)

            complete = True

    return sample

sample = generate_sample(MAX_SAMPLE_SIZE, 27)

def next_proguard_name(defined):
    families = []

    for name in sorted(defined):
        if not families:
            families.append([name])

            continue

        if name[0] == families[-1][0][0]:
            families[-1].append(name)
        else:
            families[-1] = sorted(families[-1])

            families.append([name])

    print("Families: ")
    print(families, end = '\n\n')

    if families[-1][0] < 'z':
        family = families[-1]
        member = family[-1]

        return chr(ord(member) + 1)

    _families = []

    for family in families:
        _families.extend(family)

    namesz = 2
    longest = len(sorted(_families, key = len)[-1])
    single_families = []

    print("Longest: ")
    print(longest, end = '\n\n')

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

                if member[-1] == 'z':
                    break

                return member[:-1] + chr(ord(member[-1]) + 1)

            if family[0] == 'z':
                namesz += 1

    print("Single Families: ")
    print(single_families, end = '\n\n')

    family = single_families[0]

    return family[0] + chr(ord(family[0]) + 1)

print(next_proguard_name(sample))