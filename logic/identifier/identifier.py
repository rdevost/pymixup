import datetime

import peewee as pwe

from data.base import BaseModel, validate
from logic.randomize import base_alphabet_encode, base_random_number
from logic.reserved import get_reserved_by_name


class Identifier(BaseModel):
    """Identifier database table."""
    id = pwe.PrimaryKeyField()
    name = pwe.CharField(default=u'', index=True, unique=True)
    obfuscated_name = pwe.CharField(default=u'', index=True, unique=True)
    obfuscated_lower = pwe.CharField(default=u'', index=True)
    created_timestamp = pwe.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'identifier'

    @validate('Identifier', 'name')
    def validate_name(self):
        """Validate the identifier name."""
        if not self.name:
            raise AssertionError('Name must be given.')

    @validate('Identifier', 'obfuscated_name')
    def validate_obfuscated_name(self):
        """Make sure the obfuscated name is unique."""
        if self.name != self.obfuscated_name:
            is_unique = False
            while not is_unique:
                if not self.obfuscated_name:
                    random_num = base_random_number(5)
                    self.obfuscated_name = base_alphabet_encode(random_num, 5)
                try:
                    get_reserved_by_name(self.obfuscated_name)
                except pwe.DoesNotExist:
                    is_unique = True
                else:
                    self.obfuscated_name = None

    @validate('Identifier', 'obfuscated_lower')
    def validate_obfuscated_lower(self):
        """Store lowercase value of the obfuscated name."""
        self.obfuscated_lower = self.obfuscated_name.lower()
