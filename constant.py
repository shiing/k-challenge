import os

# Constants for challenge a
PER_STRING_LENGTH = 10                      # Length of generated strings
MAXIMUM_WHITE_SPACE_COUNT = 10              # Maximum number of spaces before/after alphanumeric strings
DEFAULT_FILE_SIZE = 10 * 1024 * 1024        # Default file size: 10MB
DEFAULT_FILE_OUTPUT_PATH = 'challenge_a_output.txt'  # Output file path


# Constants for challenge b
DEFAULT_INPUT_FILE_PATH = "challenge_a_output.txt"
DEFAULT_OUTPUT_FILE_PATH = "challenge_b_output.txt"
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


DB_PATH = "kasagi.db"
HOST = os.getenv("KASAGI_HOST")
PORT = os.getenv("KASAGI_PORT")
JWT_TOKEN = os.getenv("KASAGI_JWT_TOKEN")
BINARY_FILE_PATH = "file"