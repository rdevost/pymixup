from __future__ import print_function
from distutils.dir_util import mkpath
from io import open
from os.path import join, split, isdir
import re
import sys

from logic.coroutine import coroutine
from logic.identifier import add_identifiers, search_identifiers
from logic.reserved import search_reserveds
from logic.utilities import obfuscate_path, to_unicode


def obfuscate_file(bnf_parser, source_file, from_dir, from_sub_dir, to_dir,
                   is_verbose=False, is_discovery=True, is_python=True,
                   do_obfuscate=True, platform=None):
    """Obfuscate a file.

    Parameters
    ----------
    bnf_parser
    do_obfuscate: bool
    from_dir : str
    from_sub_dir
    is_discovery : bool
    is_python : bool
    is_verbose : bool
    platform : str
        Destination platform for obfuscated file.
    source_file : str
    to_dir
    """
    # Setup output file or std output
    if to_dir:
        to_file_path = join(to_dir, from_sub_dir, source_file)
    else:
        to_file_path = None
    fh = source_gen(to_dir, from_sub_dir, source_file)

    num_reserved = 0
    num_identifiers = 0
    if is_discovery:
        num_reserved = search_reserveds(None).count()
        num_identifiers = search_identifiers(None).count()
        add_identifiers([source_file[:-3]])

    for statement, is_literal_string in source_statement_gen(
            source_file, from_dir, platform=platform):
        if is_discovery and not is_literal_string:
            if is_python:
                # Add reserved attributes to reserveds
                bnf_parser.attribs.parseString(statement)
                # Add imports and except names to reserveds
                bnf_parser.from_import.parseString(statement)
                bnf_parser.except_error.parseString(statement)
            else:
                bnf_parser.kivy_import.parseString(statement)
            # Add non-obfuscated idents to identifier
            if do_obfuscate:
                bnf_parser.conseq_idents.parseString(statement)
            else:
                bnf_parser.conseq_idents_no_obfuscate.parseString(
                    statement)
            continue

        if is_literal_string:
            modified_statement = statement
        else:
            modified_statement = bnf_parser.statement.transformString(
                statement)
        # Output source_statement
        if not to_file_path and modified_statement != statement and \
                is_verbose:
            print(statement)
            print(modified_statement)
        fh.send(modified_statement + '\n')
        if not to_file_path and modified_statement != statement and \
                is_verbose:
            print('----')
    if is_discovery:
        num_reserved_added = search_reserveds(None).count() - num_reserved
        num_identifiers_added = \
            search_identifiers(None).count() - num_identifiers
        print('Added {} reserved, {} identifiers'.format(
            str(num_reserved_added), str(num_identifiers_added)), end=' ... ')


