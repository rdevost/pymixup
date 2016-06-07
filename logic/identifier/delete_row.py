from data.base import obfuscatedb
from data.delete_row import delete_row


def delete_identifier(identifier_row, **kwargs):
    """Delete an identifier row.

    Parameters
    ----------
    identifier_row
    """
    with obfuscatedb.atomic():
        try:
            is_deleted = delete_row(identifier_row, **kwargs)
        except:
            raise

        return is_deleted
