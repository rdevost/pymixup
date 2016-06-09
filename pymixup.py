from __future__ import print_function, with_statement
import argparse

from obfuscate import obfuscate


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
    platform: The destination platform.

    norebuild: Don't rebuild the dictionary. That is, keep all the previously
        assigned variable names, but check for new names and changes in
        reserved names. The default is to rebuild the dictionary.

    notverbose: Do not print verbose messages.
    doimport: Import source.
    """
    # Set command line parameters
    parser = argparse.ArgumentParser(description='Obfuscate source files.')
    parser.add_argument(
        '--platform',
        dest='platform',
        help='destination platform',
        required=False)
    parser.add_argument(
        '--norebuild',
        action='store_true',
        help='add/refresh identifier names',
        required=False)
    parser.add_argument(
        '--notverbose',
        action='store_true',
        help='print verbose messages',
        required=False)
    parser.add_argument(
        '--doimport',
        action='store_true',
        help='import source',
        required=False)

    # Parse the command line
    args = parser.parse_args()

    # Obfuscate project
    obfuscate(platform=args.platform if args.platform else 'default',
              do_rebuild=not args.norebuild,
              is_verbose=not args.notverbose)


if __name__ == '__main__':
    main()
