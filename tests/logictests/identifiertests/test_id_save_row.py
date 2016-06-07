import pytest
from peewee import IntegrityError
from logic.identifier import save_identifier, get_identifier, \
    get_identifier_by_name
from logic.randomize import set_random_seed


@pytest.mark.usefixtures('session')
def test_save_identifier_duplicate():

    # Fail at duplicate add
    identifier_row = get_identifier(None)
    assert not identifier_row.id
    # Duplicate name
    with pytest.raises(IntegrityError):
        assert save_identifier(
            identifier_row,
            name=u'identifier_one',
            obfuscated_name='bbb')

    # Duplicate obfuscated name
    with pytest.raises(IntegrityError):
        assert save_identifier(
            identifier_row,
            name=u'identifier_xxx',
            obfuscated_name='aaa')


    # Duplicate randomly assigned obfuscated name
    identifier_row = get_identifier(None)
    set_random_seed(1)
    assert save_identifier(
        identifier_row,
        name=u'identifier_001')
    ident_001_obfuscated_name = get_identifier_by_name(
        u'identifier_001').obfuscated_name
    # Reset random seed to recreate last result
    identifier_row = get_identifier(None)
    set_random_seed(1)
    assert save_identifier(
        identifier_row,
        name=u'identifier_002')

    assert get_identifier_by_name(u'identifier_002').obfuscated_name != \
        ident_001_obfuscated_name


@pytest.mark.usefixtures('session')
def test_save_identifier_bad_column_name():
    from logic.identifier import save_identifier, get_identifier

    identifier_row = get_identifier(None)
    with pytest.raises(AttributeError):
        assert save_identifier(
            identifier_row,
            name=u'Identifier One BAD FIELD NAME',
            obfuscted_name='xxx',
            xxx='Does not exist')


@pytest.mark.usefixtures('session')
def test_save_identifier_add():
    from logic.identifier import save_identifier, get_identifier

    identifier_row = get_identifier(None)
    save_identifier(
        identifier_row,
        name=u'Identifier_Two',
        obfuscated_name='bbb')

    assert get_identifier(3).id == 3

    # Change identifier
    save_identifier(
        identifier_row,
        name=u'Test_Change_Identifier')

    assert u'Test_Change_Identifier' == get_identifier(3).name
    # Change obfuscated name
    save_identifier(
        identifier_row,
        obfuscated_name=u'zzz')

    assert u'zzz' == get_identifier(3).obfuscated_name


@pytest.mark.usefixtures('session')
def test_save_identifier_reserved():
    from logic.identifier import save_identifier, get_identifier

    identifier_row = get_identifier(None)
    assert save_identifier(
        identifier_row,
        name=u'Identifier_Two',
        obfuscated_name='reserved_one') == 3

    assert get_identifier(3).obfuscated_name != 'reserved_one'