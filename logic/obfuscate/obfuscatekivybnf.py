from pyparsing import Literal, Optional, ZeroOrMore
from peewee import DoesNotExist

from logic.obfuscate import ObfuscateBNF
from logic.reserved import get_reserved_by_name, add_reserveds


class ObfuscateKivyBNF(ObfuscateBNF):
    def __init__(self, get_obfuscated):
        """BNF grammar for Kivy source statements.

        Parameters
        ----------
        get_obfuscated : function
            Function to return the obfuscated name for an identifier.
        """
        super(ObfuscateKivyBNF, self).__init__(get_obfuscated)

        self.kivy_import = (
            ZeroOrMore(
                (self.directive |
                 Literal('import') |
                 self.ident |
                 self.separator.suppress() |
                 self.fnumber.suppress() |
                 self.string.suppress()
                ) + Optional(self.comment).suppress()
            ))

        self.kivy_import.setParseAction(self.add_kivy_import)

    ###############
    # Parse actions
    ###############
    def add_kivy_import(self, kivy_import_list):
        """Add imported modules from reserved modules to reserved.

        Parameters
        ----------
        kivy_import_list : list
            Kivy import statement.
        """
        if not kivy_import_list or \
                kivy_import_list[0].strip() != '#:' or \
                kivy_import_list[1] != 'import':
            return

        reserved_list = set()
        package_name = ''
        is_reserved = False
        for reserve_name in kivy_import_list[3:]:
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
            reserved_list.add(kivy_import_list[2])
            add_reserveds(package_name, reserved_list)
