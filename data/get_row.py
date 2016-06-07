from peewee import DoesNotExist


def get_row(model, row_id, **kwargs):
    """Get a database row by its id.

    Parameters
    ----------
    model : BaseModel
    row_id : int or None

    Returns
    -------
    row
    """
    try:
        if row_id:
            try:
                row = model.get(model.id == row_id)
            except DoesNotExist:
                raise
        else:
            row = model()
    except ImportError:
        raise

    return row


def get_row_by_name(model, row_name, FK_name=None, FK_id=None, **kwargs):
    """Get a unique row by its name or by name plus FK if a FK is needed.

    Parameters
    ----------
    FK_id : int
    FK_name : str
    model : BaseModel
    row_name : str

    Returns
    -------
    row
    """
    try:
        if FK_name:
            row = model.get(model.name == row_name,
                            getattr(model, FK_name) == FK_id)
        else:
            row = model.get(model.name == row_name)
    except DoesNotExist:
        raise
    else:
        return row


def get_row_by_FK(model, FK_name, FK_id, is_required=False, **kwargs):
    """Get a unique row a FK id or return an empty row.

    Parameters
    ----------
    FK_id : int
    FK_name : str
    is_required : bool
    model : BaseModel

    Returns
    -------
    row
    """
    if FK_id:
        try:
            row = model.get(getattr(model, FK_name) == FK_id)
        except DoesNotExist:
            if is_required:
                raise
            else:
                row = model()
    else:
        row = model()

    return row


def get_row_by_fields(model, **kwargs):
    """Get a unique row by arbitrary fields.

    Parameters
    ----------
    kwargs : dict of field names and values
    model : BaseModel

    Returns
    -------
    row
    """
    field_name = []
    field_value = []
    try:
        for name, value in kwargs.iteritems():
            field_name.append(getattr(model, name))  # Make sure column exists
            field_value.append(value)
    except AssertionError as e:
        raise

    try:
        if len(field_name) == 1:
            row = model.get(field_name[0] == field_value[0])
        elif len(field_name) == 2:
            row = model.get(field_name[1] == field_value[1])
        elif len(field_name) == 3:
            row = model.get(field_name[2] == field_value[2])
        elif len(field_name) == 4:
            row = model.get(field_name[3] == field_value[3])
        elif len(field_name) == 5:
            row = model.get(field_name[4] == field_value[4])
        else:
            raise ValueError('Too many arguments for row lookup')
    except DoesNotExist:
        raise
    else:
        return row
