import pytest
from peewee import IntegrityError


@pytest.mark.usefixtures('session')
def test_save_reserved_duplicate():
    from logic.reserved import save_reserved, get_reserved

    # Fail at duplicate add
    reserved_row = get_reserved(None)
    assert not reserved_row.id
    with pytest.raises(IntegrityError):
        assert save_reserved(
            reserved_row,
            name=u'reserved_one')


@pytest.mark.usefixtures('session')
def test_save_reserved_bad_column_name():
    from logic.reserved import save_reserved, get_reserved

    reserved_row = get_reserved(None)
    with pytest.raises(AttributeError):
        assert save_reserved(
            reserved_row,
            name=u'Reserved One BAD FIELD NAME FOR NOTES',
            notesxxx='Does not exist')


@pytest.mark.usefixtures('session')
def test_save_reserved_add():
    from logic.reserved import save_reserved, get_reserved

    reserved_row = get_reserved(None)
    assert save_reserved(
        reserved_row,
        name=u'Reserved_Three') == 2

    assert get_reserved(2).id == 2, 'Record not present or wrong id'

    # Change to Test Change Reserved
    save_reserved(
        reserved_row,
        name=u'Test_Change_Reserved')

    assert u'Test_Change_Reserved' == get_reserved(2).name


@pytest.mark.usefixtures('session')
def test_save_reserved_reassign():
    from logic.reserved import save_reserved, get_reserved
    from logic.identifier import get_identifier_by_name, save_identifier, \
        get_identifier

    identifier_row = get_identifier(None)
    save_identifier(
        identifier_row,
        name='some_ident',
        obfuscated_name='Reserved'
        )
    assert get_identifier_by_name('some_ident').obfuscated_name == 'Reserved'

    reserved_row = get_reserved(None)
    save_reserved(
        reserved_row,
        name=u'Reserved')

    assert get_identifier_by_name('some_ident').obfuscated_name != 'Reserved'
