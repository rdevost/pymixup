import datetime

import pytest
from peewee import DoesNotExist


@pytest.mark.usefixtures('session')
def test_create_decision():
    from logic.identifier import Identifier
    from logic.identifier import get_identifier

    time_before = datetime.datetime.now()
    identifier_row = get_identifier(None)
    time_after = datetime.datetime.now()

    assert not identifier_row.id
    assert identifier_row.name == Identifier.name.default
    assert identifier_row.obfuscated_name == Identifier.obfuscated_name.default
    assert time_before <= identifier_row.created_timestamp <= time_after

    # Fail at bad parameter
    with pytest.raises(DoesNotExist):
        get_identifier(999)