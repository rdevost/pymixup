import pytest
import keyword
from logic.reserved import add_reserveds, get_reserved_by_name


@pytest.mark.usefixtures('session')
def test_build_db():
    reserved_list = keyword.kwlist
    add_reserveds('Python', reserved_list)

    # Test some python keywords
    reserved_row = get_reserved_by_name('from')
    assert reserved_row.name == 'from'

    reserved_row = get_reserved_by_name('with')
    assert reserved_row.name == 'with'

    reserved_row = get_reserved_by_name('class')
    assert reserved_row.name == 'class'

    with pytest.raises(AssertionError):
        assert reserved_row.name == 'junk'
