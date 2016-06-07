from os.path import join
import io
from logic.obfuscate import source_line_gen


def test_read(tmpdir):
    dir_name = str(tmpdir.mkdir('source'))
    source_file = 'app.py'
    with io.open(join(dir_name, source_file), 'w') as source:
        source.write(u'line 1\n')
        source.write(u'line 2\n')
        source.write(u'line 3\n')

    read_source_gen = source_line_gen(source_file, dir_name)
    num_lines = 0
    for num, line in enumerate(read_source_gen):
        if num == 0:
            assert line == u'line 1'
        if num == 1:
            assert line == u'line 2'
        if num == 2:
            assert line == u'line 3'
        num_lines += 1
    assert num_lines == 3
