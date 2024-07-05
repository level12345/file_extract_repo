import os
import re

def extract_structs_from_file(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    in_struct = False
    in_union = False
    structs = []
    current_struct = []
    struct_name = ""
    union_name = ""

    for line in lines:
        stripped_line = line.strip()
        
        # Remove comments from the line
        stripped_line = re.sub(r'//.*', '', stripped_line)

        # Skip empty lines
        if not stripped_line:
            continue

        # Detecting the start of a union
        if stripped_line.startswith('union') and '{' in stripped_line:
            in_union = True
            parts = stripped_line.split()
            if len(parts) > 1:
                union_name = parts[1].split('{')[0].strip()  # Handle "union UnionName {"
            else:
                union_name = "anonymous_union"

        # Detecting the end of a union
        elif in_union and stripped_line.endswith('};'):
            in_union = False

        # Detecting the start of a struct
        elif stripped_line.startswith('struct') and '{' in stripped_line:
            in_struct = True
            parts = stripped_line.split()
            if len(parts) > 1:
                struct_name = parts[1].split('{')[0].strip()  # Handle "struct StructName {"
                print(struct_name)
            else:
                struct_name = "anonymous_struct"
            if in_union:
                struct_name = f"{union_name}::{struct_name}"  # Nested struct inside a union

        # Detecting the end of a struct
        elif in_struct and stripped_line.endswith('};'):
            in_struct = False
            structs.append(current_struct)
            current_struct = []

        # Handling struct members
        elif in_struct:
            parts = stripped_line.split()
            if len(parts) >= 2:
                member_type = ' '.join(parts[:-1])
                member_name = parts[-1].rstrip(';')
                current_struct.append(f"{os.path.basename(input_file_path)},{struct_name},{member_type},{member_name}")

    return structs

def process_directory(input_dir, intermediate_file_path):
    all_structs = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.h'):
            input_file_path = os.path.join(input_dir, filename)
            print(input_file_path)
            structs_content = extract_structs_from_file(input_file_path)
            # print(structs_content)
            if structs_content:
                all_structs.extend(structs_content)

    with open(intermediate_file_path, 'w') as intermediate_file:
        # Write the header
        intermediate_file.write("file,struct,type,member\n")
        for struct in all_structs:
            for entry in struct:
                intermediate_file.write(entry + '\n')

# Example usage with raw input paths
input_dir = r"C:\Users\Brian\Desktop\python sample script\cppStructsA"
intermediate_file_path = r"C:\Users\Brian\Desktop\python sample script\structs.txt"
process_directory(input_dir, intermediate_file_path)
