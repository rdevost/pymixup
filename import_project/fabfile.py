from __future__ import with_statement
from fabric.api import lcd, local, settings
from os.path import join
from time import ctime, time

from common.settings import imported_dir, obfuscated_packages, \
    obfuscated_root_files, project_base_dir, project_name, \
    unobfuscated_folders, unobfuscated_root_files


def import_proj():
    """Import development project for obfuscating.

    Returns
    -------
    True if successfully completed.
    """
    print('***IMPORT started at {}'.format(ctime(time())))
    from_dir = join(project_base_dir, project_name)
    to_dir = join(imported_dir, project_name)

    with settings(warn_only=True):
        result = local(' '.join(['rm -r', to_dir]))
        if result.return_code <= 1:
            pass
        else:
            print(result)
            raise SystemExit()

    local(' '.join(['mkdir', to_dir]))
    local(' '.join(['mkdir', join(to_dir, 'to_obfuscate')]))
    local(' '.join(['mkdir', join(to_dir, 'to_not_obfuscate')]))

    # Copy files to obfuscate from project root
    with lcd(join(to_dir, 'to_obfuscate')):
        print("Copying project root files to obfuscate")
        for root_file in obfuscated_root_files:
            local(' '.join(['cp', join(from_dir, root_file), '.']))

    # Copy packages to obfuscated
    with lcd(join(to_dir, 'to_obfuscate')):
        print("Copying packages to obfuscate")
        for package in obfuscated_packages:
            local(' '.join(['cp -R', join(from_dir, package), '.']))

    # Copy unobfuscated files to project root
    with lcd(join(to_dir, 'to_not_obfuscate')):
        print("Copying project root files that are not obfuscated")
        for root_file in unobfuscated_root_files:
            local(' '.join(['cp', join(from_dir, root_file), '.']))

    # Copy folders that are not obfuscated
    with lcd(join(to_dir, 'to_not_obfuscate')):
        print("Copying folders that are not obfuscated")
        for folder in unobfuscated_folders:
            local(' '.join(['cp -R', join(from_dir, folder), '.']))

    print('***IMPORT ended at {}'.format(ctime(time())))
    return True
