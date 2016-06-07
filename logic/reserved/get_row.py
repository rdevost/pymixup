from data.get_row import get_row, get_row_by_name
from logic.reserved.reserved import Reserved


def get_reserved(reserved_id, **kwargs):
    """Get an reserved row from an id.

    Parameters
    ----------
    reserved_id : int or None

    Returns
    -------
    reserved_row
    """
    try:
        reserved_row = get_row(Reserved, reserved_id)
    except:
        raise
    return reserved_row


def get_reserved_by_name(reserved_name, **kwargs):
    """Get reserved by its name.

    Parameters
    ----------
    reserved_name : str

    Returns
    -------
    reserved_row
    """
    reserved_row = get_row_by_name(Reserved, reserved_name)
    return reserved_row
