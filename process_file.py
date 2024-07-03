# process_file.py
import csv

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile:
        lines = infile.readlines()

    with open(output_file_path, 'w', newline='') as csvfile:
        fieldnames = ['file', 'struct', 'type', 'member']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for line in lines[1:]:  # Skip the header line in the input file
            parts = line.strip().split(',')
            if len(parts) == 4:
                file, struct, type_, member = parts
                writer.writerow({'file': file, 'struct': struct, 'type': type_, 'member': member})
            else:
                print(f"Skipping malformed line: {line.strip()} with parts: {parts}")




# Example usage with raw input paths


# Example usage with raw input paths
input_file_path = r"C:\Users\Brian\Desktop\python sample script\structs.txt"
output_file_path = r"C:\Users\Brian\Desktop\python sample script\structs.csv"
process_file(input_file_path, output_file_path)
