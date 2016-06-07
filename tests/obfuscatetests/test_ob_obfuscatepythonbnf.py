import pytest
from peewee import DoesNotExist
from logic.obfuscate import ObfuscatePythonBNF
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

    ####################
    # Test python source
    ####################
    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

    # Test simple substitution
    assert bnf_parser.statement.transformString(
        "    update(x.scenario_row, decision_id.y, z)") == \
        "    update(x.s002,d005.y,z)"

    # Test substitutions with other non-name symbols
    assert bnf_parser.statement.transformString(
        "    update(x.scenario_row, z) + 5*27 /3 == 'some junk'") == \
        "    update(x.s002,z)+5*27/3=='some junk'"

    # Test string parameters
    assert bnf_parser.statement.transformString(
        "    update(x.scenario_row, 'decision_id', z)") == \
        "    update(x.s002,'decision_id',z)"

    assert bnf_parser.statement.transformString(
        "variable.scenario(is_edit_mode) = scenario_list  # Do something") == \
        "v001.s001(x001)=s004"

    # Test init def
    assert bnf_parser.statement.transformString(
        "    def __init__(self,*args,**kwargs):") == \
        "    def __init__(self,*args,**kwargs):"

    # Test with None
    assert bnf_parser.statement.transformString(
        "self.get_variable_values = kwargs.get('get_values', None)") == \
        "self.get_variable_values=kwargs.get('get_values',None)"

    # Test with keyword from and import; multiple consecutive idents
    assert bnf_parser.statement.transformString(
        "from scenario import ValidationError, variable.xyz") == \
        "from s001 import ValidationError,v001.xyz"

    # Test with keyword except; multiple consecutive idents
    assert bnf_parser.statement.transformString(
        "    except FloatingPointError:") == \
        "    except FloatingPointError:"

    # Test with separator characters
    assert bnf_parser.statement.transformString(
        "print scenario, import % 2") == \
        "print s001,import%2"

    # Test dictionary
    assert bnf_parser.statement.transformString("[]") == "[]"
    assert bnf_parser.statement.transformString(
        "{'scenario': decision, scenario: 'decision'}") == \
        "{'scenario':d001,s001:'decision'}"

    # Test list
    assert bnf_parser.statement.transformString("a={}") == "a={}"
    assert bnf_parser.statement.transformString("**a=={}") == "**a=={}"
    assert bnf_parser.statement.transformString(
        "['scenario', {xyz: decision},scenario,[a,b],  'decision']") == \
        "['scenario',{xyz:d001},s001,[a,b],'decision']"

    # Test that sci-notation numbers are not obfuscated
    assert bnf_parser.fnumber.transformString(
        "(-3.969683028665376e+01, 2.209460984245205e+02)") == \
        "(-3.969683028665376e+01, 2.209460984245205e+02)"


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

    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

    # Test that numbers separated from idents and they're not obfuscated
    assert bnf_parser.statement.transformString(
        "reserved_one 1 reserved_one -2.0") == \
        "reserved_one 1 reserved_one -2.0"
    assert bnf_parser.statement.transformString(
        "reserved_one <= 0 reserved_one >= 1") == \
        "reserved_one<=0 reserved_one>=1"


@pytest.mark.usefixtures('session')
def test_transform_builder():
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

    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

    # Test kivy Builder
    assert bnf_parser.builder.transformString(
        "Builder.load_file('view/decision/scenario.kv')") == \
        "Builder.load_file('view/d001/s001.kv')"


@pytest.mark.usefixtures('session')
def test_add_conseq_idents():
    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

    # Conseq_idents will add identifiers without checking whether it is
    # an attribute of a reserved name
    bnf_parser.conseq_idents.parseString(
        "decision.scenario(variable) = reserved_one.variable.another")

    assert get_identifier_by_name('decision').obfuscated_name != 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name != 'scenario'
    assert get_identifier_by_name('variable').obfuscated_name != 'variable'
    assert get_identifier_by_name('another').obfuscated_name != 'another'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'


