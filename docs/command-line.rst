====================
Command Line Options
====================

The pymixup.py program can be run from the command line. For example, to obfuscate the project specified in **common/settings.py** with all new obfuscated names, enter::

    $ python pymixup.py --rebuild

Parameters
==========
All parameters must be preceded by a double dash. Some parameter may use a supplied value (as in the brackets (<>) below).

    **norecurs**

    - Include this parameter to NOT process the base directory recursively. That is, don't process the subdirectories.
    - Example::

        $ python pymixup.py --norecurs

    **platform <platform name>**

    - The destination platform.
    - This will be used to apply the platform directives.
    - Optional.
    - Example::

        $ python pymixup.py --platform android

    **rebuild**

    - Rebuild the identifiers and reserved name tables.
    - If not specified, existing obfuscated identifiers and reserved names will retain their prior randomized names. New identifiers and reserved names may be be added.
    - Example::

        $ python pymixup.py --rebuild

    **addidents**

    - Search for and add new identifiers or reserved names.
    - If the --rebuild parameter is specified, then this parameter is irrelevant, since the tables will be completely rebuilt.
    - Use this option when you do not want to keep the prior obfuscated name assignments but have added new names or changed some to reserved.
    - Example::

        $ python pymixup.py --addidents

    **verbose**

    - Print verbose messages.
    - Optional.
    - Example::

        $ python pymixup.py --verbose

Fabric automated tasks
======================
The import, export, and deploy tasks are automated using Fabric. See :doc:`steps` for a description of their use.
