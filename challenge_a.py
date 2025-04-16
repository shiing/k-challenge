import sys
import random
import string

# Constants
PER_STRING_LENGTH = 10                      # Length of generated strings
MAXIMUM_WHITE_SPACE_COUNT = 10              # Maximum number of spaces before/after alphanumeric strings
DEFAULT_FILE_SIZE = 10 * 1024 * 1024        # Default file size: 10MB
DEFAULT_FILE_OUTPUT_PATH = 'challenge_a_output.txt'  # Output file path


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
    spaces_before = ' ' * random.randint(0, MAXIMUM_WHITE_SPACE_COUNT)
    spaces_after = ' ' * random.randint(0, MAXIMUM_WHITE_SPACE_COUNT)

    return f"{spaces_before}{core}{spaces_after}"


def generate_file_with_4_types_object(fileSize, output_file_path):
    """
    Generate a text file with randomized objects of four types:
    - Alphabetical strings
    - Real numbers
    - Integers
    - Alphanumeric strings (with surrounding whitespace)

    Each item is separated by a comma, and the file continues to write
    until the target size (in bytes) is reached.
    """
    generators_func = [
        generate_random_alphabetical_string,
        generate_random_real_number,
        generate_random_integer,
        generate_random_alphanumeric_string,
    ]

    with open(output_file_path, "w") as f:
        size = 0
        while size < fileSize:
            gen_func = random.choice(generators_func)

            # String-based generators require a length argument
            if gen_func.__name__ in (
                'generate_random_alphabetical_string',
                'generate_random_alphanumeric_string'
            ):
                f.write(gen_func(PER_STRING_LENGTH) + ",")
            else:
                f.write(str(gen_func()) + ",")

            size = f.tell()  # Get current file size in bytes


# Example outputs for testing each generator
print('generate_random_alphabetical_string:', generate_random_alphabetical_string(10))
print('generate_random_real_number:', generate_random_real_number())
print('generate_random_integer:', generate_random_integer())
print('generate_random_alphanumeric_string:', generate_random_alphanumeric_string(10))

# Generate the full output file
generate_file_with_4_types_object(DEFAULT_FILE_SIZE, DEFAULT_FILE_OUTPUT_PATH)