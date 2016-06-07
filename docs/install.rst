============
Installation
============

Requirements
============
**Python 2.7x**
    *pymixup* uses Fabric to automate tasks, and Fabric has not (yet) migrated to Python 3. This is *pymixup's* only known requirement for Python 2.7x. When (if) Fabric is updated to use Python 3.x, *pymixup* should run on Python 3.x.

**Fabric**
    Used to automate tasks to prepare files for obfuscation and to deploy obfuscated code.

**pyparsing**
    Used to parse Python and Kivy code.

**peewee**
    Used as the ORM for the Sqlite db that contains the reserved (unobfuscated) and obfuscated names in the project.

**pytest**
    Used as the unit testing framework.

Installation
============
pip ...

If running pytest from the command line, then set an environment variable IS_PYMIXUP_TEST=1 for the tests. For example, in Linux::

    export IS_PYMIXUP_TEST=1
    py.test

This environment variable is used to determine whether to use the live on-disk database Reserved and Identifier tables or set up temporary testing in-memory ones.
