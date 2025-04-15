import re

# Constants
DEFAULT_INPUT_FILE_PATH = "output_data.txt"
INTEGER_REGEX_PATTERN = r'-?\d+'        # Regex pattern to match integers
# Regex pattern to match real numbers, including decimals and scientific notation
REAL_NUMBER_REGEX_PATTERN = r"""
    ^[-+]?                              # optional leading sign
    (?:
        (?:\d+\.\d*) | (?:\.\d+)        # match decimal numbers like 12.34 or .56
        | \d+                           # or plain integers like 123
    )
    (?:[eE][-+]?\d+)?                   # optional scientific notation (e.g., e+10, E-3)
    $                                   # end of string anchor
"""

# Regex pattern to match alphanumeric strings (letters and digits only)
ALPHANUMERIC_REGEX_PATTERN = r'[A-Za-z0-9]+'

# Compile regex patterns for reuse
integer_regex = re.compile(INTEGER_REGEX_PATTERN, re.VERBOSE)
real_number_regex = re.compile(REAL_NUMBER_REGEX_PATTERN, re.VERBOSE)
alphanumeric_regex = re.compile(ALPHANUMERIC_REGEX_PATTERN, re.VERBOSE)


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


# Read the input file
input_file = DEFAULT_INPUT_FILE_PATH

with open(input_file, "r") as f:
    data = f.read().strip(",")

# Split the content by comma to get individual data objects
items = data.split(",")

# Analyze each item and print its type
for item in items:
    obj = item.strip()  # Remove leading/trailing whitespace
    obj_type = identify_type(obj)
    print(f"{repr(obj)} => {obj_type}\n")