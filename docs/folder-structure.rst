=================================
Folder Structure for Source Files
=================================
Each step in obfuscating a project writes files into a set of designated folders. In addition to capturing the obfuscation step in the folder name (e.g., "IMPORTED"), the folder structure also uses the project name (e.g., "MyProject") and the name of the destination platform it is intended for (e.g., "android").

The default names for each step are specified in common/settings.py.

If using the defaults names, the obfuscation steps populate the folders as follows:

    1. Copies the development project into IMPORTED.
    2. Obfuscates the IMPORTED project, which writes the obfuscated code into OBFUSCATED.
    3. To test, the OBFUSCATED project (plus some other needed files from EXTRAS) is copied into EXPORTED.
    4. After deploying, the EXPORTED project is copied into DEPLOYED under a version number.

Note that files in IMPORTED, OBFUSCATED, and EXPORTED are overwritten when the steps are repeated. For deployed projects, however, permanent copies are retained under their version numbers.

The folder structure looks like::

    ~projects
        ├── <MyProject> (The development project.)
        │   └── ...
        ├── IMPORTED (Projects to obfuscate; imported from <MyProject>.)
        │   └── <MyProject>
        │       ├── to_obfuscate (Files and packages to be obfuscated.)
        │       └── to_not_obfuscate (Files and folders that are not to be obfuscated.)
        ├── OBFUSCATED (Obfuscated projects.)
        │   └── <MyProject>
        │       ├── <platform>
        │       │   ├── obfuscated (The obfuscated project files.)
        │       │   ├── unobfuscated (The unobfuscated project files.)
        │       │   │   ├── to_obfuscate (A copy of the files that will be obfuscated.)
        │       │   │   └── to_not_obfuscate (A copy of the files that are not obfuscated.)
        │       │   └── db (A copy of the db.)
        │       └── db (The db of Identifier and Reserved name tables.)
        ├── EXPORTED ... (Contains exported copies of folders in OBFUSCATED.)
        │   └── <MyProject>
        │       └── <platform>
        │           ├── obfuscated (The obfuscated project files.)
        │           ├── unobfuscated (All project files, before obfuscation.)
        │           └── db (A copy of the db.)
        ├── DEPLOYED ... (Contains deployed copies of folders in EXPORTED.)
        │   └── <MyProject>
        │       └── <platform>
        │           └── <version number>
        │               ├── obfuscated (The obfuscated project files.)
        │               ├── unobfuscated (All project files, before obfuscation.)
        │               └── db (A copy of the db.)
        └── EXTRAS (Additional packages, files, and folders needed for the project.)
            └── ...

