def validate_fields(row):
    """Validate all fields in a database row.

    Parameters
    ----------
    row : A row to validate.
    """
    try:
        row.validate_fields()
    except AssertionError:
        raise
