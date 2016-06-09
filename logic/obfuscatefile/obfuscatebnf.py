import abc

from pyparsing import alphanums, alphas, Combine, Literal, nums, oneOf, \
    OneOrMore, Optional, pythonStyleComment, QuotedString, Word, ZeroOrMore
from peewee import DoesNotExist

from logic.identifier import add_identifiers
from logic.reserved import add_reserveds, get_reserved_by_name


class ObfuscateBNF(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, get_obfuscated):
        """BNF grammar for source statements.

        Parameters
        ----------
        get_obfuscated : function
            Function to return the obfuscated name for an identifier.
        """
        self.get_obfuscated = get_obfuscated

        self.directive = oneOf("#:")
        self.comment = ~self.directive + pythonStyleComment

        self.separator = Word("~!@$%^&*()+`-={}|[]:;<>?,/.", max=2)

        self.string = \
            QuotedString(quoteChar='"', escChar='\\', multiline=False,
                         unquoteResults=False) |\
            QuotedString(quoteChar="'", escChar='\\', multiline=False,
                         unquoteResults=False)

        self.doc_string = \
            QuotedString(quoteChar='"""', escChar='\\', multiline=True,
                         unquoteResults=False) |\
            QuotedString(quoteChar="'''", escChar='\\', multiline=True,
                         unquoteResults=False)
        self.string_or_doc = self.doc_string | self.string
        self.triple_quote = Literal("'''") | Literal('"""')

        self.e = Literal('E') | Literal('e')
        self.point = Literal('.')

        self.plusorminus = Literal('+') | Literal('-')
        self.number = Word(nums)
        self.integer = Combine(Optional(self.plusorminus) + self.number)
        self.fnumber = Combine(
            self.integer +
            Optional(self.point + Optional(self.number)) +
            Optional(self.e + self.integer))

        self.tab = Literal('    ')

        self.ident = Word(alphas+'_', alphanums+'_')
        self.conseq_idents_numbs = OneOrMore(self.ident | self.fnumber)
        self.attrib = self.ident + OneOrMore('.'+self.ident)

        self.statement = (
            ZeroOrMore(
                (self.directive |
                 self.tab |
                 self.conseq_idents_numbs |
                 self.separator |
                 self.string_or_doc |
                 self.triple_quote)
            ) + Optional(self.comment).suppress()
        )

        self.attribs = (
            ZeroOrMore(
                (self.directive.suppress() |
                 self.tab.suppress() |
                 self.attrib |
                 self.ident.suppress() |
                 self.separator.suppress() |
                 self.fnumber.suppress() |
                 self.string_or_doc.suppress() |
                 self.triple_quote.suppress())
            ) + Optional(self.comment).suppress()
        )

        self.conseq_idents = (
            ZeroOrMore(
                (self.directive.suppress() |
                 self.tab.suppress() |
                 self.ident |
                 self.separator.suppress() |
                 self.fnumber.suppress() |
                 self.string.suppress())
            ) + Optional(self.comment).suppress()
        )

        self.conseq_idents_no_obfuscate = (
            ZeroOrMore(
                (self.directive.suppress() |
                 self.tab.suppress() |
                 self.ident |
                 self.separator.suppress() |
                 self.fnumber.suppress() |
                 self.string_or_doc.suppress() |
                 self.triple_quote.suppress())
            ) + Optional(self.comment).suppress()
        )

        self.attribs.setParseAction(self.add_attribs_reserveds)
        self.conseq_idents.setParseAction(self.add_conseq_idents)
        self.conseq_idents_no_obfuscate.setParseAction(
            self.add_conseq_idents_no_obfuscate)
        self.conseq_idents_numbs.setParseAction(
            self.transform_conseq_ident_numbs)
        self.directive.setParseAction(self.transform_directive)

    ###############
    # Parse actions
    ###############
    def add_conseq_idents(self, conseq_idents_list):
        """Add names to obfuscate to identifiers table.

        Parameters
        ----------
        conseq_idents_list : list
        """
        if 'import' not in conseq_idents_list[:] and \
                'except' not in conseq_idents_list[:]:
            add_identifiers(set(conseq_idents_list))

    def add_conseq_idents_no_obfuscate(
            self, conseq_idents_no_obfuscate_list):
        """Add names that are not obfuscated to identifiers table.

        Parameters
        ----------
        conseq_idents_no_obfuscate_list : list
        """
        # If an except error was not added to reserved list, don't obfuscate it
        if 'import' not in conseq_idents_no_obfuscate_list[:] and \
                'except' not in conseq_idents_no_obfuscate_list[:]:
            add_identifiers(set(conseq_idents_no_obfuscate_list),
                            do_obfuscate=False)

    def add_attribs_reserveds(self, attribs_list):
        """Add attributes of reserved names to reserved list.

        Take a list of attributes strings from a source statement, break
        it into lists of objects with their attributes, and add attributes
        that follow a reserved name to the reserved list.

        Example
         ------
         If r is reserved, then
            a.r.c + d.r.e
        would add c and e to reserveds.

        Parameters
        ----------
        attribs_list : list
        """
        if attribs_list:
            # Create an ordered list of attribute parents
            # Ex. a.b.c => [a, b]
            _attrib_list = [attribs_list[0]]
            is_last_token_an_attrib = True
            for token in attribs_list[1:]:
                if is_last_token_an_attrib and token != '.':
                    # End of attrib list reached. Process list.
                    add_attribs_reserveds_list(_attrib_list)
                    # Start new attrib list
                    _attrib_list = [token]
                    is_last_token_an_attrib = True
                elif is_last_token_an_attrib and token == '.':
                    is_last_token_an_attrib = False
                elif not is_last_token_an_attrib and token == '.':
                    continue  # Multiple dots, continue attrib list
                elif not is_last_token_an_attrib and token != '.':
                    _attrib_list.append(token)
                    is_last_token_an_attrib = True
            else:
                # Process last list
                if _attrib_list:
                    add_attribs_reserveds_list(_attrib_list)

    def transform_conseq_ident_numbs(self, conseq_ident_list):
        """Allow for non-name tokens in a statement.

        Names start with an alpha or underscore. Obfuscate these name tokens
        and simply copy unchanged other tokens.

        Parameters
        ----------
        conseq_ident_list : list

        Returns
        -------
        statement : str
        """
        return ' '.join([
            self.get_obfuscated(ident) if
            (ident[0].isalpha() or ident[0] == '_') else ident
            for ident in conseq_ident_list
        ])

    def transform_directive(self, directive_list):
        """Create a directive statement."""
        return ''.join([directive_list[0], ' '])


def add_attribs_reserveds_list(attrib_list):
    """Add attributes that follow a reserved name to reserveds list."""
    if len(attrib_list) > 1:  # A single item does not change
        is_reserved = False
        reserved_set = set()
        for name in attrib_list:
            if not is_reserved:
                try:
                    get_reserved_by_name(name)
                    is_reserved = True
                    package_name = name
                    continue  # Don't add already reserved name
                except DoesNotExist:
                    continue
            if is_reserved:
                reserved_set.add(name)
        if reserved_set:
            add_reserveds(package_name, reserved_set)
