import random
import string

import constant
import utility



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
        utility.generate_random_alphabetical_string,
        utility.generate_random_real_number,
        utility.generate_random_integer,
        utility.generate_random_alphanumeric_string,
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
                f.write(gen_func(constant.PER_STRING_LENGTH) + ",")
            else:
                f.write(str(gen_func()) + ",")

            size = f.tell()  # Get current file size in bytes


# Example outputs for testing each generator
print('generate_random_alphabetical_string:', utility.generate_random_alphabetical_string(10))
print('generate_random_real_number:', utility.generate_random_real_number())
print('generate_random_integer:', utility.generate_random_integer())
print('generate_random_alphanumeric_string:', utility.generate_random_alphanumeric_string(10))

# Generate the full output file
generate_file_with_4_types_object(constant.DEFAULT_FILE_SIZE, constant.DEFAULT_FILE_OUTPUT_PATH)