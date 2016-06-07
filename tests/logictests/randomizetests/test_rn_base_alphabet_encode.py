from logic.randomize import base_alphabet_encode, base_random_number, ALPHABET


def test_base_random_number():
    for i in range(0, 100):
        assert 0 <= base_random_number(1) <= len(ALPHABET) - 1
    for i in range(0, 100):
        assert 0 <= base_random_number(2) <= len(ALPHABET)**2 - 1
    for i in range(0, 100):
        assert 0 <= base_random_number(3) <= len(ALPHABET)**3 - 1

    for i in range(0, 5):
        assert 0 <= base_random_number(1, alphabet='ab') <= 1


def test_base_alphabet_encode():
    assert base_alphabet_encode(0) == 'a'
    assert base_alphabet_encode(0, 3) == 'aaa'
    assert base_alphabet_encode(len(ALPHABET)-1) == 'z'
    assert base_alphabet_encode(len(ALPHABET)-1, 3) == 'aaz'
    assert base_alphabet_encode(len(ALPHABET), 3) == 'aba'
    assert base_alphabet_encode(len(ALPHABET)**2 - 1, 3) == 'azz'
    assert base_alphabet_encode(len(ALPHABET)**3 - 1, 3) == 'zzz'

    assert base_alphabet_encode(0, 3, alphabet='ab') == 'aaa'
    assert base_alphabet_encode(1, 3, alphabet='ab') == 'aab'
    assert base_alphabet_encode(2, 3, alphabet='ab') == 'aba'
    assert base_alphabet_encode(3, 3, alphabet='ab') == 'abb'
    assert base_alphabet_encode(4, 3, alphabet='ab') == 'baa'
    assert base_alphabet_encode(5, 3, alphabet='ab') == 'bab'
    assert base_alphabet_encode(6, 3, alphabet='ab') == 'bba'
    assert base_alphabet_encode(7, 3, alphabet='ab') == 'bbb'
    assert base_alphabet_encode(8, 3, alphabet='ab') == 'baaa'
