import keyword
from logging import getLogger
from os import mkdir
from os.path import join, exists

import peewee as pwe
import pyparsing
import sqlite3

from logic.reserved import add_reserveds, Reserved, reserved_prefixes
from logic.identifier import add_identifiers, Identifier

logger = getLogger(__name__)


def build_db(db_dir):
    """Build the initial obfuscation database.

    Parameters
    ----------
    db_dir : str
        Directory for the database.
    """
    from data.base import obfuscatedb

    logger.info('Obfuscate.build.build_db: Starting')
    try:
        obfuscatedb.close()
    except AttributeError:  # No db
        pass

    # Create db path and file
    if not exists(db_dir):
        mkdir(db_dir)
    obfuscatedb_path = join(db_dir, 'obfuscate.db')
    logger.info(
        'Obfuscate.build.build_db: Building db {}'.format(obfuscatedb_path))

    conn = sqlite3.connect(obfuscatedb_path)
    conn.execute('PRAGMA auto_vacuum = 1')
    conn.execute('PRAGMA journal_mode = WAL')
    conn.execute('PRAGMA foreign_keys = ON')
    conn.commit()
    conn.close()

    obfuscatedb = pwe.SqliteDatabase(obfuscatedb_path)

    logger.info('Obfuscate.build.build_db: Built')

    obfuscatedb.create_tables([
        Identifier,
        Reserved
    ], safe=True)

    ##################################################
    # Populate Identifiers with names not to obfuscate
    ##################################################
    # Non-obfuscating identifiers are less restrictive than reserveds,
    # they do not cause their attributes to become reserved.
    # Note: Although self is not a Python reserved word, Kivy treats it like
    #       one.
    identifiers_list = [
        'args',
        'kwargs',
        'self',
        'tests',
    ]
    add_identifiers(identifiers_list, do_obfuscate=False)

    #####################################
    # Populate reserved folders and files
    #####################################
    # Add reserved directories (directory will be prefixed with '/')
    reserved_list = [
        'csvlite',
        'db',
        'docutils',
        'fonts',
        'help',
        'images',
        'initial_data',
        'international',
        'kivygraph',
        'pyparsing',
    ]
    add_reserveds('directories', [reserved_prefixes.reserved_dir + name 
                                  for name in reserved_list])

    # Add reserved files (file will be prefixed with '~')
    reserved_list = [
        'peewee.py',
        'pytest.ini',
    ]
    add_reserveds('files', [reserved_prefixes.reserved_file + name 
                            for name in reserved_list])

    # Add directories to not obfuscate (package will be prefixed with '#')
    reserved_list = [
    ]
    add_reserveds('directories', [reserved_prefixes.non_obfuscated_dir + name 
                                  for name in reserved_list])

    # Add files to not obfuscate (file will be prefixed with '=')
    reserved_list = [
        'basicscreen_fmt.kv',
        'basicscreen_scr.py',
        'buttonbar_fmt.kv',
        'buttonbar_scr.py',
        'buttons_fmt.kv',
        'buttons_scr.py',
        'formattingbar_fmt.kv',
        'formattingbar_scr.py',
        'gradient.py',
        'header_fmt.kv',
        'header_scr.py',
        'inputboxes_fmt.kv',
        'inputboxes_scr.py',
        'textinputbuttons_fmt.kv',
        'textinputbuttons_scr.py',
        'textinputs.py',
        'textlabel_fmt.kv',
        'textlabel_scr.py',
    ]
    add_reserveds('files', [reserved_prefixes.non_obfuscated_file + name 
                            for name in reserved_list])

    #######################################
    # Populate reserved names for libraries
    #######################################
    # To reserve names:
    #   1. Populate reserved_list with the names to reserve, then
    #   2. add_reserveds('<package_name>', reserved_list), where
    #       <package_name> is the name you want to assign the package. This
    #       name is included in the Reserved table for reference.
    # Notes:
    #   1. The library's reserved names can be loaded either by individually
    #       listing them in reserved_list or by initially setting it to
    #       library.__all__ and then extending the list with other names.
    #       For example:
    #           reserved_list = some_library.__all__
    #           reserved.list.extend(['foo', 'bar'])
    #           add_reserveds('some_library', reserved_list)
    #   2. Even if using a library's __all__ dictionary, there may be other
    #       names that must also be reserved, in particular, parameter keywords
    #       that are used must be reserved. For example, if foo is in __all__
    #       and foo is called by foo(bar=some_value), then bar will need to
    #       be added to reserveds.
    #######################################
    reserved_list = [
    ]
    add_reserveds('__future__', reserved_list)

    reserved_list = [
        'getPath',
    ]
    add_reserveds('android', reserved_list)

    reserved_list = [
        'action', 'add_argument',
        'default', 'description', 'dest',
        'help',
        'nargs',
        'parse_args',
        'required',
    ]
    add_reserveds('argparse', reserved_list)

    reserved_list = [
    ]
    add_reserveds('contextlib', reserved_list)

    reserved_list = [
        '_csv',
        'delimiter', 'dialect',
        'excel',
        'fieldnames',
        'line_num',
        'quotechar', 'quoting',
        'read', 'readline',
        'seek', 'sniff',
        'writeheader', 'writerow', 'writerows',
    ]
    add_reserveds('csvlite', reserved_list)

    reserved_list = [
        'st_ctime', 'st_mtime', 'st_size',
    ]
    add_reserveds('datetime', reserved_list)

    reserved_list = [
    ]
    add_reserveds('distutils', reserved_list)

    reserved_list = [
    ]
    add_reserveds('docutils', reserved_list)

    reserved_list = [
    ]
    add_reserveds('fabric', reserved_list)

    reserved_list = [
    ]
    add_reserveds('functools', reserved_list)

    reserved_list = [
    ]
    add_reserveds('gc', reserved_list)

    reserved_list = [
        'hexdigest',
        'update',
    ]
    add_reserveds('hashlib', reserved_list)

    reserved_list = [
    ]
    add_reserveds('international', reserved_list)

    reserved_list = [
    ]
    add_reserveds('inspect', reserved_list)

    reserved_list = [
    ]
    add_reserveds('io', reserved_list)

    reserved_list = [
        'fillvalue',
        'iter',
        'next',
        'StopIteration',
    ]
    add_reserveds('itertools', reserved_list)

    reserved_list = [
        '_can_make_payments',
        'ACTION_SEND',
        'createChooser',
        'DIRECTORY_DOWNLOADS',
        'Environment', 'EXTRA_EMAIL', 'EXTRA_STREAM', 'EXTRA_SUBJECT',
        'EXTRA_TEXT',
        'fromFile',
        'getExternalStorageDirectory',
        'java_environment',
        'getExternalStoragePublicDirectory', 'getPath',
        'parse', 'platform_api', 'putExtra',
        'setType', 'setWithObject_', 'startActivity',
        'toString',
    ]
    add_reserveds('jnius', reserved_list)

    reserved_list = [
        'encoding', 'ensure_ascii',
        'readline',
        'sort_keys',
    ]
    add_reserveds('json', reserved_list)

    reserved_list = [
        '_create_popup', '_keyboard', '_keyboard_closed', '_on_keyboard_down',
        '_set_option', '_trigger_reset_populate', '_viewport',
        'adapter', 'add_json_panel', 'add_widget', 'after',
        'allow_stretch', 'allownone', 'args_converter',
        'auto_dismiss', 'available_products',
        'background_color', 'background_normal', 'bar_color',
        'bar_inactive_color', 'bar_pos_y', 'bar_width',
        'before', 'behaviors', 'bind', 'blit', 'blit_buffer', 'bold',
        'border', 'BorderImage',
        'buf', 'bufferfmt',
        'build', 'build_config', 'build_settings',
        'build_key_handler', 'build_post_init',
        'button_color',
        'canvas', 'children', 'clear_widgets',
        'close_settings', 'cls', 'collide_point', 'color',
        'Color', 'colorfmt', 'cols',
        'content', 'copy', 'create',
        'current', 'current_language', 'cut',
        'data', 'default_font', 'deselected_color', 'dicts', 'disable',
        'disabled', 'dismiss', 'do_scroll', 'do_scroll_x', 'do_scroll_y',
        'dpi', 'dpi2px', 'dt', 'dtype', 'dx', 'dy',
        'event',
        'figsize', 'filters',
        'focus', 'font', 'font_name', 'font_size', 'foreground_color',
        'foreground_normal', 'from_undo', 'fullscreen',
        'getter', 'go_back', 'goto', 'Gradient',
        'garden', 'get_running_app', 'grab', 'grab_current', 'group',
        'halign', 'height', 'hide_keyboard', 'hint_text', 'horizontal',
        'icon', 'id', 'Image', 'info', 'input_filter', 'input_type',
        'insert_text', 'instance', 'interface',
        'is_bold', 'item_strings',
        'key', 'keyboard', 'keyboard_height', 'keycode', 'keycode1',
        'keycode2',
        'LabelBase', 'language', 'languages', 'line_height',
        'line_spacing',
        'load_file',
        'manager', 'markup', 'maxfps', 'minimum_height', 'modifiers',
        'multiline', 'multiselect',
        'number',
        'on_available_products', 'on_config_change',
        'on_current_language',
        'on_double_tap', 'on_focus', 'on_key_down', 'on_keyboard',
        'on_pause', 'on_press', 'on_release', 'on_resume', 'on_selection',
        'on_selection_change', 'on_start', 'on_stop', 'on_text_validate',
        'on_touch_down', 'on_touch_up', 'opacity', 'open', 'open_settings',
        'options', 'orientation',
        'padding', 'padding_x', 'padding_y', 'parent', 'parent_object',
        'paste', 'pixels',
        'pos', 'pos_hint', 'put', 'px',
        'quit',
        'readonly', 'Rectangle', 'ref', 'register', 'RelativeLayout',
        'release', 'remove_widget', 'request_keyboard',
        'rgba', 'root', 'rootpath',
        'RstScroll', 'run',
        'schedule_once',
        'scroll_type', 'scrollcontent', 'scrolloptions',
        'section', 'select_all', 'select_list', 'selected_color',
        'selection', 'selection_color', 'separator_color', 'setdefaults',
        'setter', 'Settings', 'settings', 'settings_cls', 'shorten',
        'shorten_from', 'show_errors', 'show_hidden',
        'show_keyboard',  'size', 'size_hint', 'size_hint_x', 'size_hint_y',
        'source',  'sp', 'spacing', 'state',
        'SwapTransition',
        'text_size',
        'texture_size', 'title', 'title_size',
        'touch', 'transition',
        'uid', 'unbind', 'ungrab', 'use_kivy_settings', 'user_data_dir',
        'valign', 'value', 'vertical',
        'width', 'win',
        'x',
        'y',
    ]
    add_reserveds('kivy', reserved_list)

    reserved_list = [
        'add_plot',
        'points',
        'remove_plot',
        'x_grid', 'x_grid_label', 'x_ticks_major', 'x_ticks_minor',
        'xlabel', 'xmax', 'xmin',
        'y_grid', 'y_grid_label', 'y_ticks_major', 'y_ticks_minor',
        'ylabel', 'ymax', 'ymin',
    ]
    add_reserveds('kivygraph', reserved_list)

    reserved_list = [
        'abs', 'all', 'any', 'axis',
        'bins',
        'cmp',
        'decimals', 'density', 'dtype',
        'float',
        'int',
        'np',
        'when',
    ]
    add_reserveds('numpy', reserved_list)

    reserved_list = [
        'getcwd',
        'IOError',
        'OSError',
    ]
    add_reserveds('os', reserved_list)

    reserved_list = [
        '_meta',
        'add_column', 'add_index', 'autocommit', 'atomic',
        'begin',
        'close', 'column', 'commit', 'connect', 'count', 'create_tables',
        'database', 'db_column', 'db_table', 'default', 'delete_instance',
        'delete_nullable', 'drop_column', 'drop_tables',
        'False',
        'get', 'get_cursor',
        'index', 'indexes', 'iterator',
        'limit',
        'Meta', 'message', 'migrate', 'migrator',
        'name', 'null',
        'offset', 'on_delete', 'order_by',
        'playhouse', 'pwe',
        'recursive', 'rel_model', 'related_name', 'rollback',
        'safe', 'save', 'SqliteMigrator', 'sqlite3',
        'table', 'table_exists', 'to_field', 'transaction',
        'unique',
        'where',
    ]
    add_reserveds('peewee', reserved_list)

    reserved_list = [
        'ACTION_SEND', 'AndroidString',
        'attachment',
        'callback', 'createChooser',
        'email',
        'macosx_api', 'MacOSXEmail',
        'platform_api', 'putExtra',
        'recipient',
        'send', 'send_email', 'subject',
        'text',
        'uri',
    ]
    add_reserveds('plyer', reserved_list)

    reserved_list = [
        'addObject_', 'addPayment_', 'addTransactionObserver_', 'alloc',
        'AppDelegate', 'arrayWithCapacity_', 'autoclass',
        'canMakePayments', 'count', 'currentDevice',
        'defaultQueue', 'delegate', 'dylib', 'dylib_manager',
        'EmailViewController', 'error',
        'filename', 'filename_alias', 'finishTransaction_',
        'identifierForVendor', 'INCLUDE', 'init', 'initWithString_',
        'initWithProductIdentifiers_', 'instance', 'invalidProductIdentifiers',
        'iOSXEmail',
        'load_framework', 'localizedDescription', 'localizedTitle',
        'mailComposeDelegate', 'mimetype',
        'objc_str', 'objectAtIndex_', 'objectForKey_', 'openURL_',
        'payment',
        'paymentQueue_restoreCompletedTransactionsFailedWithError_',
        'paymentQueueRestoreCompletedTransactionsFinished_',
        'paymentQueue_updatedTransactions_',
        'paymentWithProduct_', 'price', 'priceAsFormattedString',
        'priceAsString', 'priceLocale', 'productIdentifier', 'products',
        'productsRequest_didReceiveResponse_', 'productsRequest','protocol',
        'quantity',
        'restoreCompletedTransactions',
        'sendEmail', 'sendEmail_', 'setFormatterBehavior_', 'setNumberStyle_',
        'setObject_forKey_', 'setWithArray_',
        'setWithObject_',
        'sharedApplication',
        'standardUserDefaults', 'start', 'StoreKit', 'stringForKey_',
        'transactionState',
        'UTF8String', 'UUIDString',
    ]
    add_reserveds('pyobjus', reserved_list)

    reserved_list = pyparsing.__all__
    reserved_list.extend([
        'loc',
        'parseString',
        'setParseAction', 'strg', 'suppress',
        'toks',
    ])
    add_reserveds('pyparsing', reserved_list)

    reserved_list = keyword.kwlist
    reserved_list.extend([
        '__class__', '__file__', '__future__', '__init__', '__main__',
        '__metaclass__', '__name__', '__repr__', '__str__', '__version__',
        'abc', 'ABCMeta', 'abstractmethod', 'abstractproperty', 'add',
        'append', 'AssertionError', 'AttributeError',
        'basestring', 'basename',
        'ceil', 'chr', 'clear', 'Clock', 'clock', 'collections', 'count',
        'debug', 'defaultdict', 'difference', 'dir', 'discard', 'division',
        'divmod',
        'endswith', 'ensure_ascii', 'enumerate', 'Exception', 'extend',
        'factorial', 'False', 'fatal', 'FloatingPointError', 'floor', 'for',
        'format',
        'getattr', 'getdefault',
        'hasattr',
        'ImportError', 'index', 'IndexError', 'info', 'inspect', 'isalpha',
        'isalnum', 'isdigit', 'isfile', 'isinstance',
        'iteritems', 'itertools',
        'join',
        'KeyError', 'KeyboardInterrupt',
        'lambda', 'largs', 'len', 'list', 'lower', 'lstrip',
        'main', 'math', 'map', 'max', 'memory', 'message', 'Meta', 'min',
        'namedtuple', 'newline', 'None', 'null', 'ntpath',
        'object', 'open',
        'pop', 'popleft', 'property',
        'radians', 'range', 'read', 'remove', 'replace', 'round', 'rstrip',
        'schedule_once', 'search', 'set', 'setter', 'sort_keys',
        'splitlines', 'stack', 'startswith', 'staticmethod', 'StopIteration',
        'str', 'strip', 'sum', 'super', 'SystemExit',
        'title', 'True', 'type', 'TypeError',
        'u', 'unicode', 'union', 'update', 'upper',
        'ValueError',
        'warning', 'while',
        'xrange',
        'yield',
        'ZeroDivisionError', 'zip',
    ])
    add_reserveds('python', reserved_list)

    reserved_list.extend([
        'addfinalizer', 'assert', 'autouse',
        'conftest',
        'fixture', 'function',
        'mark',
        'raises', 'request',
        'scope', 'session',
        'teardown', 'tmpdir',
        'usefixtures',
    ])
    add_reserveds('pytest', reserved_list)

    reserved_list = [
    ]
    add_reserveds('re', reserved_list)

    reserved_list = [
        'copy',
        'ignore_errors',
    ]
    add_reserveds('shutil', reserved_list)

    reserved_list = [
        'close', 'commit',
        'execute',
    ]
    add_reserveds('sqlite', reserved_list)

    reserved_list = [
    ]
    add_reserveds('subprocess', reserved_list)

    reserved_list = [
        '_clear_type_cache', '_current_frames', '_getframe', '_mercurial',
        'api_version', 'argv',
        'builtin_module_names', 'byteorder',
        'call_tracing', 'callstats', 'copyright',
        'displayhook', 'dont_write_bytecode',
        'exc_clear', 'exc_info', 'exc_type', 'excepthook', 'exec_prefix',
        'executable', 'exit', 'exitfunc',
        'flags', 'float_info', 'float_repr_style',
        'getcheckinterval', 'getdefaultencoding', 'getdlopenflags',
        'getfilesystemencoding', 'getprofile', 'getrecursionlimit',
        'getrefcount', 'getsizeof', 'gettrace',
        'hexversion',
        'last_traceback', 'last_type', 'last_value', 'long_info',
        'maxint', 'maxsize', 'maxunicode', 'meta_path', 'modules',
        'path', 'path_hooks', 'path_importer_cache', 'platform', 'prefix',
        'py3kwarning',
        'real_prefix',
        'setcheckinterval', 'setdlopenflags', 'setprofile',
        'setrecursionlimit', 'settrace', 'stderr', 'stdin', 'stdout',
        'subversion',
        'version', 'version_info',
        'warnoptions',
    ]
    add_reserveds('sys', reserved_list)

    reserved_list = [
        'ImportError',
    ]
    add_reserveds('urllib', reserved_list)

    #####################################
    # Populate application reserved names
    #####################################
    # MyApp reserved names.
    # Add only the names that have a special reason to not obfuscate.
    # This should be a pretty short list (excepting for db field names).
    reserved_list = [
        'my_db_field', 'my_named_tuple',
        'some_var_that_should_not_be_obfuscated',
        'some_class',
    ]
    add_reserveds('MyApp', reserved_list)

    ##########
    # Finished
    ##########
    logger.info('Obfuscate.build.build_db: Finished')
