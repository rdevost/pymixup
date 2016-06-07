import datetime

import pytest
from peewee import DoesNotExist


@pytest.mark.usefixtures('session')
def test_create_decision():
    from logic.reserved import Reserved
    from logic.reserved import get_reserved

    time_before = datetime.datetime.now()
    reserved_row = get_reserved(None)
    time_after = datetime.datetime.now()

    assert not reserved_row.id
    assert reserved_row.name == Reserved.name.default
    assert time_before <= reserved_row.created_timestamp <= time_after

    # Fail at bad parameter
    with pytest.raises(DoesNotExist):
        get_reserved(999)
