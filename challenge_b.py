import re


DEFAULT_INPUT_FILE_PATH = "output_data.txt"
INTEGER_REGEX_PATTERN = r'-?\d+'
REAL_NUMBER_REGEX_PATTERN = r"""
    ^[-+]?(?:
        (?:\d+\.\d*) | (?:\.\d+)        # decimals like 123.456 or .456
        | \d+                           # or plain integers like 123
    )
    (?:[eE][-+]?\d+)?                   # optional scientific notation
    $                                   # end of string
"""
ALPHANUMERIC_REGEX_PATTERN = r'[A-Za-z0-9]+'


integer_regex = re.compile(INTEGER_REGEX_PATTERN, re.VERBOSE)
real_number_regex = re.compile(REAL_NUMBER_REGEX_PATTERN, re.VERBOSE)
alphanumeric_regex = re.compile(ALPHANUMERIC_REGEX_PATTERN, re.VERBOSE)


def identify_type(obj):
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


input_file = DEFAULT_INPUT_FILE_PATH

with open(input_file, "r") as f:
    data = f.read().strip(",")

items = data.split(",")

for item in items:
    obj = item.strip()
    obj_type = identify_type(obj)

    print(f"{repr(obj)} => {obj_type}\n")
