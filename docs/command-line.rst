====================
Command Line Options
====================

The pymixup.py program can be run from the command line. For example, to obfuscate the project specified in **common/settings.py** with all new obfuscated names, enter::

    $ python pymixup.py --norebuild

Parameters
==========
All parameters must be preceded by a double dash. Some parameter may use a supplied value (as in the brackets (<>) below).

    **platform <platform name>**

    - The destination platform.
    - This will be used to apply the platform directives.
    - Optional.
    - Example::

        $ python pymixup.py --platform android

    **norebuild**

    - Do not rebuild the identifiers and reserved name tables.
    - If specified, existing obfuscated identifiers and reserved names will retain their prior randomized names. New identifiers and reserved names may be be added.
    - Default is to rebuild tables.
    - Example::

        $ python pymixup.py --norebuild

    **verbose**

    - Print verbose messages.
    - Optional.
    - Example::

        $ python pymixup.py --verbose

    **doimport**

    - Import source files before obfuscating.
    - Optional.
    - Example::

        $ python pymixup.py --doimport

Fabric automated tasks
======================
The import, export, and deploy tasks are automated using Fabric. See :doc:`steps` for a description of their use.
