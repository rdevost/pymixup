from peewee import DoesNotExist
from pyparsing import Literal, Optional, ZeroOrMore

from logic.obfuscatefile import ObfuscateBNF
from logic.reserved import add_reserveds, get_reserved_by_name
from logic.utilities import obfuscate_path


class ObfuscatePythonBNF(ObfuscateBNF):
    def __init__(self, get_obfuscated):
        """BNF grammar for Python source statements.

        Parameters
        ----------
        get_obfuscated : function
            Function to return the obfuscated name for an identifier.
        """
        super(ObfuscatePythonBNF, self).__init__(get_obfuscated)

        self.validator = \
            Literal('@') + \
            Literal('validate') + \
            Literal('(') + \
            self.string + \
            self.string + \
            Literal(')')

        # Parse a Kivy load_file statement
        self.builder = \
            Literal('Builder.load_file(') + \
            self.string + \
            Literal(')')

        self.statement = (
            ZeroOrMore(
                (self.directive |
                 self.builder |
                 self.tab |
                 self.conseq_idents_numbs |
                 self.separator |
                 self.string_or_doc |
                 self.triple_quote)
                ) + Optional(self.comment).suppress()
            )

        self.except_error = (
            ZeroOrMore(
                (self.tab.suppress() |
                 Literal('except') |
                 self.directive.suppress() |
                 self.tab.suppress() |
                 self.ident |
                 self.separator.suppress() |
                 self.fnumber.suppress() |
                 self.string_or_doc.suppress() |
                 self.triple_quote.suppress())
                ) + Optional(self.comment).suppress()
            )

        self.from_import = (
            ZeroOrMore(
                (self.tab.suppress() |
                 Literal('from') |
                 self.directive.suppress() |
                 self.tab.suppress() |
                 self.ident |
                 Literal('import') |
                 self.separator.suppress() |
                 self.fnumber.suppress() |
                 self.string_or_doc.suppress() |
                 self.triple_quote.suppress())
                ) + Optional(self.comment).suppress()
            )

        self.except_error.setParseAction(self.add_except_error)
        self.builder.setParseAction(self.transform_builder)
        self.from_import.setParseAction(self.add_from_import)

    ###############
    # Parse actions
    ###############
    def add_from_import(self, from_import_list):
        """Add imported modules from reserved modules to reserved.

        Parameters
        ----------
        from_import_list : list
        """
        if not from_import_list or \
                from_import_list[0] != 'from' or \
                'import' not in from_import_list[:]:
            return

        reserved_list = set()
        import_index = from_import_list[:].index('import')
        package_name = ''
        is_reserved = False
        for reserve_name in from_import_list[1:import_index]:
            # Start with first reserved directory in tree (if one exists)
            if not is_reserved:
                try:
                    get_reserved_by_name(reserve_name)
                    is_reserved = True
                    package_name = reserve_name
                except DoesNotExist:
                    continue
            if is_reserved:
                if reserve_name[0].isalpha() or reserve_name[0] == '_':
                    reserved_list.add(reserve_name)

        if is_reserved:
            # Get imported items
            for reserve_name in from_import_list[import_index+1:]:
                if reserve_name[0].isalpha() or reserve_name[0] == '_':
                    reserved_list.add(reserve_name)
            add_reserveds(package_name, reserved_list)

    def add_except_error(self, except_error_list):
        """Add except Error names to reserved.

        Parameters
        ----------
        except_error_list : list
        """
        if not except_error_list or except_error_list[0] != 'except':
            return

        reserved_list = set()
        package_name = 'Except'
        for reserve_name in except_error_list[1:]:
            if reserve_name == 'as':
                break
            if reserve_name[0].isalpha() or reserve_name[0] == '_':
                reserved_list.add(reserve_name)
        if reserved_list:
            add_reserveds(package_name, reserved_list)

    def transform_builder(self, builder_list):
        """Parse a Kivy load_file statement.

        Parameters
        builder_list : list
            Kivy Builder.load_file statement.
        """
        return ''.join([
            builder_list[0],
            "'",
            obfuscate_path(builder_list[1].strip("'")),
            "'",
            builder_list[2]
            ])
