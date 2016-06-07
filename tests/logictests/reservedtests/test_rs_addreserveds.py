import pytest
import keyword
from peewee import DoesNotExist

from logic.reserved import add_reserveds, get_reserved_by_name
from logic.identifier import add_identifiers, get_identifier_by_name


@pytest.mark.usefixtures('session')
def test_add_reserveds():
    #
    # Add python reserved names
    #
    reserved_list = keyword.kwlist
    add_reserveds('python', reserved_list)

    # Test 'python' in module reserved keywords
    reserved_row = get_reserved_by_name('python')
    assert reserved_row.name == 'python'
    assert reserved_row.primary_package == 'python'

    # Test some python keywords
    reserved_row = get_reserved_by_name('from')
    assert reserved_row.name == 'from'
    assert reserved_row.primary_package == 'python'

    reserved_row = get_reserved_by_name('with')
    assert reserved_row.name == 'with'
    assert reserved_row.primary_package == 'python'

    reserved_row = get_reserved_by_name('class')
    assert reserved_row.name == 'class'
    assert reserved_row.primary_package == 'python'

    #
    # Add kivy reserved names
    #
    reserved_list = [
        'after', 'App', 'app',
        'before', 'bold', 'BooleanProperty','BoxLayout', 'Button',
        'canvas', 'color',
        'disabled', 'dp', 'dpi2px', 'dx',
        'FileChooser', 'filechooser', 'FloatLayout', 'focus', 'font',
        'GridLayout',
        'halign', 'height', 'hint_text', 'horizontal',
        'id',
        'kivy',
        'Label', 'Logger', 'logger',
        'multiline',
        'NumericProperty',
        'ObjectProperty', 'on_focus', 'op_press', 'orientation',
        'padding', 'platform', 'properties', 'px',
        'Rectangle', 'require', 'rgba', 'root',
        'ScreenManager', 'screenmanager', 'self',
        'size', 'size_hint', 'size_hint_x', 'size_hint_y', 'StringProperty',
        'sp',
        'text', 'text_size',
        'uix', 'utils',
        'valign', 'vertical',
        ]
    add_reserveds('kivy', reserved_list)

    # Test some kivy keywords
    reserved_row = get_reserved_by_name('kivy')
    assert reserved_row.name == 'kivy'
    assert reserved_row.primary_package == 'kivy'

    reserved_row = get_reserved_by_name('color')
    assert reserved_row.name == 'color'
    assert reserved_row.primary_package == 'kivy'

    reserved_row = get_reserved_by_name('BoxLayout')
    assert reserved_row.name == 'BoxLayout'
    assert reserved_row.primary_package == 'kivy'

    with pytest.raises(DoesNotExist):
        get_reserved_by_name('junk')

    # Test removing of identifier for new reserved names

    #
    # Add python identifier names
    #
    identifier_list = [
        'variable',
        'variable_row',
        ]
    add_identifiers(identifier_list)

    reserved_list = ['variable']
    add_reserveds('test', reserved_list)

    assert get_identifier_by_name('variable_row').name == 'variable_row'
    assert get_identifier_by_name('variable').obfuscated_name == 'variable'

    #
    # Should not add __init__.py
    #
    reserved_list = ['__init__.py']
    add_reserveds('test', reserved_list, '=')

    with pytest.raises(DoesNotExist):
        get_identifier_by_name('__init__.py')
