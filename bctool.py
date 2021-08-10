#     ____            ________              
#    / __ )____ _____/ / ____/___ _________
#   / __  / __ `/ __  / /   / __ `/ ___/ _ \
#  / /_/ / /_/ / /_/ / /___/ /_/ (__  )  __/
# /_____/\__,_/\__,_/\____/\__,_/____/\___/
#
# usage: python3 bctool.py [-h] [--script PATH] [--gg-src DIR] [-p PKG]
#                          [--no-gui]
# 
# Sprinkles any script you give this tool across GG's code.
# 
# optional arguments:
#   -h, --help         Show this help message and exit
#   --script PATH      Path to the script you wish to sprinkle.
#   --gg-src DIR       Path to GG's src directory. Attempts to use the
#                      current directory if this is left blank.
#   -p PKG, --pkg PKG  Set this flag to make the tool sprinkle your
#                      script across a specific java
#                      package(directory). Defaults to luaj.
#   --no-gui           Disables the creation of a GUI, but requires you
#                      to atleast supply the --script option.
# 
# If you need any help, send me a mail.

# forgive the messiness of this lol. i underestimated how complicated this will get.

import os
import sys
import random
import math
import gzip
import json

from argparse import ArgumentParser, FileType
from distutils import dir_util
from io import BytesIO
from time import sleep

_fail_gui = False

if sys.platform == 'win32':
    try:
        from tkninter import Tk, filedialog
    except:
        # fail silently for now
        _fail_gui = True
else:
    try:
        from gi import require_version as gi_require_version

        gi_require_version("Gtk", "3.0")

        from gi.repository import Gtk, GLib
    except:
        _fail_gui = True

from _private import sprinkler, marker, utils
from _private.classutils import AccessFlags

_sprinkler = sprinkler.Sprinkler({'size': utils.MAX_CHARS_PER_FILE})
_marker = marker.Marker()

def validate_args(args):
    if not args.no_gui and _fail_gui:
        print("[ - ] Unable to create a GUI for the tool. Use --no-gui "
              "to skip the creation of a GUI if you're getting this error.")

        sys.exit(1)

    if args.no_gui and args.script is None:
        print("[ - ] No script file specified. Use --script.")

        sys.exit(1)

    if 'apktool.yml' not in os.listdir(args.gg_src):
        print("[ - ] APK must be decompiled with apktool.")

        sys.exit(1)

    if 'smali' not in os.listdir(args.gg_src):
        print("[ - ] Didn't find the smali source in root '%s'."
             % args.gg_src)

        sys.exit(1)

    s_dir = os.path.join(args.gg_src, 'smali')

    if 'bcmarker.smali' in os.listdir(s_dir):
        print("[ - ] APK file has already been processed. Use a clean APK.")

        sys.exit(1)

    if args.pkg != s_dir and args.pkg not in os.listdir(s_dir):
        if args.pkg != '.':
            print("[ - ] Didn't find the package '%s'." % args.pkg)

            sys.exit(1)

    args.script = BytesIO(args.script.read())

    # being dynamic and flexible is always good
    if utils.bufsz(args.script) > len(gzip.compress(b'\x00' * 64)):
        old_fsz = utils.bufsz(args.script)

        print("[ + ] Compressing script...", end = ' ')
        args.script = BytesIO(gzip.compress(args.script.read()))
        print("done.")

        print("[ + ] %d bytes -> %d bytes" % (old_fsz, utils.bufsz(args.script)))

    p_dir = os.path.join(s_dir, args.pkg)

    if not utils.valid_pkg(args, p_dir):
        print("[ - ] Can't use package '%s'; results would be obvious."
                % args.pkg)

        sys.exit(1)

    return args

def parse_args():
    parser = ArgumentParser(
        prog = 'python3 bctool.py',
        description = "Sprinkles any script you give this tool across GG's code.",
        epilog = "If you need any help, send me a mail."
    )

    parser.add_argument(
        '--script',
        help = "Path to the script you wish to sprinkle.",
        type = FileType('rb', 0),
        metavar = 'PATH'
    )

    parser.add_argument(
        '--gg-src',
        help = "Path to GG's src directory. Attempts to use the current " +
               "directory if this is left blank.",
        type = str,
        default = os.getcwd(),
        metavar = 'DIR'
    )

    parser.add_argument(
        '-p', '--pkg',
        help = "Set this flag to make the tool sprinkle your script across " +
               "a specific java package(directory). Defaults to luaj.",
        type = str,
        default = 'luaj',
        metavar = 'PKG'
    )

    parser.add_argument(
        '--no-gui',
        help = "Disables the creation of a GUI, but requires you to atleast " +
               "supply the --script option.",
        action = 'store_true',
        default = False
    )

    return parser.parse_args()

