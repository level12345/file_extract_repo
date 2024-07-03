# extract_structs.py
import os

def extract_structs_from_file(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    in_struct = False
    structs = []
    current_struct = []
    struct_name = ""

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('struct'):
            in_struct = True
            struct_name = stripped_line.split()[1]  # Assuming format "struct StructName {"
        elif in_struct:
            if stripped_line.endswith('};'):
                in_struct = False
                structs.append(current_struct)
                current_struct = []
            else:
                parts = stripped_line.split()
                if len(parts) >= 2:
                    member_type = ' '.join(parts[:-1])
                    member_name = parts[-1].rstrip(';')
                    current_struct.append(f"{os.path.basename(input_file_path)},{struct_name},{member_type},{member_name}")

    return structs

def process_directory(input_dir, intermediate_file_path):
    all_structs = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.cpp'):
            input_file_path = os.path.join(input_dir, filename)
            structs_content = extract_structs_from_file(input_file_path)
            if structs_content:
                all_structs.extend(structs_content)

    with open(intermediate_file_path, 'w') as intermediate_file:
        # Write the header
        intermediate_file.write("file,struct,type,member\n")
        for struct in all_structs:
            for entry in struct:
                intermediate_file.write(entry + '\n')

# Example usage with raw input paths



# Example usage with raw input paths
input_dir = r"C:\Users\Brian\Desktop\python sample script\cppStructsA"
intermediate_file_path = r"C:\Users\Brian\Desktop\python sample script\structs.txt"
process_directory(input_dir, intermediate_file_path)
