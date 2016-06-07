import pytest


@pytest.mark.usefixtures('session')
def test_search_reserveds():
    from logic.reserved import get_reserved, save_reserved, \
        search_reserveds

    reserved_row = get_reserved(1)
    assert reserved_row.name == u'reserved_one'

    # Find One
    reserved_list = search_reserveds(u'reserved')
    count = 0
    for d in reserved_list:
        count += 1
        assert 'one' in d['name']
    assert count == 1

    # Add a reserved, id = 2
    reserved_row = get_reserved(None)
    assert 2 == save_reserved(reserved_row,
        name=u'reserved_two')

    # Find One and Two
    reserved_list = search_reserveds(u'res%erved &_')
    count = 0
    for d in reserved_list:
        count += 1
        assert 'reserved' in d['name']
    assert count == 2

    # Find only Two
    reserved_list = search_reserveds(u'two')
    count = 0
    for d in reserved_list:
        count += 1
        assert 'two' in d['name']
    assert count == 1

    # Find none
    reserved_list = search_reserveds(u'id xxx')
    count = 0
    for d in reserved_list:
        count += 1
    assert count == 0

    # Find all with blank search
    reserved_list = search_reserveds(u'')
    count = 0
    for d in reserved_list:
        count += 1
        assert 'reserved' in d['name']
    assert count == 2

    # Find all with None search
    reserved_list = search_reserveds(None)
    count = 0
    for d in reserved_list:
        count += 1
        assert 'reserved' in d['name']
    assert count == 2
