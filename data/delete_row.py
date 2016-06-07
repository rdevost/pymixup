from peewee import DoesNotExist


def delete_row(row, **kwargs):
    """Delete a database row.

    Parameters
    ----------
    row
    """
    try:
        num_deleted = row.delete_instance(recursive=True, delete_nullable=True)
        if num_deleted == 0:
            raise DoesNotExist
    except:
        raise
    return True
