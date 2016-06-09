from __future__ import with_statement
from time import ctime, time

from import_project import import_proj
from obfuscate import obfuscate


def obfuscate_proj(platform='default',
                   do_rebuild=True,
                   is_verbose=True,
                   do_import=False):
    """Obfuscate a project.

    Parameters
    ----------
    do_import : bool
        Run import_project fabfile if True.
    do_rebuild : bool
        Rebuild the Reserved and Identifier tables if True.
    is_verbose: bool
        Print verbose messages.
    platform : str
        Destination platform.

    Returns
    -------
    True if successfully completed.
    """
    print('***OBFUSCATE tasks started at {}'.format(ctime(time())))

    if do_import:
        if not import_proj():
            print('### Import called but failed. Export canceled. ###')
            return

    obfuscate(platform=platform, do_rebuild=do_rebuild, is_verbose=is_verbose)

    print('***OBFUSCATE tasks ended at {}'.format(ctime(time())))
    return True
