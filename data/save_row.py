from peewee import IntegrityError, DoesNotExist


def save_row(row, **kwargs):
    """Save a database row.

    Parameters
    ----------
    row

    Returns
    -------
    row_id : int
    """
    try:
        row.save()
    except IntegrityError as e:
        if 'unique' in e.message.lower():
            raise IntegrityError('\n'.join([
                'Record already exists.',
                e.message
                ]))
        else:
            raise IntegrityError
    except DoesNotExist:
        raise
    return row.id
