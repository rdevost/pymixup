from __future__ import print_function, with_statement
import argparse
from os.path import join, isfile, isdir
from distutils.dir_util import mkpath
from time import time, ctime

from fabric.api import local, settings, lcd

from common.settings import imported_dir, project_name, obfuscated_dir
from data.builddb import build_db
from logic.obfuscate import ObfuscatePythonBNF, ObfuscateKivyBNF, \
    obfuscate_file
from logic.reserved import search_reserveds
from logic.identifier import get_obfuscated_name, search_identifiers
from logic.utilities import file_gen, obfuscate_path

__version__ = '1.0.2'


###############################
# Directories and files to skip
###############################
skip_directories = [
    '.idea',
    '.git'
    ]

skip_files = [
    '.DS_Store'
    ]


#####################
# Obfuscate a project
#####################
def main():
    """Obfuscate a python project.

    Create a project in the OBFUSCATED directory for the destination platform.
    This project directory will have three subdirectories:

        1. obfuscated. This has files and packages specified in the
            common/settings.py obfuscated_packages and obfuscated_root_files
            lists.
        2. unobfuscated. This has a complete copy of the project in the
            IMPORTED directory.
        3. db. This contains a copy of the Reserved and Identifier tables.

    System arguments
    ----------------
    from: The base directory for the source project. If specified, this overrides
        the default value specified in common/settings.py.

    to: The base directory to copy the obfuscated project to. If specified,
        this overrides the default value specified in common/settings.py.

    file: Obfuscate just this file. If specified, only this file will be
        removed and rebuilt in --to directory (or its default).

    norecurs: Include this parameter to NOT process the base directory
        recursively. That is, don't process the subdirectories.

    platform: The destination platform.

    rebuild: Rebuild the identifiers and reserved name tables. If not
        specified, existing obfuscated identifiers and reserved names will
        retain their prior randomized names. New identifiers and reserved names
        may be be added.

    addidents: Search for and add new identifiers or reserved names. If the
        --rebuild parameter is specified, then this parameter is irrelevant,
        since the tables will be completely rebuilt. Use this option when you
        do not want to keep the prior obfuscated name assignments but have
        added new names or changed some to reserved.

    verbose: Print verbose messages.
    """
    # Set command line parameters
    parser = argparse.ArgumentParser(description='Obfuscate source files.')
    parser.add_argument(
        '--norecurs',
        action='store_false',
        help='process directory recursively to include subdirectories',
        required=False)
    parser.add_argument(
        '--platform',
        dest='platform',
        help='destination platform',
        required=False)
    parser.add_argument(
        '--rebuild',
        action='store_true',
        help='rebuild the obfuscate dictionaries',
        required=False)
    parser.add_argument(
        '--addidents',
        action='store_true',
        help='add/refresh identifier names',
        required=False)
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='print verbose messages',
        required=False)

    start_time = time()
    print('***PYMIXUP started at {}'.format(ctime(start_time)))

    # Parse the command line
    args = parser.parse_args()

    # Setup directories
    from_dir = join(imported_dir, project_name, 'to_obfuscate')
    to_dir = join(obfuscated_dir,
                  project_name,
                  args.platform if args.platform else 'default')
    # db is built in OBFUSCATED/<project_name>, not in the <platform>
    # subdirectory, because it must exist (for builddb.py) before the
    # parameters are loaded.
    db_dir = join(obfuscated_dir, project_name, 'db')

    # Create/clear the obfuscated folders and db
    if args.rebuild or args.addidents:
        clear_source(to_dir, db_dir, is_rebuild=args.rebuild)

    # Add/refresh reserved names
    if args.rebuild or args.addidents or not isfile(join(db_dir,
                                                         'obfuscated.db')):
        build_db(db_dir)

    bnf_python_parser = ObfuscatePythonBNF(get_obfuscated_name)
    bnf_kivy_parser = ObfuscateKivyBNF(get_obfuscated_name)
    # Run multiple times; first, run as often as needed to populate obfuscated
    # db with identifiers and reserved names, then run a final time to
    # obfuscate the source.
    num_runs = 0
    num_reserved = 0
    num_identifiers = 0

    if args.rebuild or args.addidents:
        pre_process = [True, False]
    else:
        pre_process = [False]
    for is_preprocess in pre_process:
        do_transform = not is_preprocess
        while is_preprocess or do_transform:
            num_runs += 1
            if is_preprocess:
                num_reserved = search_reserveds(None).count()
                num_identifiers = search_identifiers(None).count()

            print('***PREPROCESSING***' if is_preprocess
                  else '***OBFUSCATING***')
            for file_name, dir_name, is_reserved_dir, is_reserved_file, \
                    do_obfuscate in file_gen(from_dir,
                                             do_recursive=not args.norecurs):
                if len(dir_name) > len(from_dir):
                    from_sub_dir = dir_name[len(from_dir)+1:]
                else:
                    from_sub_dir = ''
                print(join(dir_name, file_name), end=' ... ')

                # Skip selected directories and files
                if from_sub_dir in skip_directories:
                    print('skipped')
                    continue
                if file_name in skip_files:
                    print('skipped')
                    continue

                if not is_reserved_file and file_name[-3:] in ['.py', '.kv']:
                    obfuscate_file(bnf_python_parser if file_name[-3:] == '.py'
                                   else bnf_kivy_parser,
                                   file_name,
                                   from_dir=dir_name,
                                   from_sub_dir=from_sub_dir,
                                   to_dir=None if is_preprocess
                                   else join(to_dir, 'obfuscated'),
                                   is_verbose=args.verbose,
                                   is_preprocess=is_preprocess,
                                   is_python=file_name[-3:] == '.py',
                                   do_obfuscate=do_obfuscate,
                                   platform=args.platform)
                    print('obfuscated')
                else:
                    if not is_preprocess:
                        if is_reserved_dir:
                            to_path = join(to_dir, 'obfuscated', from_sub_dir)
                        else:
                            to_path = join(to_dir, 'obfuscated',
                                           obfuscate_path(from_sub_dir))
                        if not isdir(to_path):
                            mkpath(to_path)
                        print('copied', end=' => ')
                        local(' '.join(['cp',
                                        join(dir_name, '"'+file_name+'"'),
                                        to_path]))
                    else:
                        print('reserved')
            if is_preprocess:
                # Continue preprocess if reserveds or identifiers added
                # Notes:
                #   1. Changes to reserveds always increase its number.
                #   2. Changes to identifiers will either add to identifiers
                #      or add to reserved if identifier is removed
                #   3. Therefore, any db changes have num record changes
                num_reserved_added = \
                    search_reserveds(None).count() - num_reserved
                num_identifiers_added = \
                    search_identifiers(None).count() - num_identifiers
                if not (num_reserved_added or num_identifiers_added):
                    is_preprocess = False
                print('===> Run number {}: Added {} reserved, {} identifiers'.
                      format(str(num_runs), str(num_reserved_added),
                             str(num_identifiers_added)))
            else:
                print('===> Finished. Run number {}: '.
                      format(str(num_runs)))
                # Copy unobfuscated source
                print('===> Copying unobfuscated source.')
                with lcd(join(to_dir, 'unobfuscated', 'to_obfuscate')):
                    local(' '.join(['cp -R', join(imported_dir,
                                                  project_name,
                                                  'to_obfuscate',
                                                  '*'), '.']))
                with lcd(join(to_dir, 'unobfuscated', 'to_not_obfuscate')):
                    local(' '.join(['cp -R', join(imported_dir,
                                                  project_name,
                                                  'to_not_obfuscate',
                                                  '*'), '.']))
                # Copy db dir
                print('===> Copying db.')
                with lcd(join(to_dir, 'db')):
                    local(' '.join(['cp -R', join(db_dir,
                                                  '*'), '.']))

            if do_transform:
                do_transform = False

    end_time = time()
    elapsed_minutes, elapsed_seconds = divmod(end_time - start_time, 60)
    print('***PYMIXUP ended at {}'.format(ctime(end_time)))
    print('===> Elapsed time: {} minutes, {} seconds'.format(
        int(elapsed_minutes), int(elapsed_seconds)))


