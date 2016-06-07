from data.base import obfuscatedb
from data.save_row import save_row
from peewee import IntegrityError, DoesNotExist


def save_identifier(identifier_row, **kwargs):
    """Save and identifier row.

    Parameters
    ----------
    identifier_row

    Returns
    -------
    identifier_id : int
    """
    try:
        for name, value in kwargs.iteritems():
            getattr(identifier_row, name)  # Make sure column exists
            setattr(identifier_row, name, value)

    except AttributeError:
        raise

    with obfuscatedb.atomic():
        try:
            identifier_id = save_row(identifier_row, **kwargs)
        except IntegrityError as e:
            # Resave with different obfuscated_name if already exists
            if 'unique' in e.message.lower() \
                    and not kwargs.get('obfuscated_name', None) \
                    and 'obfuscated_name' in e.message:
                identifier_row.obfuscated_name = None
                identifier_id = save_identifier(identifier_row)
            else:
                raise
        except DoesNotExist:
            raise

        return identifier_id
