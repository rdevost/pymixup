import pytest


@pytest.mark.usefixtures('session')
def test_search_identifiers():
    from logic.identifier import get_identifier, save_identifier, \
        search_identifiers

    identifier_row = get_identifier(1)
    assert identifier_row.name == u'identifier_one'

    # Find One
    identifier_list = search_identifiers(u'identifier')
    count = 0
    for d in identifier_list:
        count += 1
        assert 'one' in d['name']
    assert count == 1

    # Add a identifier, id = 3
    identifier_row = get_identifier(None)
    assert 3 == save_identifier(identifier_row,
        name=u'identifier_two')

    # Find One and Two
    identifier_list = search_identifiers(u'iden%tifie &_')
    count = 0
    for d in identifier_list:
        count += 1
        assert 'identifier' in d['name']
    assert count == 2

    # Find only Two
    identifier_list = search_identifiers(u'two')
    count = 0
    for d in identifier_list:
        count += 1
        assert 'two' in d['name']
    assert count == 1

    # Find none
    identifier_list = search_identifiers(u'id xxx')
    count = 0
    for d in identifier_list:
        count += 1
    assert count == 0

    # Find all with blank search
    identifier_list = search_identifiers(u'')
    count = 0
    for d in identifier_list:
        count += 1
        assert 'identifier' in d['name'] or 'reserved_one' in d['name']
    assert count == 3

    # Find all with None search
    identifier_list = search_identifiers(None)
    count = 0
    for d in identifier_list:
        count += 1
        assert 'identifier' in d['name'] or 'reserved_one' in d['name']
    assert count == 3