def clear_source(to_dir, db_dir, is_rebuild=False):
    """Clear obfuscate destination folders.

    Parameters
    ----------
    to_dir : str
    db_dir : str
    is_rebuild : bool
    """
    with settings(warn_only=True):
        if is_rebuild:
            with settings(warn_only=True):
                local(' '.join(['rm -r', to_dir]))
                local(' '.join(['rm -r', db_dir]))
        else:
            with settings(warn_only=True):
                local(' '.join(['rm -r', join(to_dir, 'obfuscated')]))
                local(' '.join(['rm -r', join(to_dir, 'unobfuscated')]))
                local(' '.join(['rm -r', join(to_dir, 'db')]))

    if not isdir(to_dir):
        local(' '.join(['mkdir', to_dir]))
    if not isdir(db_dir):
        local(' '.join(['mkdir', db_dir]))
    local(' '.join(['mkdir', join(to_dir, 'obfuscated')]))
    local(' '.join(['mkdir', join(to_dir, 'unobfuscated')]))
    local(' '.join(['mkdir', join(to_dir, 'unobfuscated', 'to_obfuscate')]))
    local(' '.join(['mkdir', join(to_dir, 'unobfuscated',
                                  'to_not_obfuscate')]))
    local(' '.join(['mkdir', join(to_dir, 'db')]))

if __name__ == '__main__':
    main()
