import pytest
from peewee import DoesNotExist
from logic.identifier import add_identifiers, get_identifier_by_name


@pytest.mark.usefixtures('session')
def test_add_identifiers():
    #
    # Add python identifier names
    #
    identifier_list = [
        'variable',
        'variable_row',
        'search_variables',
        'variable_list',
        'variable_id',
        'select_variable',
        'variable_name',
        'VarValues',
        'scenario',
        'scenario_row',
        'search_scenarios',
        'scenario_list',
        'scenario_id',
        'select_scenario',
        'is_for_scenario_result',
        'is_for_variable_name',
        'decision',
        'decision_row',
        'search_decision',
        'decision_list',
        'decision_id',
        'is_edit_mode'
        ]
    add_identifiers(identifier_list)

    # Test some python keywords
    identifier_row = get_identifier_by_name('scenario')
    assert identifier_row.name == 'scenario'
    assert identifier_row.obfuscated_name != 'scenario'

    identifier_row = get_identifier_by_name('variable_id')
    assert identifier_row.name == 'variable_id'
    assert identifier_row.obfuscated_name != 'variable_id'

    identifier_row = get_identifier_by_name('search_decision')
    assert identifier_row.name == 'search_decision'
    assert identifier_row.obfuscated_name != 'search_decision'

    with pytest.raises(DoesNotExist):
        get_identifier_by_name('junk')

    #
    # Try to add reserved name
    #
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'
    identifier_list = [
        'reserved_one'
        ]
    add_identifiers(identifier_list)

    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'


    #
    # Save a non-obfuscated identifier, should change obfucated_name
    #
    identifier_list = [
        'decision'
        ]
    add_identifiers(identifier_list, do_obfuscate=False)
    assert get_identifier_by_name('decision').obfuscated_name == 'decision'

    #
    # Save a double-underscore name (should not be obfuscated)
    #
    identifier_list = [
        '__decision'
        ]
    add_identifiers(identifier_list)
    assert get_identifier_by_name('__decision').obfuscated_name == '__decision'
