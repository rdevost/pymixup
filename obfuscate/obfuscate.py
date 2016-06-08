from __future__ import print_function, with_statement
from os.path import join, isdir
from distutils.dir_util import mkpath
from time import time, ctime

from fabric.api import local, settings, lcd

from common.settings import imported_dir, project_name, obfuscated_dir
from data.builddb import build_db
from import_project.fabfile import import_proj
from logic.obfuscatefile import ObfuscatePythonBNF, ObfuscateKivyBNF, \
    obfuscate_file
from logic.reserved import search_reserveds
from logic.identifier import get_obfuscated_name, search_identifiers
from logic.utilities import file_gen, obfuscate_path


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
def obfuscate(platform='default', is_rebuild=True, is_verbose=True,
              do_import=False):
    """Obfuscate a python project.

    Create a project in the OBFUSCATED directory for the destination platform.
    This project directory will have three subdirectories:

        1. obfuscated. This has files and packages specified in the
            common/settings.py obfuscated_packages and obfuscated_root_files
            lists.
        2. unobfuscated. This has a complete copy of the project in the
            IMPORTED directory.
        3. db. This contains a copy of the Reserved and Identifier tables.

    Parameters
    ----------
    platform : str
        The destination platform.

    is_rebuild : bool
        Don't rebuild the dictionary. That is, keep all the previously
        assigned variable names, but check for new names and changes in
        reserved names. The default is to rebuild the dictionary.

    is_verbose : bool
        Print verbose messages.

    do_import : bool
        Import source if True.
    """
    start_time = time()
    print('***PYMIXUP started at {}'.format(ctime(start_time)))

    if do_import:
        import_proj()

    # Setup directories
    from_dir = join(imported_dir, project_name, 'to_obfuscate')
    to_dir = join(obfuscated_dir, project_name, platform)
    # db is built in OBFUSCATED/<project_name>, not in the <platform>
    # subdirectory, because it must exist (for builddb.py) before the
    # parameters are loaded.
    db_dir = join(obfuscated_dir, project_name, 'db')

    # Create/clear the obfuscated folders and db
    clear_source(to_dir, db_dir, is_rebuild=is_rebuild)

    # Add/refresh reserved names
    build_db(db_dir)

    bnf_python_parser = ObfuscatePythonBNF(get_obfuscated_name)
    bnf_kivy_parser = ObfuscateKivyBNF(get_obfuscated_name)
    # Run multiple times; first, run as often as needed to populate obfuscated
    # db with identifiers and reserved names, then run a final time to
    # obfuscate the source.
    num_runs = 0
    num_reserved = 0
    num_identifiers = 0

    discovery_phase = [True, False]
    for is_discovery in discovery_phase:
        do_transform = not is_discovery
        while is_discovery or do_transform:
            num_runs += 1
            if is_discovery:
                num_reserved = search_reserveds(None).count()
                num_identifiers = search_identifiers(None).count()

            print('***PREPROCESSING***' if is_discovery
                  else '***OBFUSCATING***')
            for file_name, dir_name, is_reserved_dir, is_reserved_file, \
                    do_obfuscate in file_gen(from_dir):
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
                                   to_dir=None if is_discovery
                                   else join(to_dir, 'obfuscated'),
                                   is_verbose=is_verbose,
                                   is_discovery=is_discovery,
                                   is_python=file_name[-3:] == '.py',
                                   do_obfuscate=do_obfuscate,
                                   platform=platform)
                    print('obfuscated')
                else:
                    if not is_discovery:
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
            if is_discovery:
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
                    is_discovery = False
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


def clear_source(to_dir, db_dir, is_rebuild=True):
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
