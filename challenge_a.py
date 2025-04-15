import sys
import random
import string


PER_STRING_LENGTH = 10
MAXIMUM_WHITE_SPACE_COUNT = 10
DEFAULT_FILE_SIZE = 10 * 1024 * 1024
DEFAULT_FILE_OUTPUT_PATH = 'output_data.txt'

def generate_random_alphabetical_string(str_length=1):
    return ''.join(random.choices(string.ascii_letters, k=str_length))

def generate_random_real_number():
    return random.uniform(-sys.maxsize, sys.maxsize)

def generate_random_integer():
    return random.randint(0, sys.maxsize)

def generate_random_alphanumeric_string(str_length=1):
    core = ''.join(random.choices(string.ascii_letters + string.digits, k=str_length))
    spaces_before = ' ' * random.randint(0, MAXIMUM_WHITE_SPACE_COUNT)
    spaces_after = ' ' * random.randint(0, MAXIMUM_WHITE_SPACE_COUNT)

    return f"{spaces_before}{core}{spaces_after}"

def generate_file_with_4_types_object(fileSize=DEFAULT_FILE_SIZE, output_file_path=DEFAULT_FILE_OUTPUT_PATH):
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
            
            if gen_func.__name__ == 'generate_random_alphabetical_string' or gen_func.__name__ == 'generate_random_alphanumeric_string':
                f.write(gen_func(PER_STRING_LENGTH) + ",")
            else:
                f.write(str(gen_func()) + ",")

            size = f.tell()


print('generate_random_alphabetical_string', generate_random_alphabetical_string(10))
print('generate_random_real_number', generate_random_real_number())
print('generate_random_integer', generate_random_integer())
print('generate_random_alphanumeric_string', generate_random_alphanumeric_string(10))


generate_file_with_4_types_object()
