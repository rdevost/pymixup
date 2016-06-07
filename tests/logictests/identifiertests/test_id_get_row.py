import pytest
from peewee import DoesNotExist
from logic.identifier import get_identifier, get_identifier_by_name, \
    get_identifier_by_obfuscated, get_obfuscated_name


@pytest.mark.usefixtures('session')
def test_get_identifier():

    # Get good identifier_id
    identifier_row = get_identifier(1)
    assert identifier_row.id == 1
    assert identifier_row.name == u'identifier_one'

    # Fail at getting bad identifier_id
    with pytest.raises(DoesNotExist):
        get_identifier(999)


@pytest.mark.usefixtures('session')
def test_get_identifier_by_name():

    # Get good identifier_id
    identifier_row = get_identifier_by_name('identifier_one')
    assert identifier_row.id == 1
    assert identifier_row.name == u'identifier_one'

    # Fail at getting bad identifier_id
    with pytest.raises(DoesNotExist):
        get_identifier_by_name('junk')


@pytest.mark.usefixtures('session')
def test_get_obfuscated_name():

    # Get good identifier_id
    assert get_obfuscated_name('identifier_one') == u'aaa'
    assert get_obfuscated_name('junk') == u'junk'


@pytest.mark.usefixtures('session')
def test_get_identifier_by_obfuscated():

    # Get good identifier_id
    identifier_row = get_identifier_by_obfuscated('aaa')
    assert identifier_row.id == 1
    assert identifier_row.name == u'identifier_one'

    # Fail at getting bad identifier_id
    with pytest.raises(DoesNotExist):
        get_identifier_by_obfuscated('junk')