def source_statement_gen(source_file, dir_name, platform=None):
    """Get a complete source statement.

    Notes
    -----
    1. Skip doc strings and comment lines.
    2. Remove end-of-line comments.
    3. Combine multi-line statements into a single-line statement.
    4. Pass through triple-quoted strings.

        a. Pass unchanged multi-line triple-quote strings that start with
            a stand-alone triple quote.
        b. Pass as a single statement triple-quoted lines that start with
            something other than a triple quote (e.g., starts with a variable
            assignment).

    Parameters
    ----------
    dir_name
    platform : str
        Destination platform of obfuscated file.
    source_file
    """

    is_end_of_statement = True
    is_current_platform = True
    is_doc_string = False
    is_quote_string = False
    is_end_of_quote_string = False
    is_quote_variable = False
    is_end_of_quote_variable = False
    source_statement = ''
    num_open_parens = 0
    for source_line in source_line_gen(source_file, dir_name):
        # Skip doc strings
        #   1. If line starts with triple-quote:
        #       a. If part of a continuing docstring, end of docstring, skip
        #       b. If ends with another triple-quote, single line docs., skip
        #       c. If nothing else on line, then is string, keep
        #       d. If followed by other than triple-quote, new docstring, skip
        #   2. If line ends with triple-quote:
        #       a. If part of continuing docstring, end of docstring, skip
        #       b. Otherwise, part of quoted string, keep
        #   3. If docstring, skip
        is_literal_string = False
        try:
            if source_line.strip()[0:3] in ['"""', "'''"]:
                if is_doc_string:
                    # Is end of docstring
                    is_doc_string = False
                    continue
                else:
                    if source_line.strip()[-3:] in ['"""', "'''"]:
                        if len(source_line.strip()) >= 6:
                            # Is single line docstring
                            continue
                        else:
                            # Is last line of string or starting new string
                            pass
                    else:
                        # Is new multi-line docstring
                        is_doc_string = True
                        continue
        except IndexError:
            pass

        if is_doc_string:
            continue

        # Pass unchanged quote strings
        if is_quote_string or is_quote_variable:
            if source_line.strip()[-3:] in ['"""', "'''"]:
                is_end_of_quote_string = True
                is_end_of_quote_variable = True
        else:
            if source_line.strip()[:3] in ['"""', "'''"]:
                is_quote_string = True
            else:
                if '"""' in source_line or "'''" in source_line:
                    is_quote_variable = True
        if is_quote_string:
            source_statement = source_line.rstrip()

        elif source_line.strip().startswith('def test_'):
            source_statement = source_line.rstrip()
            is_literal_string = True

        else:
            # Skip platform directive blocks
            if source_line.strip().startswith('# {-'):
                is_current_platform = True
                continue
            if source_line.strip().startswith('# {+'):
                if platform and source_line.strip() != ''.join([
                        '# {+',
                        platform,
                        '}']):
                    is_current_platform = False
                continue
            if not is_current_platform:
                continue

            # Skip comment lines, keep kivy directives
            if source_line.strip().startswith('#') and \
                    not source_line.strip().startswith('#:'):
                continue

            if is_end_of_statement:
                source_statement = ''
                num_open_parens = 0

            if not source_statement:
                source_statement += source_line.rstrip()  # Strip only right
            else:
                source_statement += ''.join([' ', source_line.strip()])

            # Determine if line is continued
            # Don't count paren within quotes, so
            # remove adjacent quote marks and contents between quotes
            non_quoted_source = re.sub('\'[^\']+\'', '',
                                       re.sub('\"[^\"]+\"', '',
                                              re.sub("\'\'", '',
                                                     re.sub('\"\"', '',
                                                            source_line))))
            num_open_parens += non_quoted_source.count('(')
            num_open_parens += non_quoted_source.count('[')
            num_open_parens += non_quoted_source.count('{')

            num_open_parens -= non_quoted_source.count(')')
            num_open_parens -= non_quoted_source.count(']')
            num_open_parens -= non_quoted_source.count('}')

            if num_open_parens or source_line.endswith('\\'):
                is_end_of_statement = False
                source_statement = source_statement.rstrip('\\')
                continue

        # Yield a statement
        is_end_of_statement = True
        # Quote strings are also literal
        if is_quote_string:
            is_literal_string = True
        yield source_statement, is_literal_string
        if is_end_of_quote_string or is_end_of_quote_variable:
            is_quote_string = False
            is_end_of_quote_string = False
            is_quote_variable = False
            is_end_of_quote_variable = False


def source_line_gen(source_file, dir_name):
    """Read a source file.

    Parameters
    ----------
    dir_name
    source_file

    Yields
    ------
    line : source line
    """
    with open(join(dir_name, source_file), 'r', newline='\n',
              encoding='utf-8') as source:
        for line in source:
            yield line.rstrip()


@coroutine
def source_gen(to_dir, from_sub_dir, source_file=None):
    """Write to a file or stdout.

    Parameters
    ----------
    from_sub_dir : str
    source_file : str
    to_dir : str

    Yields
    ------
    line : source line
    """
    if to_dir:
        obf_path = obfuscate_path(join(from_sub_dir, source_file))
        basepath, filename = split(obf_path)
        to_basepath = join(to_dir, basepath)
        if not isdir(to_basepath):
            mkpath(to_basepath)
        to_obf_path = join(to_basepath, filename)
        fh = open(to_obf_path, 'w', encoding='utf-8')
    else:
        fh = sys.stdout

    while True:
        line = yield
        fh.write(to_unicode(line))
