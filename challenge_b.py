import sys
import re

import constant
import utility



# Input file path
input_file = sys.argv[1] if len(sys.argv) > 1 else constant.DEFAULT_INPUT_FILE_PATH
# Output file path
output_file = sys.argv[2] if len(sys.argv) > 2 else constant.DEFAULT_OUTPUT_FILE_PATH


# Read input file
with open(input_file, "r") as f:
    data = f.read().strip(",")

# Split the content by comma to get individual data objects
items = data.split(",")

# Analyze each item and print its type
with open(output_file, "w") as f:
    for item in items:
        obj = item.strip()  # Remove leading/trailing whitespace
        obj_type = utility.identify_type(obj)
        output_line = f"{repr(obj)} => {obj_type}\n"
        f.write(output_line)