@pytest.mark.usefixtures('session')
def test_add_attribs():
    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

    # Identifiers after leading reserved attributes should not be obfuscated

    # Attribs should reserve and unobfuscate names in identifiers
    source = "decision.scenario(variable) = reserved_one.variable.another"
    bnf_parser.attribs.parseString(source)
    bnf_parser.conseq_idents.parseString(source)
    assert get_identifier_by_name('decision').obfuscated_name != 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name != 'scenario'
    assert get_identifier_by_name('variable').obfuscated_name == 'variable'
    assert get_identifier_by_name('another').obfuscated_name == 'another'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'

    assert get_reserved_by_name('variable').primary_package == 'reserved_one'
    assert get_reserved_by_name('another').primary_package == 'reserved_one'

    # Attribs should reserve only after reserved name
    source = "decision.scenario.reserved_one.variable2.another2"
    bnf_parser.attribs.parseString(source)
    bnf_parser.conseq_idents.parseString(source)
    assert get_identifier_by_name('decision').obfuscated_name != 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name != 'scenario'
    assert get_identifier_by_name('variable2').obfuscated_name == 'variable2'
    assert get_identifier_by_name('another2').obfuscated_name == 'another2'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'

    # Attribs should reserve only after reserved name, not parameters
    source = "decision.scenario.reserved_one(variable3).another3"
    bnf_parser.attribs.parseString(source)
    bnf_parser.conseq_idents.parseString(source)
    assert get_identifier_by_name('decision').obfuscated_name != 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name != 'scenario'
    assert get_identifier_by_name('variable3').obfuscated_name != 'variable3'
    assert get_identifier_by_name('another3').obfuscated_name != 'another3'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'

    # Attribs should reserve only after reserved name
    source = "decision.scenario.reserved_one.variable4 " \
             "+ variable5.reserved_one.another5"
    bnf_parser.attribs.parseString(source)
    bnf_parser.conseq_idents.parseString(source)
    assert get_identifier_by_name('decision').obfuscated_name != 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name != 'scenario'
    assert get_identifier_by_name('variable4').obfuscated_name == 'variable4'
    assert get_identifier_by_name('variable5').obfuscated_name != 'variable5'
    assert get_identifier_by_name('another5').obfuscated_name == 'another5'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'

    # Attribs should reserve even if they are functions
    source = "decision.scenario.reserved_one.variable6(another6)"
    bnf_parser.attribs.parseString(source)
    bnf_parser.conseq_idents.parseString(source)
    assert get_identifier_by_name('decision').obfuscated_name != 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name != 'scenario'
    assert get_identifier_by_name('variable6').obfuscated_name == 'variable6'
    assert get_identifier_by_name('another6').obfuscated_name != 'another6'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
           'reserved_one'


@pytest.mark.usefixtures('session')
def test_add_conseq_idents_no_obfuscate():
    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

    # Conseq_idents_no_obfuscate will add identifiers without checking
    # whether it is an attribute of a reserved name
    bnf_parser.conseq_idents_no_obfuscate.parseString(
        "decision.scenario(variable) = reserved_one.variable")

    assert get_identifier_by_name('decision').obfuscated_name == 'decision'
    assert get_identifier_by_name('scenario').obfuscated_name == 'scenario'
    assert get_identifier_by_name('variable').obfuscated_name == 'variable'
    assert get_identifier_by_name('reserved_one').obfuscated_name == \
        'reserved_one'


@pytest.mark.usefixtures('session')
def test_add_from_import():
    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

    # Reserve imported modules if first from module is reserved
    bnf_parser.from_import.parseString(
        "   from some_module.reserved_one import is_reserved, also_is")
    assert get_reserved_by_name('is_reserved')
    assert get_reserved_by_name('also_is')

    # Reserve imported modules if first from module is reserved
    bnf_parser.from_import.parseString(
        "   from reserved_one.some_module import is_reserved, also_reserved")
    assert get_reserved_by_name('is_reserved').primary_package == \
        'reserved_one'
    assert get_reserved_by_name('also_reserved').primary_package == \
        'reserved_one'

    # Import (without a from) should take no action
    bnf_parser.from_import.parseString(
        "   import reserved_one, not_reserved_1, also_not_1")
    with pytest.raises(DoesNotExist):
        get_reserved_by_name('not_reserved_1')
    with pytest.raises(DoesNotExist):
        get_reserved_by_name('also_not_1')


@pytest.mark.usefixtures('session')
def test_add_except_error():
    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

    # Reserve exception names
    bnf_parser.except_error.parseString(
        "   except (FloatingPointError, SomeOtherError) as exc_err")
    assert get_reserved_by_name('FloatingPointError')
    assert get_reserved_by_name('SomeOtherError')
    with pytest.raises(DoesNotExist):
        assert get_reserved_by_name('exc_err')

    # Reserve exception names with double tab
    bnf_parser.except_error.parseString(
        "       except (FloatingPointError, SomeOtherError) as exc_err")
    assert get_reserved_by_name('FloatingPointError')
    assert get_reserved_by_name('SomeOtherError')
    with pytest.raises(DoesNotExist):
        assert get_reserved_by_name('exc_err')


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

    bnf_parser = ObfuscatePythonBNF(get_obfuscated_name)

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