def mark_apk(args):
    with open(utils.get_apk_marker_path(args), 'w') as marker:
        marker.write(
            ".class private final Lbcmarker;\n"
            ".super Ljava/lang/Object;\n"
        )

        print("[ + ] APK file has been marked.")

def write_data(payload, clazz):
    # it doesn't really matter where certain elements of a smali
    # class file goes, so long as the syntax is correct and the
    # code checks out.
    marker = payload['marker']
    method = payload['payload']

    clazz.write('\n')

    # todo: this is straight up ugly and sloppy work.
    # fix this some time in the future, but it works
    # for now.
    _marker.write(clazz, marker)
    _sprinkler.write(clazz, method)

def finalizer():
    print("[ + ] Remember! Recompile the APK with apktool to avoid")
    print("[ + ] certain issues with the smali code.")

def main(args):
    script_sz = utils.bufsz(args.script)
    limit = math.ceil(script_sz / utils.MAX_CHARS_PER_FILE)
    classlist = utils.qual_classlist(utils.get_pkg_dir(args), recurse = True)
    processed = []

    print("[ + ] Generating sprinkle code...")

    for clazz in random.sample(list(classlist), limit):
        print(clazz)
        with open(clazz, 'r') as clazz_fileobj:
            target = sprinkler.Target(clazz_fileobj, _marker)

            if AccessFlags.INTERFACE not in target.smali.access_flags:
                payload = _sprinkler.sprinkle(target, args.script)

                processed.append({
                    'payload': payload,
                    'class': clazz
                })

    print("[ + ] Done.")
    print("[ + ] Processing and writing to files...", end = ' ')

    for item in processed:
        with open(item['class'], 'a') as clazz_fileobj:
            write_data(item['payload'], clazz_fileobj)

    print('done.')

    # hardcoded stuff below.
    print("[ + ] Writing TwoWayStream...")

    if not os.path.exists(utils.TWOWAYSTREAM):
        print("[ - ] TwoWayStream class not found.")

        sys.exit(1)

    with open(utils.TWOWAYSTREAM, 'r') as io_smali_r:
        with open(utils.TWOWAYSTREAM, 'w') as io_smali_w:
            parent_dir = random.choice(list(os.walk(utills.get_smali_dir(args))))
            classes = list(utils.qual_classlist(parent_dir[0], recurse = True))

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

            for line in io_smali_r:
                if 'LTwoWayStream;' in line:
                    line = line.replace('TwoWayStream', name)

def _gtk_stop():
    Gtk.main_quit()

    return False

def _gtk_quit():
    GLib.timeout_add(150, _gtk_stop)
    Gtk.main()

    sleep(1.3)

def init():
    class attrdict(dict):
        __getattr__ = dict.get
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

    # gather and process the command-line arguments
    args = attrdict(vars(parse_args()))

    if not args.no_gui:
        ui = utils._fsdialog()

        args.gg_src = ui.select_folder("Select GameGuardian's Folder")
        smali_dir = os.path.join(args.gg_src, 'smali')

        if not os.path.exists(smali_dir):
            print("[ - ] Selected folder has no smali source.")

            sys.exit(1)

        args.pkg = ui.select_folder("Select Package", root = smali_dir)
        args.script = ui.select_file("Select Lua Script", mode = 'rb',
                                        ext = [('Lua Script', '*.lua')])

        if sys.platform != 'win32':
            _gtk_quit()
            print() # to separate any possible gtk messages from the tool's messages.

    args = validate_args(args)
    backup = True

    if os.path.isdir(os.path.join(args.gg_src, 'smali_bak')):
        print("[ + ] A backup of the smali source already exists.")
        
        resp = input("[ + ] Overwrite? (yes/no): ").lower()

        if resp == 'no' or resp == 'n':
            backup = False

    if backup:
        print("[ + ] Backing up the smali folder...", end = ' ')

        smali_dir = os.path.join(args.gg_src, 'smali')
        bak_dir = os.path.join(args.gg_src, 'smali_bak')
        failed = False

        if len(dir_util.copy_tree(smali_dir, bak_dir, update = 1)) == 0:
            resp = input("\n[ - ] Failed. Proceed? (yes/no): ").lower()

            if resp == 'yes' or resp == 'y':
                failed = True
            else:
                sys.exit(1)

        if not failed:
            print('done.')

    # mark the apk
    # uncomment when doing a production release
    mark_apk(args)

    # initiate the marker
    marker.Marker.init(_marker, args)

    # invoke the main program
    main(args)

if __name__ == '__main__':
    init()
    finalizer()