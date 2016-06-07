import re

import peewee as pwe

from data.search_rows import search_rows
from logic.reserved.reserved import Reserved


def search_reserveds(search_text, **kwargs):
    is_first = True
    where_clause = None
    if search_text:
        search_values = re.sub('[~`%&-+=]', '', search_text).split()
        for s in search_values:
            s_ = u'%'+s+u'%'
            if is_first:
                where_clause = (Reserved.name ** s_)
                is_first = False
            else:
                where_clause = where_clause & \
                    (Reserved.name ** s_)
    if is_first:
        where_clause = (~(Reserved.id >> None))

    select_clause = pwe.SelectQuery(Reserved, Reserved.id, Reserved.name)
    order_by_clause = Reserved.name
    reserved_list = search_rows(select_clause, where_clause, order_by_clause)

    return reserved_list
