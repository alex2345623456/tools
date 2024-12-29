import argparse
import os
import math

def split_file(input_file, num_files):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    lines_per_file = math.ceil(total_lines / num_files)

    base_name = os.path.splitext(os.path.basename(input_file))[0]

    for i in range(num_files):
        start_index = i * lines_per_file
        end_index = min(start_index + lines_per_file, total_lines)
        
        output_file = f"{i+1}{base_name}.txt"
        with open(output_file, 'w') as out_file:
            out_file.writelines(lines[start_index:end_index])

        print(f"Created {output_file} with lines {start_index + 1}-{end_index}")

def main():
    parser = argparse.ArgumentParser(description="Split a text file into multiple files with equal number of lines.")
    parser.add_argument('-l', '--file', required=True, help="Path to the input text file.")
    parser.add_argument('-n', '--num', type=int, required=True, help="Number of files to split into.")

    args = parser.parse_args()

    split_file(args.file, args.num)

if __name__ == "__main__":
    main()
