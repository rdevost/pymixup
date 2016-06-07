from peewee import IntegrityError

from logic.reserved import get_reserved, save_reserved


def add_reserveds(package_name, reserved_list, name_prefix=''):
    # Add package name as a module reserved name
    try:
        reserved_row = get_reserved(None)
        save_reserved(reserved_row,
                      name=package_name,
                      primary_package=package_name)
    except IntegrityError as e:
        # Continue if name already in db, o/w raise error
        if 'unique' not in e.message.lower():
            raise
    # Add package reserved names
    for reserved_name in reserved_list:
        if reserved_name == '__init__.py':
            continue
        reserved_row = get_reserved(None)
        try:
            save_reserved(reserved_row,
                          name=''.join([name_prefix, reserved_name]),
                          primary_package=package_name)
        except IntegrityError as e:
            # Continue if name already in db, o/w raise error
            if 'unique' not in e.message.lower():
                raise
