import os
import io
import pytest
from os.path import join
from logic.utilities import file_gen, obfuscate_path, split_path
from logic.reserved import get_reserved, save_reserved, get_reserved_by_name
from logic.identifier import get_identifier_by_name


@pytest.mark.usefixtures('session')
def test_get_dir(tmpdir):
    # Setup reserved folder
    reserved_row = get_reserved(None)
    assert 2 == save_reserved(
        reserved_row,
        name=u'/rsv_dir',
        primary_package='rsv_pkg')

    reserved_row = get_reserved(None)
    assert 3 == save_reserved(
        reserved_row,
        name=u'~rsv_file.py',
        primary_package='rsv_file_pkg')

    reserved_row = get_reserved(None)
    assert 4 == save_reserved(
        reserved_row,
        name=u'#no_obf',
        primary_package='no_obf_pkg')

    reserved_row = get_reserved(None)
    assert 5 == save_reserved(
        reserved_row,
        name=u'=no_obf_file.py')

    # Setup folders and files
    f = io.open(join(str(tmpdir), 'test.py'), 'w')
    f.close()

    f = io.open(join(str(tmpdir), 'rsv_file.py'), 'w')
    f.close()

    included_dir = join(str(tmpdir), 'not_rsv0')
    os.mkdir(included_dir)
    f = io.open(join(included_dir, 'not_rsv0a.py'), 'w')
    f.close()
    f = io.open(join(included_dir, 'not_rsv0b.py'), 'w')
    f.close()
    included_dir = join(str(tmpdir), 'not_rsv0', 'not_rsv0.1')
    os.mkdir(included_dir)
    f = io.open(join(included_dir, 'not_rsv0.1.py'), 'w')
    f.close()

    excluded_dir = join(str(tmpdir), 'rsv_dir')
    os.mkdir(excluded_dir)
    excluded_dir = join(str(tmpdir), 'rsv_dir', 'rsv_dir_subdir')
    os.mkdir(excluded_dir)
    f = io.open(join(excluded_dir, 'rsv_subdir_file.py'), 'w')
    f.close()

    included_dir = join(str(tmpdir), 'not_rsv_file')
    os.mkdir(included_dir)
    f = io.open(join(included_dir, 'not_rsv_file.py'), 'w')
    f.close()

    included_dir = join(str(tmpdir), 'not_rsv0', 'no_obf')
    os.mkdir(included_dir)
    included_dir = join(str(tmpdir), 'not_rsv0', 'no_obf', 'no_obf_1')
    os.mkdir(included_dir)
    f = io.open(join(included_dir, 'no_obf_1.py'), 'w')
    f.close()

    f = io.open(join(str(tmpdir), 'no_obf_file.py'), 'w')
    f.close()

    # Test reading directory structure
    get_files_gen = file_gen(str(tmpdir))
    num_lines = 0
    for file_name, dir_name, is_reserved_dir, is_reserved_file, \
            do_obfuscate in get_files_gen:
        if file_name == 'test.py':
            assert dir_name == str(tmpdir)
            assert not is_reserved_dir
            assert not is_reserved_file
            assert do_obfuscate
        if file_name == 'not_rsv0a.py':
            assert dir_name == join(str(tmpdir), 'not_rsv0')
            assert not is_reserved_dir
            assert not is_reserved_file
            assert do_obfuscate
        if file_name == 'not_rsv0b.py':
            assert dir_name == join(str(tmpdir), 'not_rsv0')
            assert not is_reserved_dir
            assert not is_reserved_file
            assert do_obfuscate
        if file_name == 'not_rsv0.1.py':
            assert dir_name == join(str(tmpdir), 'not_rsv0', 'not_rsv0.1')
            assert not is_reserved_dir
            assert not is_reserved_file
            assert do_obfuscate
        if file_name == 'not_rsv_file.py':
            assert dir_name == join(str(tmpdir), 'not_rsv_file')
            assert not is_reserved_dir
            assert not is_reserved_file
            assert do_obfuscate
        if file_name == 'rsv_subdir_file.py':
            assert dir_name == join(str(tmpdir), 'rsv_dir', 'rsv_dir_subdir')
            assert is_reserved_dir
            assert is_reserved_file
            assert not do_obfuscate
            assert get_reserved_by_name(
                ''.join(['/', 'rsv_dir_subdir'])).primary_package == 'rsv_pkg'
        if file_name == 'rsv_file.py':
            assert dir_name == str(tmpdir)
            assert not is_reserved_dir
            assert is_reserved_file
            assert not do_obfuscate
        if file_name == 'no_obf_1.py':
            assert dir_name == join(str(tmpdir), 'not_rsv0', 'no_obf', 
                                    'no_obf_1')
            assert not is_reserved_dir
            assert not is_reserved_file
            assert not do_obfuscate
            assert get_reserved_by_name(
                ''.join(['#', 'no_obf_1'])).primary_package == 'no_obf'
        if file_name == 'no_obf_file.py':
            assert dir_name == str(tmpdir)
            assert not is_reserved_dir
            assert not is_reserved_file
            assert not do_obfuscate
        num_lines += 1
    assert num_lines == 9
    assert get_reserved_by_name('~rsv_subdir_file.py').primary_package == \
        'rsv_dir_subdir'
    assert get_identifier_by_name('no_obf_1').name == 'no_obf_1'


def test_split_path():
    assert split_path('dir1/dir2/dir3/file.py') == ['dir1', 'dir2', 'dir3',
                                                    'file.py']
    assert split_path('file.py') == ['file.py']


@pytest.mark.usefixtures('session')
def test_obfuscate_path():
    # Test with no obfuscated identifiers
    assert obfuscate_path('file.py') == 'file.py'
    assert obfuscate_path('dir1/dir2/dir3/file.py') == \
        'dir1/dir2/dir3/file.py'

    # Test with obfuscated identifiers
    assert obfuscate_path('identifier_one.py') == 'aaa.py'
    assert obfuscate_path('dir1/identifier_one/dir3/identifier_one.py') == \
        'dir1/aaa/dir3/aaa.py'
