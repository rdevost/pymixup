from peewee import IntegrityError, DoesNotExist

from logic.identifier import save_identifier, get_identifier, \
    get_identifier_by_name
from logic.reserved import get_reserved_by_name


def add_identifiers(identifier_list=None, do_obfuscate=True):
    """Add identifier and obfuscated names to Identifiers table.

    Parameters
    ----------
    do_obfuscate : bool
    identifier_list : list
    """
    for identifier_name in identifier_list:
        # Skip identifiers in reserved
        try:
            get_reserved_by_name(identifier_name)
        except DoesNotExist:
            pass
        else:
            continue

        if not do_obfuscate \
                or identifier_name[0:2] == '__' \
                or identifier_name == '__init__.py' \
                or identifier_name.startswith('test_') \
                or identifier_name.endswith('_test.py'):
            obfuscated_name = identifier_name
        else:
            obfuscated_name = ''

        identifier_row = get_identifier(None)
        try:
            save_identifier(identifier_row,
                            name=identifier_name,
                            obfuscated_name=obfuscated_name)
        except IntegrityError as e:
            if 'unique' not in e.message.lower():
                raise
            # If should not be obfuscated, replace obfuscated, o/w pass
            if not do_obfuscate:
                identifier_row = get_identifier_by_name(identifier_name)
                if identifier_row.obfuscated_name != identifier_name:
                    save_identifier(identifier_row,
                                    obfuscated_name=identifier_name)
