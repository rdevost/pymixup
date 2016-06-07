import re

import peewee as pwe

from data.search_rows import search_rows
from logic.identifier.identifier import Identifier


def search_identifiers(search_text, **kwargs):
    """Fetch identifier rows.

    Parameters
    ----------
    search_text : str or None

    Returns
    -------
    identifier_list
    """
    is_first = True
    where_clause = None
    if search_text:
        search_values = re.sub('[~`%&-+=]', '', search_text).split()
        for s in search_values:
            s_ = u'%'+s+u'%'
            if is_first:
                where_clause = (Identifier.name ** s_)
                is_first = False
            else:
                where_clause = where_clause & \
                    (Identifier.name ** s_)
    if is_first:
        where_clause = (~(Identifier.id >> None))

    select_clause = pwe.SelectQuery(Identifier, Identifier.id, Identifier.name)
    order_by_clause = Identifier.name
    identifier_list = search_rows(select_clause, where_clause, order_by_clause)

    return identifier_list
