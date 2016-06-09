============================
Steps to Obfuscate a Project
============================
Obfuscating a project <MyProject> requires that:

1. The project files are copied into a working folder.
2. All unreserved variables, method names, modules names, and folder names are discovered and assigned new obfuscated names.
3. A new obfuscated version of the program is created.

The steps to accomplish this are described next, with an assumed name of <MyProject> for your project.

Setup the project
=================
Perform the setup steps described in :doc:`setup` to prepare the project.

Obfuscate the code
==================
Run the following two steps to create obfuscate your code. See :doc:`command-line` for run options.

1. Run **import_project/fabfile/import_proj()** to copy the source from <MyProject> into **IMPORTED/<MyProject>/project**. (This must be done every time a source code change is made in your project.)

    For example::

        $ fab --fabfile=import_project/fabfile.py import_proj

2. Run **obfuscate/fabfile/obfuscate()** (or **pymixup.py** from the command line) to obfuscate the source project. This will:

    - Discover all names used in the project and assign them obfuscated values. These will be stored in an SQLite database.
    - Obfuscate the source and write it to the folder **OBFUSCATED/<MyProject>/<platform>/obfuscated**.
    - Copy the unobfuscated source to **OBFUSCATED/<MyProject>/<platform>/unobfuscated**.
    - Save a copy of the names database in **OBFUSCATED/<MyProject>/obfuscated/<platform>/db**.

    For more information on the directories, see :doc:`folder-structure`.

    For example, to obfuscate for the Android platform with a complete rebuild of the Identifier dictionary::

        $ fab --fabfile=obfuscate/fabfile.py obfuscate:platform=android

    or, alternatively::

        $ python pymixup.py --platform android

    NOTE: If no --platform parameter is given, then the project will be copied into a folder called "default".

    The **obfuscate** fabric file can also run the **import_project** step beforehand by using a **do_import** parameter::

        $ fab --fabfile=obfuscate/fabfile.py obfuscate:platform=android,do_import=True

Export and test in your development platform
============================================
Part of setting up the project is to identify all the files, directories, and modules needed on the destination platform to run your project. Test this collection of files to make sure that everything needed has been identified.

1. Run **export/fabfile.py/deploy()** to create full obfuscated and unobfuscated projects in **EXPORTED/<MyProject>/<platform>**.
2. Run the unit tests for the unobfuscated project.
3. After successfully completing the unobfuscated unit tests, run the unit test for the obfuscated project. These tests are the most valuable resource to discover names that were obfuscated that should not have been.

    For example, to export for the Android platform::

        $ fab --fabfile=export/fabfile.py export:platform=android

    The **export** fabric file can also run the **import_project** and **obfuscate** steps beforehand by using the **do_import** and **do_obfuscate** parameters::

        $ fab --fabfile=export/fabfile.py export:platform=android,do_import=True,do_obfuscate=True

Export and test on the destination platform
===========================================
1. Copy and test the **unobfuscated** project on the destination platform.
    Note that you can use export/fabfile/deploy(do_copy_obfuscated=False) to create an unobfuscated project in the EXPORTED/obfuscated directory. This could be helpful if the destination platform is configured to use only one directory. For example, if an iOS Xcode environment is setup to rebuild when it discovers changes in .../EXPORTED/obfuscated, you can use the do_copy_obfuscated=False to test unobfuscated code on iOS devices.
2. Copy and test the **obfuscated** project on the destination platform.
3. If the unobfuscated build works, but the obfuscated does not, it is very likely due to a keyword that was obfuscated that should not have been. Often, the traceback will tell you which name is at fault.

Deploy the obfuscated project
=============================
Once a build is submitted as a release, run **deploy/fabfile.py/save_deployed(platform=<platform>)** to keep a copy of the original source, the obfuscated source, and the database of reserved names and identifiers. This option will ask for a version number, which will be used to create a folder under **DEPLOYED/<MyProject>/<platform>/<version number>**.

    For example, to deploy an exported iOS project with version number 1.2.1a::

        $ fab --fabfile=deploy/fabfile.py save_deployed:platform=ios

    You will be prompted for the version number. Enter the version number and the project files will be saved.
