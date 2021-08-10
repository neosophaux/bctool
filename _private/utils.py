#     ____            ________              
#    / __ )____ _____/ / ____/___ _________
#   / __  / __ `/ __  / /   / __ `/ ___/ _ \
#  / /_/ / /_/ / /_/ / /___/ /_/ (__  )  __/
# /_____/\__,_/\__,_/\____/\__,_/____/\___/
#

import os
import math
import glob
import sys
import re

from io import FileIO
from .classutils import SmaliClass

if sys.platform == 'win32':
    try:
        from tkninter import Tk, filedialog
    except:
        pass # the error is handled in bctool.py
else:
    try:
        from gi import require_version as gi_require_version

        gi_require_version("Gtk", "3.0")

        from gi.repository import Gtk
    except:
        pass

# Indentation per line of code
INDENT = 4

# Indentation character
INDENT_CHAR = ' '

# Determines the maxmium number of sprinkled characters per smali file.
# I recommend leaving this as is to keep things inconspicuous.
MAX_CHARS_PER_FILE = 8

# Determines the maximum allowable file name length in the file filter.
# I recommend leaving this as is to keep things inconspicuous.
MAX_FILENAME_THRESHOLD = 2

# Path to a custom smali class which supports input and output. used to
# hijack the InputStream of the lua parser.
TWOWAYSTREAM = 'rebuilder/smali/proguarded/TwoWayStream.smali'

class _fsdialog(object):
    def __init__(self):
        self._root = None
        self._funcs = {
            'file': {
                'select': None
            },
            'dir': {
                'select': None
            }
        }

        if sys.platform == 'win32':
            self._funcs['file']['select'] = _fsdialog._w32_rd_file
            self._funcs['dir']['select'] = _fsdialog._w32_sel_dir
            self._root = Tk()

            self._root.withdraw()
        else:
            self._funcs['file']['select'] = _fsdialog._nix_rd_file
            self._funcs['dir']['select'] = _fsdialog._nix_sel_dir

    def select_file(self, title, mode = 'r', root = '.', ext = []):
        return self._funcs['file']['select'](self, title, mode, root, ext)

    def select_folder(self, title, root = '.'):
        return self._funcs['dir']['select'](self, title, root)

    @classmethod
    def _w32_rd_file(cls, self, title, mode, root, ext):
        fobj = filedialog.askopenfile(
            mode = mode,
            title = title,
            initialdir = root,
            filetypes = ext
        )

        if fobj == None:
            print("[ + ] Cancelled.")

            sys.exit(1)

        return fobj

    @classmethod
    def _w32_sel_dir(cls, self, title, root):
        dpath = filedialog.askdirectory(
            title = title,
            initialdir = root,
            mustexist = True
        )

        if len(path) == 0:
            print("[ + ] Cancelled.")

            sys.exit(1)

        return dpath

    @classmethod
    def _nix_rd_file(cls, self, title, mode, root, ext):
        dialog = Gtk.FileChooserDialog(title = title,
            action = Gtk.FileChooserAction.OPEN)

        for extension in ext:
            filter = Gtk.FileFilter()

            filter.add_pattern(extension[1])
            filter.set_name(' '.join([
                extension[0], '(' + extension[1] + ')'
            ]))

            dialog.add_filter(filter)

        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
        dialog.set_show_hidden(True)
        dialog.set_current_folder(root)

        if dialog.run() != Gtk.ResponseType.OK:
            print("[ + ] Cancelled.")

            sys.exit(1)

        fpath = dialog.get_filename()

        dialog.hide()

        return open(fpath, mode)

    @classmethod
    def _nix_sel_dir(cls, self, title, root):
        dialog = Gtk.FileChooserDialog(title = title,
            action = Gtk.FileChooserAction.SELECT_FOLDER)

        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
        dialog.set_show_hidden(True)
        dialog.set_current_folder(root)

        if dialog.run() != Gtk.ResponseType.OK:
            print("[ + ] Cancelled.")

            sys.exit(1)

        fpath = dialog.get_filename()

        dialog.destroy()

        return fpath

def pad(line, lvl = 1):
    return (INDENT_CHAR * (INDENT * lvl)) + line

def bufsz(buf):
    return len(buf.getvalue())

def qual_classlist(path, recurse = False):
    for clazz in classlist(path, recursive = recurse):
        if is_valid_class(clazz):
            yield clazz

def get_class_names(path, recurse = False):
    for clazz in SmaliClass.iter_dir(path, recurse):
        yield clazz.name

def get_smali_dir(args):
    return os.path.join(args.gg_src, 'smali')

def classlist(path, recursive = False):
    query = '**/*.smali' if recursive else '*.smali'

    return glob.glob(path + os.sep + query,
                            recursive = recursive)

def get_pkg_dir(args):
    smali_dir = os.path.join(args.gg_src, 'smali')

    return os.path.join(smali_dir, args.pkg)

def type_from_ref(reference):
    return reference.split('->')[0]

def item_from_ref(reference):
    return reference.split('->')[1]

def get_method_sig(method):
    return re.match("\\.method.*\\s([A-Za-z0-9_<>]+\\.*\\.+)$", method)[1]

def get_field_sig(field):
    if isinstance(field, list):
        field = field[0] # extract the header

    match = re.match("\\.field.*\\s([A-Za-z0-9_]+:.*)$")

    return re.sub("\\s+=\\s+0x[-0-9-a-f]+$", '', match[1]).strip()

def get_apk_marker_path(args):
    smali_dir = os.path.join(args.gg_src, 'smali')

    return os.path.join(smali_dir, 'bcmarker.smali')

def is_gzipped(buf):
    gzip_magic = b'\x1f\x8b'
    old_pos = buf.tell()

    buf.seek(0)

    for i in range(len(gzip_magic)):
        byte = buf.read(1)[0]

        if byte != gzip_magic[i]:
            return False

    buf.seek(old_pos)

    return True

# attempt to select proguarded classes only
def is_valid_class(filename):
    name = os.path.basename(filename[:filename.rfind('.smali')])
    check_1 = len(name) <= MAX_FILENAME_THRESHOLD
    check_2 = name.islower()

    return (check_1 and check_2)

def file_filter(parent, file):
    name = file[:file.rfind('.smali')]

    if is_valid_class(os.path.basename(file)):
        return FileIO(os.path.join(parent, file), 'r+')

    return None

def valid_dir(parent, files):
    if not os.path.isdir(parent):
        print("[ - ] Can't use package '%s'. Is a file." % parent)

        sys.exit(1)

    if parent.endswith('/smali') or parent.endswith('/smali/.'):
        return True

    return len(files) != 0

def valid_pkg(args, pkg_dir):
    if not os.path.exists(pkg_dir):
        print("[ - ] Can't use package '%s'. Does not exist." % pkg_dir)

        sys.exit(1)

    if not valid_dir(pkg_dir, classlist(pkg_dir)):
        return False

    script_sz = bufsz(args.script)
    class_count = len(classlist(pkg_dir, recursive = True))

    return ((class_count - 
                math.ceil(script_sz / MAX_CHARS_PER_FILE)) >= 0)