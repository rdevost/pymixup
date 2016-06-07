import pytest
from peewee import DoesNotExist


@pytest.mark.usefixtures('session')
def test_logic_reserved_delete():
    from logic.reserved import delete_reserved, get_reserved, \
        save_reserved

    reserved_row = get_reserved(None)
    assert save_reserved(
        reserved_row,
        name=u'Reserved Two')

    assert get_reserved(2).id == 2, 'Record not present or wrong id'

    # Delete an existing reserved
    row = get_reserved(2)
    assert delete_reserved(row) == 1

    with pytest.raises(DoesNotExist):
        assert get_reserved(2).id == 2, 'Record not found'

    # Fail to delete a non-existing reserved
    with pytest.raises(DoesNotExist):
        assert delete_reserved(row)
