import pytest
from peewee import DoesNotExist
from logic.reserved import get_reserved, get_reserved_by_name


@pytest.mark.usefixtures('session')
def test_get_reserved():

    # Get good reserved_id
    reserved_row = get_reserved(1)
    assert reserved_row.id == 1
    assert reserved_row.name == u'reserved_one'

    # Fail at getting bad reserved_id
    with pytest.raises(DoesNotExist):
        get_reserved(999)


@pytest.mark.usefixtures('session')
def test_get_reserved_by_name():

    # Get good reserved_id
    reserved_row = get_reserved_by_name('reserved_one')
    assert reserved_row.id == 1
    assert reserved_row.name == u'reserved_one'

    # Fail at getting bad reserved_id
    with pytest.raises(DoesNotExist):
        get_reserved_by_name('junk')
