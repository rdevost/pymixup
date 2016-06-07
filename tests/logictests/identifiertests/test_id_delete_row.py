import pytest
from peewee import DoesNotExist


@pytest.mark.usefixtures('session')
def test_logic_identifier_delete():
    from logic.identifier import delete_identifier, get_identifier, \
        save_identifier

    identifier_row = get_identifier(None)
    assert save_identifier(
        identifier_row,
        name=u'Identifier Two')

    assert get_identifier(2).id == 2, 'Record not present or wrong id'

    # Delete an existing identifier
    row = get_identifier(2)
    assert delete_identifier(row) == 1

    with pytest.raises(DoesNotExist):
        assert get_identifier(2).id == 2, 'Record not found'

    # Fail to delete a non-existing identifier
    with pytest.raises(DoesNotExist):
        assert delete_identifier(row)