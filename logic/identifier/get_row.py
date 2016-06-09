from peewee import DoesNotExist

from data.get_row import get_row, get_row_by_fields, get_row_by_name
from logic.identifier.identifier import Identifier


def get_identifier(identifier_id, **kwargs):
    """Get an identifier row from an id.

    Parameters
    ----------
    identifier_id : int or None

    Returns
    -------
    identifier_row
    """
    try:
        identifier_row = get_row(Identifier, identifier_id)
    except:
        raise
    return identifier_row


def get_identifier_by_name(identifier_name, **kwargs):
    """Get identifier row by its name.

    Parameters
    ----------
    identifier_name : str

    Returns
    -------
    identifier_row
    """
    identifier_row = get_row_by_name(Identifier, identifier_name)
    return identifier_row


def get_identifier_by_obfuscated(obfuscated_name):
    """Get an identifier row by it's obfuscated name.

    Parameters
    ----------
    obfuscated_name: str

    Returns
    -------
    identifier_row
    """
    identifier_row = get_row_by_fields(Identifier,
                                       obfuscated_name=obfuscated_name)
    return identifier_row


def get_obfuscated_by_lower(obfuscated_lower, **kwargs):
    """Get an identifier row from the lowercase obfuscated value.

    Parameters
    ----------
    obfuscated_lower: str

    Returns
    -------
    identifier_row
    """
    try:
        identifier_row = get_row_by_fields(Identifier,
                                           obfuscated_lower=obfuscated_lower)
        return identifier_row.name
    except DoesNotExist:
        return None


def get_obfuscated_name(identifier_name, **kwargs):
    """Get obfuscated name of an identifier.

    Parameters
    ----------
    identifier_name : str

    Returns
    -------
    obfuscated_name : str
    """
    try:
        identifier_row = get_identifier_by_name(identifier_name)
        return identifier_row.obfuscated_name
    except DoesNotExist:
        return identifier_name
