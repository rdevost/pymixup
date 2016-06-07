def search_rows(select_clause, where_clause, order_by_clause, **kwargs):
    """Fetch rows.

    Parameters
    ----------
    order_by_clause
    select_clause
    where_clause

    Returns
    -------
    row_list
    """
    try:
        row_list = select_clause.where(where_clause).order_by(
            order_by_clause).dicts()
    except:
        raise

    return row_list
