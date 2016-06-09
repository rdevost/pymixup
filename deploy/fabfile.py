from __future__ import with_statement
from fabric.api import lcd, local, settings
from os.path import join, isdir
from time import ctime, time

from common.settings import deployed_dir, exported_dir, project_name

try:
    input = raw_input  # For python 2.x
except NameError:
    pass


def save_deployed(platform='default'):
    """Save a deployed obfuscated project.

    Input values
    ------------
    version_num : str
        Version number of the deployed project.

    Parameters
    ----------
    platform : str
        Destination platform.
    """
    print('***DEPLOY started at {}'.format(ctime(time())))
    version_num = input(
        'Version number to save to. Don\'t use parens, like 1.2(a). '
        'Use just numbers, letters, and dots, like: 1.2.4a.: ')

    from_base_dir = join(exported_dir, project_name, platform)
    to_base_dir = join(deployed_dir, project_name, platform, str(version_num))

    if isdir(to_base_dir):
        resp = None
        while not resp:
            resp = input('Directory {} already exists. Delete it (y/n): '
                         .format(to_base_dir)).lower()
            if resp not in ['y', 'n']:
                resp = None
        if resp == 'y':
            with settings(warn_only=True):
                result = local(' '.join(['rm -r', to_base_dir]))
                if result.return_code <= 1:
                    pass
                else:
                    print(result)
                    raise SystemExit()
        else:
            quit()

    local(' '.join(['mkdir', to_base_dir]))
    local(' '.join(['mkdir', join(to_base_dir, 'obfuscated')]))
    local(' '.join(['mkdir', join(to_base_dir, 'unobfuscated')]))
    local(' '.join(['mkdir', join(to_base_dir, 'db')]))

    # Copy obfuscated program
    with lcd(join(to_base_dir, 'obfuscated')):
        local(' '.join(['cp -R', join(from_base_dir, 'obfuscated', '*'), '.']))

    # Copy unobfuscated program
    with lcd(join(to_base_dir, 'unobfuscated')):
        local(' '.join(['cp -R',
                        join(from_base_dir, 'unobfuscated', '*'), '.']))

    # Copy db
    with lcd(join(to_base_dir, 'db')):
        local(' '.join(['cp -R', join(from_base_dir, 'db', '*'), '.']))

    print('***DEPLOY ended at {}'.format(ctime(time())))
    return True
