from peewee import IntegrityError, DoesNotExist

from data.base import obfuscatedb
from data.save_row import save_row
from logic.reserved import reserved_prefixes


def save_reserved(reserved_row, **kwargs):
    """Save a Reserved row."""
    from logic.identifier import get_identifier_by_name, \
        get_identifier_by_obfuscated, save_identifier, get_identifier
    try:
        for name, value in kwargs.iteritems():
            getattr(reserved_row, name)  # Make sure column exists
            setattr(reserved_row, name, value)

    except AttributeError:
        raise

    with obfuscatedb.atomic():
        try:
            reserved_id = save_row(reserved_row, **kwargs)
        except IntegrityError:
            raise

        ####################
        # Update identifiers
        ####################
        if reserved_row.name[0] in [reserved_prefixes.reserved_dir,
                                    reserved_prefixes.non_obfuscated_dir]:
            identifier_name = reserved_row.name[1:]
        elif reserved_row.name[0] in [reserved_prefixes.reserved_file,
                                      reserved_prefixes.non_obfuscated_file]:
            identifier_name = reserved_row.name[1:-3]
        else:
            identifier_name = reserved_row.name

        # Reassign identifier obfuscated name if it exists for another name
        try:
            identifier_row = get_identifier_by_obfuscated(identifier_name)
        except DoesNotExist:
            pass
        else:
            if identifier_row.name != identifier_name:
                identifier_row.obfuscated_name = None
                save_identifier(identifier_row)

        # Unobfuscate name in identifiers
        try:
            identifier_row = get_identifier_by_name(identifier_name)
        except DoesNotExist:
            identifier_row = get_identifier(None)
            save_identifier(
                identifier_row,
                name=identifier_name,
                obfuscated_name=identifier_name)
        else:
            if identifier_row.obfuscated_name != identifier_name:
                save_identifier(
                    identifier_row,
                    name=identifier_name,
                    obfuscated_name=identifier_name)

        return reserved_id
