import random


#################
# Base conversion
#################
# ALPHABET is printable characters to use for encoding; excludes l and I
# ALPHABET = 'abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
# RANDOM_SEED is used mostly for testing
RANDOM_SEED = None


def set_random_seed(random_seed):
    global RANDOM_SEED
    # Force seed if one is given (used for tests)
    RANDOM_SEED = random_seed


def base_random_number(num_len, alphabet=ALPHABET):
    global RANDOM_SEED
    if RANDOM_SEED:
        random.seed(RANDOM_SEED)
    RANDOM_SEED = None
    return random.randint(0, len(alphabet)**num_len - 1)


def base_alphabet_encode(num, min_num_pos=None, alphabet=ALPHABET):
    """Encode a number in Base X

    Field notes:
        num: The number to encode
        min_num_pos: Minimum number of generated positions (zero-fill missing)
        alphabet: The alphabet to use for encoding
    """
    if num == 0:
        if min_num_pos:
            return alphabet[0] * min_num_pos
        else:
            return alphabet[0]
    if num < 0:
        num *= -1
        arr = ['-']
    else:
        arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num //= base
        arr.append(alphabet[rem])
    arr.reverse()
    base_num = ''.join(arr)
    if min_num_pos and len(base_num) < min_num_pos:
        return ''.join([alphabet[0] * (min_num_pos - len(base_num)), base_num])
    else:
        return base_num


def base_alphabet_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    is_pos = True
    if string[-1] == '-':
        is_pos = False
        string = string[0:-1]
    str_len = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (str_len - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num if is_pos else -num
