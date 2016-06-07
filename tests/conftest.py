# -*- coding: utf-8 -*-
"""Setup database for testing.

Decorate pytest functions with @pytest.mark.usefixtures('session')
to use database.
"""
from os import environ

import pytest


@pytest.fixture(autouse=True)
def set_env():
    environ['IS_PYMIXUP_TEST'] = '1'


@pytest.fixture(scope='session')
def database(request):
    from logic.identifier import Identifier
    from logic.reserved import Reserved
    from data.base import obfuscatedb

    obfuscatedb.create_tables([Identifier, Reserved])

    def teardown():
        pass

    request.addfinalizer(teardown)
    return database


@pytest.fixture(scope='function')
def session(database, request):
    from logic.identifier import Identifier, get_identifier, save_identifier
    from logic.reserved import Reserved, get_reserved, save_reserved
    from data.base import obfuscatedb

    obfuscatedb.create_tables([Identifier,
                               Reserved], safe=True)

    # Add a decision, decision_id = 1
    identifier_row = get_identifier(None)
    assert 1 == save_identifier(
        identifier_row,
        name=u'identifier_one',
        obfuscated_name=u'aaa')

    reserved_row = get_reserved(None)
    assert 1 == save_reserved(
        reserved_row,
        name=u'reserved_one',
        primary_package=u'module')

    assert get_identifier(1).name == 'identifier_one'
    assert get_identifier(1).obfuscated_name == 'aaa'
    assert get_identifier(2).name == 'reserved_one'
    assert get_identifier(2).obfuscated_name == 'reserved_one'

    def teardown():
        obfuscatedb.drop_tables([Identifier,
                                 Reserved], safe=True)

    request.addfinalizer(teardown)
    return session
