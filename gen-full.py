#!/usr/bin/env python3

import re
import os
import sys

def main(input_file, output_file, base_dir):
    # Read the content of the input file (run.js)
    with open(input_file, 'r') as file:
        input_content = file.read()

    # Regular expression to find load() calls
    load_pattern = re.compile(r"load\((base_dir \+ '([^']+)')\);")

    # Function to read the content of a file
    def read_file_content(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    # Replace each load() call with the content of the corresponding file
    def replace_load_calls(content):
        matches = load_pattern.findall(content)
        for match in matches:
            file_path = os.path.join(base_dir, match[1])
            file_content = read_file_content(file_path)
            content = content.replace(f"load({match[0]});", file_content)
        return content

    # Replace load() calls in the input content
    output_content = replace_load_calls(input_content)

    # Write the full content to the output file (run-full.js)
    with open(output_file, 'w') as file:
        file.write(output_content)

    print(f"{output_file} has been created.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_run_full.py <input_file> <output_file> <base_dir>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        base_dir = sys.argv[3]
        main(input_file, output_file, base_dir)

