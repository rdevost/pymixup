=====
Setup
=====
The obfuscator uses a few lists and some extra files or packages to create the final project.

Identify the project files
==========================
*pymixup* needs to know which Python packages plus other files and directories make up the project. These are specified in the following **common/settings.py** lists.

    **obfuscated_packages**
        Your project's Python packages; that is, your source code packages. Note that for Kivy projects, this will automatically pick up the .kv files. Do not include Python standard libraries and libraries imported from site-packages in this list.
    **unobfuscated_folders**
        Non-python folders required by the project plus any Python packages copied into your project's root directory that should not be obfuscated. For example, a folder *fonts* of fonts could be in this list. Also, if a Python package like *peewee* is used in your project and is copied into your project root instead of using site-packages, then include it here too.
    **obfuscated_root_files**
        Required files that are in the project root folder that should be obfuscated. Use a wild card to specify the extension type. For example, "main.py" and "\*.kv".
    **unobfuscated_root_files**
        Required files that are in the project root folder that should not be obfuscated. Use a wild card to specify the extension type. For example, "\*.ini" and "setup.py".

Identify the obfuscation directories
====================================
The project's root directory and the working directories needed for obfuscating the project must also be specified. A project is obfuscated by using the following steps:

    1. It is imported into IMPORTED.
    2. The imported project is obfuscated and placed in OBFUSCATED.
    3. The obfuscated project is exported into EXPORTED for testing.
    4. The exported project is deployed into DEPLOYED.
    5. Extra files required for the deployed project will be copied from EXTRAS.

These are directories are defined in the following **common/settings.py** variables. (By default, the directories for these five steps end with /IMPORTED, /OBFUSCATED, /EXPORTED, /DEPLOYED, and /EXTRAS respectively, although this is not required. See :doc:`folder-structure` for a graphic of the directory tree.)

    **project_name**
        The root directory of the project. For example, the **project_name** for a project ~/projects/MyProject would be "MyProject".
    **project_base_dir**
        The directory which contains the root directory of the development project. For example, the **project_base_dir** for project ~/projects/MyProject would be "~/projects".
    **imported_dir**
        The working directory that the development project will be imported into.
    **obfuscated_dir**
        The working directory the obfuscated project will be placed in.
    **exported_dir**
        The directory to hold obfuscated projects that are ready to test.
    **deployed_dir**
        The directory to deploy the obfuscated project to.
    **extras_dir**
        Location for extra files, packages, and folders that the deployed project will need. For exapmle, add files, Python modules, or whole folders to this folder for which there is no "recipe" to include as part of the platform build. The entire file, module, or folder will be copied to the platform without modification.

    NOTE: These base directories must be created before running the project; that is, *pymixup* expects the basic project structure to be in place, it does not create these base directories. *pymixup* will create any required sub-folders of these base directories.

Specify names that should not be obfuscated
===========================================
*pymixup* builds a database of all the names used in a project. Some names, like Python key names, should not be obfuscated. Identify these names in the following lists found in **data/builddb.py** package.

    **reserved_list**
        These names will not be obfuscated. For convenience, the loading of *reserved_list* has been broken up into sections matching the library the reserved name is part of.

        If the name is a module name, then any imported name from the module and any attribute from one of those names will be considered reserved as well. For example,
        with reserved name "foo"::

            from foo import bar

            x = bar.baz

        "bar" and "baz" will be reserved as well.

        The following should be included in *reserved_list*:

            - Python reserved names.
            - Libraries you are importing that that should not be obfuscated (that is, libraries you did not write as part of your project).
            - Names (methods, class names, etc.) from imported libraries that are not either specifically imported using a "from somelibrary import name1, name2, ..." statement, or an attribute of a reserved name.
            - Parameter names in reserved methods and classes.

                For example, consider the following code for reserved libraries foo where bar is a class in foo::

                    from foo import *

                    x = bar.baz(parm1=True)
                    y = x.something

                In this case, the following describes whether the names have to be added to *reserved_list*:

                    - "foo": yes, to designate the module as reserved,
                    - "bar": yes, it's not identified as a reserved name in the import statement,
                    - "baz": no,  it's an attribute of "bar",
                    - "parm1": yes, parameters in reserved objects have to be added,
                    - "x": optional, if it is added, then "something" does not need to be added. If you want the variable "x" itself to be obfuscated, then add it.
                    - "something", yes, unless "x" is added

            - Database variable names (fields), named tuple fields, and other variables that exist both as quoted names and unquoted names in your programs or external tables. For example, the variable name "amount" cannot be obfuscated if it is used both as row.amount and row["amount"].


    **identifiers_list**
        The names in *identifiers_list* that should not be obfuscated are a special class of reserved names. They will be added to Identifier with the parameter **do_obfuscate** equal to False. This will prevent these names from being obfuscated, but will allow their attributes to be obfuscated. For example, "self" is a reserved name in the program Kivy, so it should not be obfuscated. However, we do want "bar" in self.bar to be obfuscated. Therefore add "self" to the *identifiers_list*, not to the *reserved_list*.

        There should be a very limited number of names in this list.

Specify work files and directories to exclude
=============================================
Some files and directories may be generated by your working environment that should not be included in the deployed version (for example, the .git folder). These are specified in the skip lists found in **<pymixup.py**.

    **skip_directories**
        Directories to skip (exclude from final project). For example, the .git repository.

    **skip_files**
        Files to skip (exclude from the final project).

Specify modules and files to add
================================
Some deployed platforms, for example Android and iOS, may require additional modules and files. Add these to the folder **extras_dir** (defined in the obfuscation directories above) and map them to the appropriate platform by including them in the **extra_paths** list. This list is loaded in **export/fabfile.py**, which is run with a parameter to specify which platform to export to.

    **extra_paths**
        Add the names of the files, modules, and folders that are in **extras_dir** to this list for the <platform> build.

For example, to use a Python library called "somelibrary", for which there is no Android recipe, plus a "bin" folder and a "buildozer.spec" file in your Android build, copy the entire library somelibrary, the directory bin, and the file buildozer.spec into the **extras_dir** library and add them to the **extra_paths** list in **export/fabfile.py**::

    if platform is 'android':
        extra_paths = [
            'somelibrary',
            'bin',
            'buildozer.spec',
        ]

These will be copied into the EXPORTED project as a final step when exporting to the "android" platform.