from collections import defaultdict
from functools import wraps
import logging
from os import environ
from os.path import join, isdir

from fabric.api import local
import peewee as pwe

from common.settings import obfuscated_dir, project_name


logging.debug('data.base: Starting')
###############
# Connect to db
###############
# Note: This module is loaded as part of the pymixup.py initialization.
#       Therefore, is run before the parsing of the command-line options,
#       which specifies the platform. So, the build and use of the db uses
#       a db folder under the project name, not the platform.
if 'IS_PYMIXUP_TEST' in environ and environ['IS_PYMIXUP_TEST'] in (1, '1'):
    obfuscatedb = pwe.SqliteDatabase(':memory:', autocommit=False)
else:
    to_dir = join(obfuscated_dir, project_name)
    if not isdir(to_dir):
        local(' '.join(['mkdir', to_dir]))
    if not isdir(join(to_dir, 'db')):
        local(' '.join(['mkdir', join(to_dir, 'db')]))
    obfuscatedb = pwe.SqliteDatabase(join(obfuscated_dir,
                                          project_name,
                                          'db/obfuscate.db'))


######################
# Validation decorator
######################
def validate(model, field):
    """Decorator to add validation methods to validation_fields dictionary.

    Populate validation_fields dictionary. The key/value pair is made up of
    the model (table) name and tuples field name and the method to run.

    For example,
        {'table_1': [('field_1', 'method_1'), ('field_2', 'method_2'), ...],
         'table_A': [('field_a', 'method_a'), ('field_b', 'method_b'), ...],
        }

    Parameters
    ----------
    field : str
    model : str
    """
    def _validate(validation_method):
        try:
            validate.validation_fields[model].append(
                (field, validation_method.__name__))
        except AttributeError:
            validate.validation_fields = defaultdict(list)
            validate.validation_fields[model].append(
                (field, validation_method.__name__))

        @wraps(validation_method)
        def wrapped(self):
            return validation_method(self)
        return wrapped

    return _validate


#####################
# Extend peewee Model
#####################
class BaseModel(pwe.Model):
    """Add field-level validation to the Peewee ORM."""
    def validate_fields(self):
        """Validate model fields."""
        fields = validate.validation_fields.get(self.__class__.__name__, None)
        try:
            for field, method in fields:
                try:
                    getattr(self, method)()
                except AssertionError:
                    raise
        except TypeError:
            pass

    def save(self, *args, **kwargs):
        """Validate fields then save record."""
        self.validate_fields()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = obfuscatedb
