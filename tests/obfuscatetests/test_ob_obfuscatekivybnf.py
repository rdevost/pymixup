import pytest
from peewee import DoesNotExist
from logic.obfuscatefile import ObfuscateKivyBNF
from logic.identifier import get_identifier, save_identifier, \
    get_obfuscated_name, get_identifier_by_name
from logic.reserved import get_reserved_by_name


@pytest.mark.usefixtures('session')
def test_transform_statement():
    # Define values to be updated, and their new values
    names_to_update = {
        "variable": "v001",
        "variable_row": "v002",
        "search_variables": "v003",
        "variable_list": "v004",
        "variable_id": "v005",
        "select_variable": "v006",
        "variable_name": "v007",
        "VarValues": "v008",
        "scenario": "s001",
        "scenario_row": "s002",
        "search_scenarios": "s003",
        "scenario_list": "s004",
        "scenario_id": "s005",
        "select_scenario": "s006",
        "is_for_scenario_result": "s007",
        "is_for_variable_name": "s008",
        "decision": "d001",
        "decision_row": "d002",
        "search_decision": "d003",
        "decision_list": "d004",
        "decision_id": "d005",
        "is_edit_mode": "x001",
        }

    for ident_name, obfuscated_name in names_to_update.iteritems():
        identifier_row = get_identifier(None)
        save_identifier(
            identifier_row,
            name=ident_name,
            obfuscated_name=obfuscated_name
            )

    ##################
    # Test kivy source
    ##################
    bnf_parser = ObfuscateKivyBNF(get_obfuscated_name)

    # Test simple substitution
    assert bnf_parser.statement.transformString(
        "<VarValues>") == \
        "<v008>"

    # Test internationalization function
    assert bnf_parser.statement.transformString(
        "text: _('Variable type: Values')") == \
        "text:_('Variable type: Values')"

    # Test function
    assert bnf_parser.statement.transformString(
        "height: dp(self.variable) * font_multiplier + "
        "scenario.height") == \
        "height:dp(self.v001)*font_multiplier+s001.height"

    # Test kivy directive
    assert bnf_parser.statement.transformString(
        "#: import ButtonBar view.scenario.ButtonBar") == \
        "#: import ButtonBar view.s001.ButtonBar"


@pytest.mark.usefixtures('session')
def test_transform_conseq_idents_numbs():
    # Define values to be updated, and their new values
    names_to_update = {
        "variable": "v001",
        "variable_row": "v002",
        "scenario": "s001",
        "decision": "d001",
        "decision_row": "d002"
        }

    for ident_name, obfuscated_name in names_to_update.iteritems():
        identifier_row = get_identifier(None)
        save_identifier(
            identifier_row,
            name=ident_name,
            obfuscated_name=obfuscated_name
            )

    bnf_parser = ObfuscateKivyBNF(get_obfuscated_name)

    # Test that numbers separated from idents and they're not obfuscated
    assert bnf_parser.statement.transformString(
        "reserved_one 1 reserved_one -2.0") == \
        "reserved_one 1 reserved_one -2.0"
    assert bnf_parser.statement.transformString(
        "reserved_one <= 0 reserved_one >= 1") == \
        "reserved_one<=0 reserved_one>=1"


@pytest.mark.usefixtures('session')
def test_add_conseq_idents():
    bnf_parser = ObfuscateKivyBNF(get_obfuscated_name)

    # Identifiers after leading reserved attributes should not be obfuscated
    # conseq_idents will add identifiers indiscriminately
    bnf_parser.conseq_idents.parseString(
        "decision.scenario(variable) = reserved_one.variable")

    assert get_identifier_by_name('decision').obfuscated_name != 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name != 'scenario'
    assert get_identifier_by_name('variable').obfuscated_name != 'variable'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'

    # attribs should reserve
    bnf_parser.attribs.parseString(
        "decision.scenario(variable) = reserved_one.variable")
    assert get_identifier_by_name('decision').obfuscated_name != 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name != 'scenario'
    assert get_identifier_by_name('variable').obfuscated_name == 'variable'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'

    assert get_reserved_by_name('variable').primary_package == 'reserved_one'


@pytest.mark.usefixtures('session')
def test_add_conseq_idents_no_obfuscate():
    bnf_parser = ObfuscateKivyBNF(get_obfuscated_name)

    # Identifiers after leading reserved attributes should not be obfuscated
    # conseq_idents will add identifiers indiscriminately
    bnf_parser.conseq_idents_no_obfuscate.parseString(
        "decision.scenario(variable) = reserved_one.variable")

    assert get_identifier_by_name('decision').obfuscated_name == 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name == 'scenario'
    assert get_identifier_by_name('variable').obfuscated_name == 'variable'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'


@pytest.mark.usefixtures('session')
def test_add_kivy_import():
    bnf_parser = ObfuscateKivyBNF(get_obfuscated_name)

    # Reserve imported modules from first reserved module
    bnf_parser.kivy_import.parseString(
        "#: import is_reserved some_module.reserved_one")
    assert get_reserved_by_name('is_reserved').primary_package == \
        'reserved_one'
    with pytest.raises(DoesNotExist):
        get_reserved_by_name('some_module')

    # Reserve imported modules if first from module is reserved
    bnf_parser.kivy_import.parseString(
        "#: import is_reserved reserved_one.some_module")
    assert get_reserved_by_name('is_reserved').primary_package == \
        'reserved_one'
    assert get_reserved_by_name('some_module').primary_package == \
        'reserved_one'

    # Import without directive should take no action
    bnf_parser.kivy_import.parseString(
        "import not_reserved_1 reserved_one")
    with pytest.raises(DoesNotExist):
        get_reserved_by_name('not_reserved_1')


@pytest.mark.usefixtures('session')
def test_add_reserveds():
    # Define values to be updated, and their new values
    names_to_update = {
        "variable": "v001",
        "variable_row": "v002",
        "scenario": "s001",
        "decision": "d001",
        "decision_row": "d002"
        }

    for ident_name, obfuscated_name in names_to_update.iteritems():
        identifier_row = get_identifier(None)
        save_identifier(
            identifier_row,
            name=ident_name,
            obfuscated_name=obfuscated_name
            )

    bnf_parser = ObfuscateKivyBNF(get_obfuscated_name)

    # Identifiers after leading reserved attributes should not be obfuscated
    # They should be added to reserved and removed from identifiers
    bnf_parser.attribs.parseString(
        "decision.scenario(variable) = reserved_one.variable "
        "+ view.reserved_one")

    assert bnf_parser.statement.transformString(
        "decision.scenario(variable) = reserved_one.variable") == \
        "d001.s001(variable)=reserved_one.variable"

    assert get_reserved_by_name('variable').primary_package == 'reserved_one'
    assert get_identifier_by_name('variable').obfuscated_name == 'variable'
    with pytest.raises(DoesNotExist):
        assert get_identifier_by_name('view').obfuscated_name != 'view'
