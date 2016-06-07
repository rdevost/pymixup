from os import walk, sep
from os.path import basename, normpath, join
from peewee import DoesNotExist

from logic.reserved import get_reserved_by_name, add_reserveds, \
    reserved_prefixes
from logic.identifier import add_identifiers


def file_gen(from_dir, do_recursive=True, file_name=None):
    """Process a file or directory.

    Parameters
    ----------
    do_recursive : bool
    file_name : str
    from_dir : str

    Yields
    ------
    dir_name : str
    do_obfuscate : bool
    file_name : str
    is_reserved_dir : bool
    is_reserved_file : bool
    """
    # Process for a single file
    if file_name:
        # Skip excluded files
        is_reserved_dir = None
        try:
            get_reserved_by_name(''.join([
                reserved_prefixes.reserved_file, file_name]))
        except DoesNotExist:
            is_reserved_file = False
        else:
            is_reserved_file = True

        yield file_name, from_dir, is_reserved_dir, is_reserved_file
        return

    # Process for a directory
    for dir_name, subdir_list, file_list in walk(from_dir):
        if do_recursive and not dir_name:
            break
        # Remove unwanted files from file_list
        file_list = [file_name for file_name in file_list
                     if file_name[-4:] not in ['.pyc', '.pyo']
                     ]
        #####################
        # Process directories
        #####################
        is_reserved_dir = True
        do_obfuscate_dir = False

        # Identify reserved directories
        try:
            reserved_row = get_reserved_by_name(
                ''.join([reserved_prefixes.reserved_dir, basename(dir_name)]))
        except DoesNotExist:
            is_reserved_dir = False
        else:
            # Add identifiers to reserved
            if subdir_list:
                add_reserveds(reserved_row.primary_package, subdir_list,
                              reserved_prefixes.reserved_dir)
            if file_list:
                add_reserveds(basename(dir_name), file_list,
                              reserved_prefixes.reserved_file)

        # Identify non-obfuscated directories
        if not is_reserved_dir:
            try:
                get_reserved_by_name(''.join([
                    reserved_prefixes.non_obfuscated_dir, basename(dir_name)]))
            except DoesNotExist:
                do_obfuscate_dir = True

                # Add to obfuscated identifiers
                add_identifiers(basename(dir_name))
                if subdir_list:
                    add_identifiers(subdir_list)
                if file_list:
                    ob_files = [
                        file_name[:-3] for file_name in file_list
                        if file_name[-3:] in ['.py', '.ky']
                        ]
                    if ob_files:
                        add_identifiers(ob_files)
            else:
                # Add non-obfuscated identifiers
                add_identifiers([basename(dir_name)], do_obfuscate=False)
                if subdir_list:
                    add_reserveds(basename(dir_name), subdir_list,
                                  reserved_prefixes.non_obfuscated_dir)
                if file_list:
                    add_reserveds(basename(dir_name), file_list,
                                  reserved_prefixes.non_obfuscated_file)

        for file_name in file_list:
            do_obfuscate = False
            is_reserved_file = False
            # Files in reserved directory are reserved
            if is_reserved_dir:
                is_reserved_file = True
            else:
                # Identify reserved files
                try:
                    get_reserved_by_name(''.join([
                        reserved_prefixes.reserved_file, file_name]))
                except DoesNotExist:
                    # Identify files to obfuscate
                    if do_obfuscate_dir:
                        try:
                            get_reserved_by_name(''.join([
                                reserved_prefixes.non_obfuscated_file,
                                file_name]))
                        except DoesNotExist:
                            do_obfuscate = True
                else:
                    is_reserved_file = True

            if file_name == '__init__.py' and \
                    not is_reserved_dir and \
                    not do_obfuscate_dir:
                do_obfuscate = True

            yield file_name, dir_name, is_reserved_dir, is_reserved_file, \
                do_obfuscate


def split_path(file_path):
    """Split a path into its parts.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    path : list
    """
    return normpath(file_path).split(sep)


def obfuscate_path(file_path):
    """Create an obfuscated path name.

    Parameters
    ----------
    file_path : str

    Returns
    -------
    obfuscated path : str
    """
    from logic.identifier import get_obfuscated_name

    obf_path = [get_obfuscated_name(p) for
                p in normpath(file_path).split(sep)]

    if obf_path[-1][-3:] in ['.py', '.kv']:
        obf_path[-1] = ''.join([get_obfuscated_name(obf_path[-1][:-3]),
                                obf_path[-1][-3:]])

    return join(*obf_path)


def to_unicode(unicode_or_string):
    """Convert a string to unicode.

    Parameters
    ----------
    unicode_or_string : str  # or unicode

    Returns
    -------
    value : unicode
    """
    if isinstance(unicode_or_string, str):
        value = unicode_or_string.decode('utf-8')
    else:
        value = unicode_or_string
    return value


def to_str(unicode_or_str):
    """Convert a string to unicode.

    Parameters
    ----------
    unicode_or_str : unicode  # or str

    Returns
    -------
    value : str
    """
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value
