from __future__ import with_statement
from fabric.api import local, settings, lcd
from os.path import join

from common.settings import obfuscated_dir, exported_dir, project_name, \
    extras_dir


def export(platform='default',
           do_import=False,
           do_obfuscate=False,
           do_copy_obfuscated=True):
    """Export obfuscated project for testing or deployment.

    Parameters
    ----------
    platform : str
        Destination platform.
    do_import : bool
        Run import_project fabfile if True.
    do_obfuscate : bool
        Run obfuscate fabfile if True.
    do_copy_obfuscated : bool
        Copy obfuscated files to EXPORT directory if '1', otherwise copy the
        unobfuscated files to allow testing the unobfuscated project on the
        destination platform. Testing the unobfuscated project on the
        destination assures that the project should run on that platform.

        WARNING: Changing the default of do_copy_obfuscated will put
        unobfuscated files in your destination EXPORT folder. Do this only if
        testing on your destination platform is tied to the 'obfuscated'
        folder. For example, if an iOS Xcode environment builds from
        'obfuscated'.
    """
    from_base_dir = join(obfuscated_dir, project_name, platform)
    to_base_dir = join(exported_dir, project_name, platform)

    if platform is 'android':
        extra_paths = [
            'bin',
            'buildozer.spec',
        ]
    elif platform is 'ios':
        extra_paths = [
            'docutils',
            'peewee.py',
            'pyparsing.py'
        ]
    elif platform is 'macosx':
        extra_paths = []
    else:  # default
        extra_paths = []

    if do_copy_obfuscated:
        print('***Exporting obfuscated {}'.format(platform))
    else:
        print('***WARNING: Exporting unobfuscated {}'.format(platform))

    with settings(warn_only=True):
        result = local(' '.join(['rm -r', to_base_dir]))
        if result.return_code <= 1:
            pass
        else:
            print(result)
            raise SystemExit()

    local(' '.join(['mkdir', to_base_dir]))
    local(' '.join(['mkdir', join(to_base_dir, 'obfuscated')]))
    local(' '.join(['mkdir', join(to_base_dir, 'unobfuscated')]))
    local(' '.join(['mkdir', join(to_base_dir, 'db')]))

    with lcd(join(to_base_dir, 'obfuscated')):
        #########################################################
        # Copy development project files to destination obfuscate
        #########################################################
        # First, copy needed unobfuscated files and folders
        local(' '.join(['cp -R', join(from_base_dir,
                                      'unobfuscated',
                                      'to_not_obfuscate', '*'), '.']))
        # Tests are both unobfuscated and obfuscated
        with settings(warn_only=True):
            # Remove unobfuscated tests (which have unobfuscated names)
            # from the obfuscated folder
            local(' '.join(['rm -r',
                            join(to_base_dir, 'obfuscated', 'tests')]))
        # Then, copy obfuscated files and packages
        if do_copy_obfuscated:
            local(' '.join(['cp -R',
                            join(from_base_dir, 'obfuscated', '*'), '.']))
        else:
            local(' '.join(['cp -R',
                            join(from_base_dir, 'unobfuscated',
                                 'to_obfuscate', '*'), '.']))

        #############
        # Copy extras
        #############
        # Copy common folders
        for extra_path in extra_paths:
            local(' '.join(['cp -R', join(extras_dir,
                                          extra_path), '.']))

        ########################
        # Remove other platforms
        ########################
        # Note: This assumes the project has a platform_api folder with
        #       specific api calls to that platform.
        #       Remove or disregard this block if that is not the case.
        ########################
        with settings(warn_only=True):
            if platform != 'android':
                local(' '.join(['rm -r', 'platform_api/android_api']))
            if platform != 'ios':
                local(' '.join(['rm -r', 'platform_api/ios_api']))
            if platform != 'macosx':
                local(' '.join(['rm -r', 'platform_api/macosx_api']))

    if do_copy_obfuscated:
        ####################################
        # Save a copy of unobfuscated source
        ####################################
        with lcd(join(to_base_dir, 'unobfuscated')):
            local(' '.join(['cp -R',
                            join(from_base_dir, 'unobfuscated',
                                 'to_obfuscate', '*'), '.']))
            local(' '.join(['cp -R',
                            join(from_base_dir, 'unobfuscated',
                                 'to_not_obfuscate', '*'), '.']))

        ###################
        # Copy obfuscate db
        ###################
        with lcd(join(to_base_dir, 'db')):
            local(' '.join(['cp -R', join(
                join(from_base_dir, 'db'), '*'), '.']))
