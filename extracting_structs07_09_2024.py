import os
import re

def extract_structs_from_file(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    in_struct = False
    in_union = False
    structs = []
    current_struct = []
    current_union = []
    struct_name = ""
    union_name = ""
    declaration_line = ""
    specific_string = ['double', 'float', 'uint32_t','int32_t','uint16_t', 'int16_t', 'uint8_t', 'int8_t', 'bool']
    union_string = ['d','f','u32','i32','u16','i16','u8','i8','b']


    for line in lines:
        # print(line)
        stripped_line = line.strip()
        
        # Remove comments from the line
        stripped_line = re.sub(r'//.*', '', stripped_line)
        stripped_line = re.sub(r';', '', stripped_line)
        # Skip empty lines
        if not stripped_line:
            continue

        # Detecting the start of a union (single line)
        if stripped_line.startswith('union') and stripped_line[1] in stripped_line:
            in_union = True
            parts = stripped_line.split()
            if len(parts) > 1:
                union_name = parts[1]  # Handle "union UnionName {"
            else:
                union_name = "anonymous_union"
        # Detecting the end of a union
        elif in_union and stripped_line.endswith('}'):
            in_union = False
            union_name = ""

        # Detecting the start of a struct (single line)
        elif stripped_line.startswith('struct'):
            in_struct = True
            parts = stripped_line.split()
            if len(parts) > 1:
                struct_name = parts[1].split('{')[0].strip()  # Handle "struct StructName {"
            else:
                struct_name = "anonymous_struct"
            if in_union:
                struct_name = f"{union_name}::{struct_name}"  # Nested struct inside a union

        # Detecting the end of a struct
        elif in_struct and stripped_line.endswith('}'):
            in_struct = False
            structs.append(current_struct)
            current_struct = []

### if parts[0] is not within inside list containing exceptible sub strings
### if parts[0] 
### length of stripped line is greater than 2 [type var] 
### do not process


        
        # Handling struct members
        elif in_struct:
            parts = stripped_line.split()
            print(parts)
            if len(parts) >= 2:
                member_type = ' '.join(parts[:-1])
                member_name = parts[1]
                bVal = ""
                for s in specific_string:
                  if s in parts: 
                    index_position = specific_string.index(s)
                    unionVal = union_string[index_position]
                    stringY = "test_b[0]."
                    bVal = stringY + unionVal
                    # print(bVal)
                # print(bVal)
                totalOutput = "obj1.obj2." + parts[1] + ';'
                # print(totalOutput)
                fullAssignment = ""
                if len(bVal) > 0:
                  fullAssignment = bVal + ' = ' + totalOutput
                else:
                    fullAssignment = ""
                
                print(fullAssignment)
                current_struct.append(f"{os.path.basename(input_file_path)},{struct_name},{member_type},{member_name},{union_name},{bVal},{totalOutput},{fullAssignment}")

        # partA = stripped_line.split()
        # # print(partA)
        # specific_string = ['double', 'float', 'uint32_t','int32_t','uint16_t', 'int16_t', 'uint8_t', 'int8_t', 'bool']
        # union_string = ['d','f','u32','i32','u16','i16','u8','i8','b']
        # for s in specific_string:
        #     if s in partA:
        #         x = s
        #         # print("Heres whats found!: " + x + "\n")
        #         index_position = specific_string.index(x)
        #         # print(index_position)
        #         # print(union_string[index_position])
        #         unionVal = union_string[index_position]
        #         stringY = "test_b[0]."
        #         bVal = stringY + unionVal
        #         print(bVal)
        #         # if x in union_string:
                #     print(x)
            # else:
            #     print("not found")
            # print(s)
        # print(partA)
    return structs

def process_directory(input_dir, intermediate_file_path):
    all_structs = []

    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.h'):
                input_file_path = os.path.join(root, filename)
                structs_content = extract_structs_from_file(input_file_path)
                if structs_content:
                    all_structs.extend(structs_content)

    with open(intermediate_file_path, 'w') as intermediate_file:
        # Write the header
        intermediate_file.write("file,struct,type,member,union,buffer,totalOutput,fullAssignment\n")
        for struct in all_structs:
            for entry in struct:
                intermediate_file.write(entry + '\n')

# Example usage with raw input paths
# input_dir = r"C:\Users\Brian\Desktop\python sample script\cppStructsA"
# intermediate_file_path = r"C:\Users\Brian\Desktop\python sample script\structs.txt"
# process_directory(input_dir, intermediate_file_path)

input_dir = r"C:\Users\Brian\Desktop\python sample script"
intermediate_file_path = r"C:\Users\Brian\Desktop\python sample script\structswithDIR.txt"
process_directory(input_dir, intermediate_file_path)


