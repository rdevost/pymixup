============
Program Flow
============
*pymixup* reads a Python project and creates a corresponding obfuscated project by using the following steps.

Initially load the reserved names list
======================================
*pymixup* builds a database of all distinct names used in a project. The **Identifier** table contains all the names in a project plus their obfuscated values. The **Reserved** contains all the names that are reserved and should not be obfuscated. These tables are initially populated by a list of names you specify that should not be obfuscated.

Discover all names used in the project
======================================
*pymixup* then reads through the project files and finishes loading the Identifier and Reserved tables. This is done as follows.

1. Examine every non-string and non-comment name in the Python programs and add it to the Reserved and Identifier tables. This step uses the following logic::

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

2. Each name is obfuscated by assigning it a randomly-generated name based on allowed letters (specified in ALPHABET in logic/randomizename.py) and a name length (specified when calling the randomizer in logic/identifier.py). The length of obfuscated words and what characters are allowed for them can be changed there.
3. File and folder names that are not reserved are also obfuscated.

Obfuscate the project
=====================
After discovering all the names used in a project (which may require reading through the project files a few times), *pymixup* reads through the project files again and creates obfuscated versions using the Identifier table (from above). The obfuscated source files have:

1. Comments and doc strings removed.
2. Line breaks in Python statements removed, so each statement will be on a single line, regardless of its length.
3. Names changed to their obfuscated values.
