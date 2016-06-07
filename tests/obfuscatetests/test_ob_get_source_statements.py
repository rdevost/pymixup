import pytest
from os.path import join
import io
from logic.obfuscate import source_statement_gen


def test_get_source_statements(tmpdir):
    #
    # Create a short source file
    #
    dir_name = str(tmpdir.mkdir('source'))
    source_file = 'app.py'
    with io.open(join(dir_name, source_file), 'w') as source:
        # Test a python line
        source.write(u'from x import y\n')

        # Test a lines which continues with a \  --they should be merged
        source.write(u'from z import a, \\ \n')
        source.write(u'b, \\ \n')
        source.write(u'c \n')

        # Test a single-line doc string  --it should be skipped
        source.write(u'"""Single line-doc string with double-quotes."""\n')
        source.write(u"'''Single line-doc string with single-quotes.'''\n")

        # Test a multi-line doc string  --they should be skipped
        source.write(u'""" Multi-line \n')
        source.write(u'doc string \n')
        source.write(u'with double-quotes.\n')
        source.write(u'"""\n')

        source.write(u"''' Multi-line \n")
        source.write(u"doc string \n")
        source.write(u"with single-quotes.\n")
        source.write(u"'''\n")

        # Test comment lines  --it should be skipped
        source.write(u'    # This is a comment\n')

        # Test code lines with comments,
        # these will not be stripped by statement but rather by transformation
        source.write(u'    some_func(x)  # Comment\n')

        # Test skip platform block
        source.write(u'    # {+android}\n')
        source.write(u'    android_func(x)\n')
        source.write(u'    # {-android}\n')

        # Keep kivy directives
        source.write(u'#: scenario xyz\n')

        # Treat line continuation with parens  --they should be merged
        source.write(u'    row = get(\n')
        source.write(u'        dist_id if dist_id\n')
        source.write(u'        else var.dist.id)\n')

        # Treat lines with parens in quotes  --parens should be ignored
        source.write(u'this "( should be a complete line("\n')
        source.write(u"...as ')' should this')'\n")

        # Treat multiline triple-quoted variable strings as strings
        source.write(u'x = """ Multi-line \n')
        source.write(u'string \n')
        source.write(u'with double-quotes.\n')
        source.write(u'"""\n')  # End with stand-alone quotes

        source.write(u"x =''' Multi-line \n")
        source.write(u"string \n")
        source.write(u"with single-quotes.'''\n")  # End with quotes at end

        # Treat multiline triple-quoted strings as strings
        source.write(u'"""\n')
        source.write(u'Multi-line \n')
        source.write(u'string \n')
        source.write(u'with double-quotes.\n')
        source.write(u'"""\n')

        source.write(u"'''\n")
        source.write(u"Multi-line \n")
        source.write(u"string \n")
        source.write(u"with single-quotes.'''\n")

    #
    # Read source file for iOS platform (should skip android lines)
    #
    get_statement_gen = source_statement_gen(source_file, dir_name,
                                             platform='iOS')
    assert get_statement_gen.next() == (u'from x import y', False)
    assert get_statement_gen.next() == (u'from z import a,  b,  c', False)
    assert get_statement_gen.next() == \
        (u'    some_func(x)  # Comment', False)
    assert get_statement_gen.next() == \
        (u'#: scenario xyz', False)
    assert get_statement_gen.next() == \
        (u'    row = get( dist_id if dist_id else var.dist.id)', False)
    assert get_statement_gen.next() == \
        (u'this "( should be a complete line("', False)
    assert get_statement_gen.next() == \
        (u"...as ')' should this')'", False)

    # Quote variable string
    assert get_statement_gen.next() == \
        (u'x = """ Multi-line', False)
    assert get_statement_gen.next() == \
        (u'string', False)
    assert get_statement_gen.next() == \
        (u'with double-quotes.', False)
    assert get_statement_gen.next() == \
        (u'"""', False)
    assert get_statement_gen.next() == \
        (u"x =''' Multi-line", False)
    assert get_statement_gen.next() == \
        (u"string", False)
    assert get_statement_gen.next() == \
        (u"with single-quotes.'''", False)

    # Quote string
    assert get_statement_gen.next() == \
        (u'"""', True)
    assert get_statement_gen.next() == \
        (u'Multi-line', True)
    assert get_statement_gen.next() == \
        (u'string', True)
    assert get_statement_gen.next() == \
        (u'with double-quotes.', True)
    assert get_statement_gen.next() == \
        (u'"""', True)
    assert get_statement_gen.next() == \
        (u"'''", True)
    assert get_statement_gen.next() == \
        (u"Multi-line", True)
    assert get_statement_gen.next() == \
        (u"string", True)
    assert get_statement_gen.next() == \
        (u"with single-quotes.'''", True)
    with pytest.raises(StopIteration):
        assert get_statement_gen.next()

    #
    # Read source file for android platform (should include android lines)
    #
    get_statement_gen = source_statement_gen(
        source_file, dir_name, platform='android')
    assert get_statement_gen.next() == (u'from x import y', False)
    assert get_statement_gen.next() == (u'from z import a,  b,  c', False)
    assert get_statement_gen.next() == \
        (u'    some_func(x)  # Comment', False)
    assert get_statement_gen.next() == \
        (u'    android_func(x)', False)
    assert get_statement_gen.next() == \
        (u'#: scenario xyz', False)
    assert get_statement_gen.next() == \
        (u'    row = get( dist_id if dist_id else var.dist.id)', False)
    assert get_statement_gen.next() == \
        (u'this "( should be a complete line("', False)
    assert get_statement_gen.next() == \
        (u"...as ')' should this')'", False)

    # Quote variable string
    assert get_statement_gen.next() == \
        (u'x = """ Multi-line', False)
    assert get_statement_gen.next() == \
        (u'string', False)
    assert get_statement_gen.next() == \
        (u'with double-quotes.', False)
    assert get_statement_gen.next() == \
        (u'"""', False)
    assert get_statement_gen.next() == \
        (u"x =''' Multi-line", False)
    assert get_statement_gen.next() == \
        (u"string", False)
    assert get_statement_gen.next() == \
        (u"with single-quotes.'''", False)

    # Quote string
    assert get_statement_gen.next() == \
        (u'"""', True)
    assert get_statement_gen.next() == \
        (u'Multi-line', True)
    assert get_statement_gen.next() == \
        (u'string', True)
    assert get_statement_gen.next() == \
        (u'with double-quotes.', True)
    assert get_statement_gen.next() == \
        (u'"""', True)
    assert get_statement_gen.next() == \
        (u"'''", True)
    assert get_statement_gen.next() == \
        (u"Multi-line", True)
    assert get_statement_gen.next() == \
        (u"string", True)
    assert get_statement_gen.next() == \
        (u"with single-quotes.'''", True)
    with pytest.raises(StopIteration):
        get_statement_gen.next()


    #
    # Read source file for default platform (should include android lines)
    #
    get_statement_gen = source_statement_gen(
        source_file, dir_name)
    assert get_statement_gen.next() == (u'from x import y', False)
    assert get_statement_gen.next() == (u'from z import a,  b,  c', False)
    assert get_statement_gen.next() == \
           (u'    some_func(x)  # Comment', False)
    assert get_statement_gen.next() == \
           (u'    android_func(x)', False)
    assert get_statement_gen.next() == \
           (u'#: scenario xyz', False)
    assert get_statement_gen.next() == \
           (u'    row = get( dist_id if dist_id else var.dist.id)', False)
    assert get_statement_gen.next() == \
           (u'this "( should be a complete line("', False)
    assert get_statement_gen.next() == \
           (u"...as ')' should this')'", False)

    # Quote variable string
    assert get_statement_gen.next() == \
           (u'x = """ Multi-line', False)
    assert get_statement_gen.next() == \
           (u'string', False)
    assert get_statement_gen.next() == \
           (u'with double-quotes.', False)
    assert get_statement_gen.next() == \
           (u'"""', False)
    assert get_statement_gen.next() == \
           (u"x =''' Multi-line", False)
    assert get_statement_gen.next() == \
           (u"string", False)
    assert get_statement_gen.next() == \
           (u"with single-quotes.'''", False)

    # Quote string
    assert get_statement_gen.next() == \
           (u'"""', True)
    assert get_statement_gen.next() == \
           (u'Multi-line', True)
    assert get_statement_gen.next() == \
           (u'string', True)
    assert get_statement_gen.next() == \
           (u'with double-quotes.', True)
    assert get_statement_gen.next() == \
           (u'"""', True)
    assert get_statement_gen.next() == \
           (u"'''", True)
    assert get_statement_gen.next() == \
           (u"Multi-line", True)
    assert get_statement_gen.next() == \
           (u"string", True)
    assert get_statement_gen.next() == \
           (u"with single-quotes.'''", True)
    with pytest.raises(StopIteration):
        get_statement_gen.next()


