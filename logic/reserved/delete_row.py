from data.base import obfuscatedb
from data.delete_row import delete_row


def delete_reserved(reserved_row, **kwargs):
    """Delete a row from the Reserved table."""
    with obfuscatedb.atomic():
        try:
            is_deleted = delete_row(reserved_row, **kwargs)
        except:
            raise

        return is_deleted
