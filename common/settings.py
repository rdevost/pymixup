from os.path import expanduser


######################
# Common project files
######################
# These are files, packages, and folders that will be copied from the
# development folder to the destination obfuscated project.
######################

# Python packages to obfuscate.
obfuscated_packages = [
    'controller',
    'db',
    'dbdata',
    'logic',
    'migrations',
    'platform_api',
    'tests',
    'view'
    ]

# Non-python folders and Python packages that are not obfuscated.
# Note: Tests are a special case: both obfuscated and unobfuscated versions
#       are desired.
unobfuscated_folders = [
    'csvlite',
    'fonts',
    'help',
    'images', 'initial_data', 'international',
    'kivygraph',
    'tests',
    ]

# Required files or types in the project directory (that is, the base
# directory in which all the common packages exist in) that must be
# obfuscated. For example, main.py is not in any of the common packages, but
# should be obfuscated and included in the project, so *.py (or alternatively,
# main.py) is included here.
obfuscated_root_files = [
    '*.kv',
    '*.py',
    ]

# Required files or types in the project directory that should not be
# obfuscated.
unobfuscated_root_files = [
    '*.ini',
    '*.txt',
    ]

#####################
# Default directories
#####################
# A project is moved through directories as follows:
#    1. It is copied into IMPORTED (use import_project/fabfile.py).
#    2. The IMPORTED project is obfuscated and written into OBFUSCATED (run
#       pymixup.py).
#    3. When an obfuscated project is ready to test, it is copied into
#       EXPORTED for a particular platform (e.g., for ios, use
#       export_ios/fabfile.py).
#       If no platform is specified, it will be copied into a folder called
#       "default".
#    4. When an exported project is deployed, it is copied into DEPLOYED under
#       its version number.
#
# Note that files in IMPORTED, OBFUSCATED, and EXPORTED are overwritten with
# each refresh from the development project. When a project is deployed,
# however, a permanent copy is retained under its version number.
#####################

# Project name. This should be the name of the last folder in the project
# path. The name is appended to the directories below.
project_name = 'MyProject'

# The base directory of the project to obfuscate.
# For example, the base directory of a project in '~/projects/MyProject' would
# be '~/projects'
project_base_dir = expanduser('~/PycharmProjects')

# The directory to copy the imported development project files to.
# Make sure this base directory exists; the fabfile scripts expects it.
# The project_name will be appended to the directory.
# For example, specify '~/projects/IMPORTED' to have the files from the
# project MyProject copied into '~/projects/IMPORTED/MyProject'.
imported_dir = expanduser('~/projects/IMPORTED')

# The directory to write the obfuscated files to.
# Make sure this base directory exists; the fabfile scripts expects it.
# The project_name and platform will be appended to the directory.
# For example, if '~/projects/OBFUSCATED' is specified, then the project
# MyProject obfuscated for the android platform will be placed in
# '~/projects/OBFUSCATED/MyProject/android'.
obfuscated_dir = expanduser('~/projects/OBFUSCATED')

# The directory to write the exported files to.
# Make sure this base directory exists; the fabfile scripts expects it.
# The project_name and platform will be appended to the directory.
# For example, if '~/projects/EXPORTED' is specified, then the project
# MyProject exported for the android platform will be placed in
# '~/projects/EXPORTED/MyProject/android'.
exported_dir = expanduser('~/projects/EXPORTED')

# The directory to write the exported files to.
# Make sure this base directory exists; the fabfile scripts expects it.
# For example, if '~/projects/EXPORTED' is specified, then the project
# MyProject deployed for the android platform for version 1.3.2 will be placed
# in '~/projects/DEPLOYED/MyProject/android/1.3.2'.
deployed_dir = expanduser('~/projects/DEPLOYED')

# The directory that contains extra files and folders needed for the project.
extras_dir = expanduser('~/project/EXTRAS')