def test_get_source_statements_multiple_parens(tmpdir):
    dir_name = str(tmpdir.mkdir('source'))
    source_file = 'app.py'
    # Test with adjacent single quotes
    with io.open(join(dir_name, source_file), 'w') as source:
        # Test a python line
        source.write(u"class ValidationError(Exception):\n")
        source.write(u"def __init__(self, message='', title=_('Error')):\n")
        source.write(u"self.message = message\n")
        source.write(u"self.title = title\n")
    get_statement_gen = source_statement_gen(
        source_file, dir_name)
    assert get_statement_gen.next() == (
        u"class ValidationError(Exception):", False)
    assert get_statement_gen.next() == (
        u"def __init__(self, message='', title=_('Error')):", False)
    assert get_statement_gen.next() == (u"self.message = message", False)
    assert get_statement_gen.next() == (u"self.title = title", False)

    # Test with quoted parens
    with io.open(join(dir_name, source_file), 'w') as source:
        # Test a python line
        source.write(u"self.lpar = Literal('(').suppress()\n")
        source.write(u"self.rpar = Literal(')').suppress()\n")
    get_statement_gen = source_statement_gen(source_file, dir_name)
    assert get_statement_gen.next() == (
        u"self.lpar = Literal('(').suppress()", False)
    assert get_statement_gen.next() == (
        u"self.rpar = Literal(')').suppress()", False)
    with pytest.raises(StopIteration):
        get_statement_gen.next()
