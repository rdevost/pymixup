from collections import namedtuple

import peewee as pwe

from data.base import BaseModel, validate


############################
# Reserved folders and files
############################
# Leading special characters:
#     / = reserved directory, copy as is
#     ~ = reserved file, copy as is
#     # = non-obfuscated directory: run through obfuscator to pick up other
#         other module's obfuscated names, but treat the
#         names as reserved
#     = = non-obfuscated file: run through obfuscator, but treat all names
#         as reserved
ReservedPrefixes = namedtuple('ReservedPrefixes', ['reserved_dir',
                                                   'reserved_file',
                                                   'non_obfuscated_dir',
                                                   'non_obfuscated_file'])
reserved_prefixes = ReservedPrefixes('/', '~', '#', '=')


class Reserved(BaseModel):
    """ORM for a name."""
    import datetime
    id = pwe.PrimaryKeyField()
    name = pwe.CharField(default=u'', index=True, unique=True)
    primary_package = pwe.CharField(default=u'')
    created_timestamp = pwe.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'reserved'

    @validate('Reserved', 'name')
    def validate_name(self):
        if not self.name:
            raise AssertionError('Name must be given.')
