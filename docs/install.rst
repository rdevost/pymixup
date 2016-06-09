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
*pymixup* should be installed in a development folder that you can edit. That is, it should not be installed in Python's site-packages directory. If you use virtual environments (in directory ~/virtualenv), an install in Unix could look like this::

    $ cd ~/virtualenv
    $ virtualenv pymixup
    $ pip install fabric pyparsing peewee pytest
    $ source pymixup/bin/activate
    $ cd ~/projects
    $ git clone git://github.com/rdevost/pymixup

Run pytests
===========
To running pytest from the command line, first set an environment variable IS_PYMIXUP_TEST=1. For example, in Unix::

    export IS_PYMIXUP_TEST=1
    cd pymixup
    py.test

This environment variable is used to determine whether to use the live on-disk database Reserved and Identifier tables or set up temporary testing in-memory ones.
