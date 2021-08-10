import os

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