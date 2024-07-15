import os
import re

file_name = ['sampleStruct.h']
global i
i = 0
x = 0

def extract_structs_from_file(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    global clear_array 
    clear_array = False
    in_struct = False
    in_union = False
    in_namespace = False
    structs = []
    current_struct = []
    current_union = []
    member_struct_array = []
    member_name_array = []
    member_type_array = []
    midStruct = []
    midType = []
    midMember = []

    


    global current_namespace_content 
    megastruct = []
    current_namespace_content = []
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
        
                # Detecting the start of a namespace
        if stripped_line.startswith('namespace'):
            in_namespace = True
            namespace_name = stripped_line.split()[1].strip('{')
            # print(type(namespace_name))
            # print(namespace_name)
            continue

        # Detecting the end of the namespace block
        if in_namespace and stripped_line.startswith('#pragma'):
            in_namespace = False

        # If inside a namespace block, collect its content
        if in_namespace:
            listNameSpaceContent = stripped_line.split()
            listNameSpaceContentint = int(listNameSpaceContent[-1])
            # listNameSpaceContent = int(stripped_line.split()[-1])
            current_namespace_content.append(stripped_line)
            
            # print(type(stripped_line))
            # print(stripped_line)
            # current_namespace_content.append(listNameSpaceContent)
            # print(type(current_namespace_content))
            # print(current_namespace_content)
            # print(listNameSpaceContent)
            # print(listNameSpaceContentint)
            # print(type(a))
            # b = int(a[-1])
            # print(b)
            # print(type(b))






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
                # member_struct_array.append(struct_name)
            else:
                struct_name = "anonymous_struct"
                # member_struct_array.append(struct_name)
            if in_union:
                struct_name = f"{union_name}::{struct_name}"  # Nested struct inside a union
                # member_struct_array.append(struct_name)

        # Detecting the end of a struct
        elif in_struct and stripped_line.endswith('}'):
            in_struct = False
            structs.append(current_struct)
            current_struct = []


### if parts[0] is not within inside list containing exceptible sub strings
# if parts[0] 
### length of stripped line is greater than 2 [type var] 
### do not process



        # Handling struct members
        elif in_struct:
            parts = stripped_line.split()
            # print("Parts are: ")
            # print(parts)
            global x
            if x == 0:
                pass
            else:
                member_struct_array.append(struct_name)
            x+=1
            # member_struct_array.append(struct_name)
            # print(parts)
            if len(parts) >= 2:
                member_type = ' '.join(parts[:-1])
                member_name = parts[1]
                bVal = ""
                for s in specific_string:
                  if s in parts: 
                    index_position = specific_string.index(s)
                    unionVal = union_string[index_position]
                    stringY = "TM_Buffer[0]."
                    bVal = stringY + unionVal
                    # print(bVal)
                # print(bVal)
                totalOutput = "msg.payload." + parts[1] + ';'
                # print(totalOutput)
                fullAssignment = ""
                if len(bVal) > 0:
                  fullAssignment = bVal + ' = ' + totalOutput
                else:
                    fullAssignment = ""
                
                # print(fullAssignment)
                # print(input_file_path)
                # print("Here is struct")
                # member_struct_array.append(struct_name)
                # print(member_struct_array)


                file_name.append(f"{os.path.basename(input_file_path)}")
                length_file = int(len(file_name))

                current_struct.append(f"{os.path.basename(input_file_path)},{struct_name},{member_type},{member_name},{union_name},{bVal},{totalOutput},{fullAssignment},{current_namespace_content}")

                if (file_name[length_file-1] == file_name[length_file-2]):
                  # print(file_name[length_file-1])
                  # print(file_name[length_file-2])
                  # print("File has changed")
                  #  print(file_name[length_file-2])
                  #  print([length_file-2])
                  #  print(file_name[length_file-1])
                  #  print([length_file-1])
                  #  print(len(file_name))
                  #  print("\n")
                   clear_array = False
                else:
                  print("File name changed from " + file_name[length_file-2] + " to " +file_name[length_file-1])
                  print("The index of change is " + str(length_file-2) + " and " + str(length_file-1))

                  clear_array = True
                  # member_struct_array.append(struct_name)
                  # member_type_array.append(member_type)
                  # member_name_array.append(member_name)
                  print("\n")
      

                if (int(len(member_struct_array)) < 2):
                    member_struct_array.append(struct_name)
                     
                if (member_struct_array[int(len(member_struct_array))-1] == member_struct_array[int(len(member_struct_array))-2]):
                    
                    midStruct.append(struct_name)
                    midType.append(member_type)
                    # print(midType)
                    # print(len(midType))
                    midMember.append(member_name)
                    # print(midMember)
                    # print(len(midMember))
                    # member_struct_array.
                    # i+=1
                    # if (int(len(member_struct_array)) == 2):
                    #   member_struct_array.append(struct_name)
                    # else:
                    #     print("gay")
                    # print("Midstruct is")
                    # print(midStruct)
                    # print("MidType is")
                    # print(midType)
                    # print(midMember)
                    # print("Member struct is constant++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")



                    
                    



                if clear_array == False:
                  # print("Trigger")
                  member_type_array.append(member_type)
                  member_name_array.append(member_name)
                  
                  # print("Member Structs are :")
                  # print(member_struct_array)
                  # print(len(member_struct_array))
                  # # print("Member Types are :")
                  # print(member_type_array)     
                  # print(len(member_type_array)) 
                  # # print("Member Names are :")
                  # print(member_name_array)
                  # print(len(member_name_array))




                  # for i in range(1,int(len(member_struct_array))):
                  #     if member_struct_array[i] != member_struct_array[i-1]:
                  #       # myStruct.append(i)
                  #       # print(myStruct)
                  #       # print(i)
                  #       print("Struct has changed from")
                  #       print(member_struct_array[i-1])
                  #       print("to")
                  #       print(member_struct_array[i])
                  # looper = int(len(member_struct_array))
                  # for i in range(1,looper):
                  #   if member_struct_array[i] == member_struct_array[i-1]:
                  #     print("same")
                  #     myStruct.append(member_struct_array[i])
                  #     print(myStruct)
                  #     # print(myStruct)
                  #     # print(i)
                      
                    
                  #   else:
                  #     print("Struct has changed from")
                  #     print(member_struct_array[i-1])
                  #     print("to")
                  #     print(member_struct_array[i])
                    




                        
                else:
                    # print(member_type_array)
                    # print("\n")
                    # print(member_name_array)



                    member_struct_array.pop(1)





                    working_struct = member_struct_array
                    # print("working_struct")
                    # print(working_struct)
                    # if member_struct_array.length != 0:
                    
                    print("myStruct is !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    # print(myStruct)
                    print("Arrays being cleared!!!")
                    member_type_array = []
                    member_name_array = []
                    member_type_array.append(member_type)
                    member_name_array.append(member_name)
                    midStruct = []
                    midType = []
                    midMember = []
                    # print("New struct being entered +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    midStruct.append(struct_name)
                    midType.append(member_type)
                    midMember.append(member_name)

                # print(file_name[1-1])
                # print(file_name[0])
                # if (file_name[1] != file_name[0]):
                #     print("File has changed")
                # else:
                #     print(file_name[length_file])
                    
                
                # print(file_name)
                # print(len(file_name))
            # print("###################################New LINE###########################################")
    # print(file_name)
    fullStructHandler = []
    fullTypeHandler = []
    fullMemberHandler = []
    
    sameStruct = [member_struct_array[0]]
    sameType = [member_type_array[0]]
    sameMember = [member_name_array[0]]

    if (int(len(member_struct_array)) != int(len(member_type_array))):
      member_struct_array.pop(-1)
    looper = int(len(member_struct_array))
    for i in range(1,looper):
      # if (int(len(member_struct_array)) != int(len(member_type_array))):
      #     member_struct_array.pop(1)
      if member_struct_array[i] == member_struct_array[i-1]:
        # print("same")
        sameStruct.append(member_struct_array[i])
        sameType.append(member_type_array[i])
        sameMember.append(member_name_array[i])
        # print(sameStruct)
        # print(myStruct)
        # print(i)
        # print(member_struct_array[i-1])
        # print("to")
        # print(member_struct_array[i])
        
      
      else:
        fullStructHandler.append(sameStruct)
        sameStruct = [member_struct_array[i]]
        fullTypeHandler.append(sameType)
        sameType = [member_type_array[i]]
        fullMemberHandler.append(sameMember)
        sameMember = [member_name_array[i]]

        # print("Struct has changed from")

        # print(member_struct_array[i-1])
        # print("to")
        # print(member_struct_array[i])


    # if (int(len(member_struct_array)) != int(len(member_type_array))):
    #   member_struct_array.pop(1)


    
    fullStructHandler.append(sameStruct)
    fullTypeHandler.append(sameType)
    fullMemberHandler.append(sameMember)
    print("fullStructHandler is")
    print(fullStructHandler)
    print(len(fullStructHandler))
    print("fullTypeHandler is")
    print(fullTypeHandler)
    print(len(fullTypeHandler))
    print("fullMemberHandler is")
    print(fullMemberHandler)
    print(len(fullMemberHandler))
    # print(member_struct_array)
    # print(len(member_struct_array))
    # print(member_type_array)
    # print(len(member_type_array))
    # print(member_name_array)
    # print(len(member_name_array))
    # return structs, current_namespace_content
    print("###################################New LINE###########################################")


    



    return structs

def process_directory(input_dir, intermediate_file_path):
    all_structs = []

    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith('.h'):

                input_file_path = os.path.join(root, filename)
                # global x
                # x = 0
                structs_content = extract_structs_from_file(input_file_path)
                if structs_content:
                    all_structs.extend(structs_content)

    with open(intermediate_file_path, 'w') as intermediate_file:
        # Write the header
        intermediate_file.write("file,struct,type,member,union,buffer,totalOutput,fullAssignment\n")
        for struct in all_structs:
            for entry in struct:
                # print(type(entry))
                # print(entry)

                intermediate_file.write(entry + '\n')

input_dir = r"C:\Users\Brian\Desktop\python sample script"
intermediate_file_path = r"C:\Users\Brian\Desktop\python sample script\structswithDIR07102024.txt"
process_directory(input_dir, intermediate_file_path)


