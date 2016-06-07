============
Program Flow
============
*pymixup* will read a Python project and create a corresponding obfuscated project by using the following steps.

Initially load the reserved names list
======================================
It executes data/builddb.py to initially populate the **Identifier** (which contains all the names in a project that should be obfuscated plus their obfuscated values) and **Reserved** (which contains all the names that are reserved and should not be obfuscated) tables with names that you specified should not be obfuscated.

Discover all names used in the project
======================================
*pymixup* will read through the project files and finish loading the Identifier and Reserved tables. This is done as follows.

1. Examine every non-string and non-comment name in the Python programs and add it to either Reserved or Identifier. Note that this will run repeatedly until no new names are added or moved between tables. This step uses the following logic::

    if the name is a reserved name
    or is imported from a reserved package
    or is an attribute of a reserved name
        add it to Reserved (if it isn't already there)
        if the name is in Identifier
            unobfuscate it (by changing it's obfuscated value to its real name)
        else
            add it to Identifier without obfuscation
    else
        obfuscate it and add it to Identifier

2. Each name is obfuscated by assigning it a randomly-generated name based on the allowed letters to use (specified in ALPHABET in logic/randomizename.py) and a name length (specified when calling the randomizer in logic/identifier.py). The length of obfuscated words and what characters are allowed for them can be changed there.
3. Every file and folder name that is not reserved will be obfuscated as well.

Obfuscate the project
=====================
After discovering all the names used in a project, *pymixup* will read through the project files again and create obfuscated versions based on the generated Identifier table (from above).

1. Comments and doc strings will be stripped out of the obfuscated files.
2. Line breaks will be removed, so that each python statement will be on a single line, regardless of its length.
3. Each name defined in Identifier (above) will be replaced with its obfuscated counterpart.