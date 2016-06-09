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

Use Fabric tasks to facilitate the steps
========================================
These Fabric tasks have been set up (they're described below):

    - **import_proj** in the file *import_project/fabfile.py*
    - **obfuscate_proj** in the file *obfuscate/fabfile.py*
    - **export_proj** in the file *export/fabfile.py*
    - **save_deployed** in the file *deploy/fabfile.py*

A Fabric task is run like this::

    fab --fabfile=<relative path to fabfile> <method to run>:<parm1>=<value1>,<parm2>=<value2>,...

For example, to run the **export_proj** method in the fabric file **export/fabfile.py** with parameter **platform** set to "android" and the parameter **do_obfuscate** set to True::

    fab --fabfile=export/fabfile.py export_proj:platform=android,do_import=True

Import a development project
============================
The import task copies files from your development project into the folders *pymixup* uses to obfuscate.

This task copies the source from <MyProject> into **IMPORTED/<MyProject>**. It must be run every time a source code change is made in your project::

    $ fab --fabfile=import_project/fabfile.py import_proj

Obfuscate the project
=====================
The obfuscate task obfuscates the source code. This will:

    - Discover all names used in the project and assign them obfuscated values. These will be stored in an SQLite database.
    - Obfuscate the source and write it to the folder **OBFUSCATED/<MyProject>/<platform>/obfuscated**.
    - Put a copy of the unobfuscated source in **OBFUSCATED/<MyProject>/<platform>/unobfuscated**.
    - Save a copy of the names database in **OBFUSCATED/<MyProject>/obfuscated/<platform>/db**.

    For more information on the directories, see :doc:`folder-structure`.

---------------
Task parameters
---------------
    **platform**
        - A string for the destination platform. For example, "android" or "ios".
        - This will be used to apply the platform directives.
        - If no platform is specified, "default" will be used.

    **do_rebuild**
        - Rebuild the identifiers and reserved name tables. Can be "True" or "False".
        - If set to False, existing obfuscated identifiers and reserved names will retain their prior randomized names. New identifiers and reserved names may be be added.
        - Default is to rebuild tables.

    **is_verbose**
        - Print verbose messages. Can be "True" or "False".
        - Default is to print verbose messages.

    **do_import**
        - Run the **import_proj** task before obfuscating. Can be "True" or "False".
        - Default is False.

--------
Examples
--------
   To obfuscate with all the defaults::

        $ fab --fabfile=obfuscate/fabfile.py obfuscate_proj

   To obfuscate for the Android platform while retaining the existing Identifier dictionary (that is, not rebuilding the dictionary from scratch)::

        $ fab --fabfile=obfuscate/fabfile.py obfuscate_proj:platform=android,do_rebuild=False

    Use the **do_import** parameter to run the **import_project** step beforehand::

        $ fab --fabfile=obfuscate/fabfile.py obfuscate_proj:do_import=True

Export and test in your development platform
============================================
Part of setting up the project is to identify all the files, directories, and modules needed on the destination platform to run your project. Test this collection of files to make sure that everything needed has been identified.

Run the **export_proj** task to collect all the obfuscated code and other resources and copy them to the destination platform.

---------------
Task parameters
---------------
    **platform**
        - A string for the destination platform. For example, "android" or "ios".
        - This will be used to apply the platform directives.
        - If no platform is specified, "default" will be used.

    **do_obfuscate**
        - Run the **obfuscate_proj** task before exporting. Can be "True" or "False".
        - Defaults to False.

    **do_import**
        - Run the **import_proj** task before running the **do_obfuscate** task. Can be "True" or "False".
        - This parameter is disregarded if **do_obfuscate** is False.
        - Defaults to False.

    **do_rebuild**
        - Rebuild the Reserved and Identifier tables if when obfuscating.
        - This parameter is disregarded if **do_obfuscate** is False.
        - Defaults to True.

    **is_verbose**
        - Print verbose messages while obfuscating.
        - This parameter is disregarded if **do_obfuscate** is False.
        - Defaults to True.

    **do_copy_obfuscated**
        - Create an obfuscated project in the EXPORTED/obfuscated directory.
        - If set to false, an unobfuscated project will be created there.
        - This could be helpful if the destination platform is configured to use only one directory. For example, if an iOS Xcode environment is setup to rebuild when it discovers changes in .../EXPORTED/obfuscated, then set **do_copy_obfuscated** to False to test unobfuscated code on iOS devices.
        - WARNING: Set this to False only for special cases. Then re-export your project with the default of True.
        - Default is True (export the obfuscated project).


-----
Steps
-----
    1. Run the **export_proj** task to create full obfuscated and unobfuscated projects in **EXPORTED/<MyProject>/<platform>**.
    2. Run the unit tests in the unobfuscated project folder EXPORTED/<MyProject>/<platform>/unobfuscated.
    3. After successfully completing the unobfuscated unit tests, run the unit test in the obfuscated folder. These tests are the most valuable resource to discover names that were obfuscated that should not have been.

    For example, to export for the Android platform::

        $ fab --fabfile=export/fabfile.py export_proj:platform=android

    Use the **do_import** and **do_obfuscate** parameters to run the **import_project** and **obfuscate_proj** tasks beforehand::

        $ fab --fabfile=export/fabfile.py export_proj:platform=android,do_obfuscate=True,do_import=True

Export and test on the destination platform
===========================================
Once testing is successful for the obfuscated project on the development platform, copy it into the destination platform and test it there.

1. Copy and test the unobfuscated project on the destination platform.
2. Copy and test the obfuscated project on the destination platform.

NOTE: If the unobfuscated build works, but the obfuscated does not, it is very likely due to a keyword that was obfuscated that should not have been. Often, the traceback will tell you which name is at fault.

Deploy the obfuscated project
=============================
Once a build is submitted as a release, run **deploy/fabfile.py/save_deployed(platform=<platform>)** to keep a copy of the original source, the obfuscated source, and the database of reserved names and identifiers. This option will ask for a version number, which will be used to create a folder under **DEPLOYED/<MyProject>/<platform>/<version number>**.

    For example, to deploy an exported iOS project with version number 1.2.1a::

        $ fab --fabfile=deploy/fabfile.py save_deployed:platform=ios

    You will be prompted for the version number. Enter the version number and the project files will be saved.
