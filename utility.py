import sys
import random
import re
import string

import constant


# Compile regex patterns for reuse
integer_regex = re.compile(constant.INTEGER_REGEX_PATTERN, re.VERBOSE)
real_number_regex = re.compile(constant.REAL_NUMBER_REGEX_PATTERN, re.VERBOSE)
alphanumeric_regex = re.compile(constant.ALPHANUMERIC_REGEX_PATTERN, re.VERBOSE)


def generate_random_alphabetical_string(str_length=1):
    """
    Generate a random alphabetical string of given length.
    Characters include both lowercase and uppercase letters.

    Ex, "ADiNbTjknM"
    """
    return ''.join(random.choices(string.ascii_letters, k=str_length))


def generate_random_real_number():
    """
    Generate a random real number (float) in the range of -sys.maxsize to sys.maxsize.

    Ex, 5.361683868024361e+17
    """
    return random.uniform(-sys.maxsize, sys.maxsize)


def generate_random_integer():
    """
    Generate a random integer between 0 and sys.maxsize.

    Ex, 4474644657006917053
    """
    return random.randint(0, sys.maxsize)


def generate_random_alphanumeric_string(str_length=1):
    """
    Generate an alphanumeric string of given length,
    padded with random leading and trailing whitespace (up to MAXIMUM_WHITE_SPACE_COUNT).

    Ex, "     7GicUmvY5H      "
    """
    core = ''.join(random.choices(string.ascii_letters + string.digits, k=str_length))
    spaces_before = ' ' * random.randint(0, constant.MAXIMUM_WHITE_SPACE_COUNT)
    spaces_after = ' ' * random.randint(0, constant.MAXIMUM_WHITE_SPACE_COUNT)

    return f"{spaces_before}{core}{spaces_after}"


def identify_type(obj):
    """
    Identify the type of the input string `obj` based on regex matching and string methods.

    Returns:
        str: One of the following types:
             - "alphabetical"
             - "integer"
             - "real number"
             - "alphanumeric"
             - "unknown"
    """
    obj = obj.strip()

    if obj.isalpha():
        return "alphabetical"
    elif re.fullmatch(integer_regex, obj):
        return "integer"
    elif re.fullmatch(real_number_regex, obj):
        return "real number"
    elif re.fullmatch(alphanumeric_regex, obj):
        return "alphanumeric"
    return "unknown"