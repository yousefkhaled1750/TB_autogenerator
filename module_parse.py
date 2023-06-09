import re
import random

fname = input("Enter the name of the file: ")

parameters    = []
input_ports   = []
output_ports  = []
def get_module_name(fname):
    file_code = open(fname, 'rt')
    for line in file_code:
        if re.search(r'^module\s|\s+module\s',line):
            s = re.split(r'\s',line)
            module_name = str(re.findall(r'\s*\w+\s*',s[-3]))[2:][:-2]        
    return module_name

def get_module_paramters(fname):
    file_code = open(fname, 'rt')
    for line in file_code:
        if re.search(r'^parameter\s|\s+parameter\s',line):
            s = re.split(r'\s',line)
            name_param = str(re.findall(r'\s*\w+\s*',s[-4]))[2:][:-2]   
            print(name_param)
            parameters.append(name_param)
    return parameters

def get_module_ports(fname):
    file_code = open(fname, 'rt')
    for line in file_code:
        signal = {}
        if re.search(r'^input\s|\s+input\s',line):
            if re.search(r'\s+wire\s',line):
                if re.search(r'\[',line):
                    s = re.split(r'\[|\]',line)
                    name = str(re.findall(r'\w+',s[2]))[2:][:-2]
                    if re.search(r'^[A-Za-z]\w*-',s[1]):
                        size = str(re.findall((r'(.*)-'),s[1]))[2:][:-2]
                    else:
                        size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                    signal["name"] = name
                    signal["type"] = 'wire'
                    signal["size"] = size         
                    input_ports.append(signal)
                else:
                    s = re.split(r'\s+wire\s',line)
                    name = str(re.findall(r'\w+',s[1]))[2:][:-2]
                    signal["name"] = name
                    signal["type"] = 'wire'
                    signal["size"] = int(1)
                    input_ports.append(signal)
            elif re.search(r'\s+reg\s',line):
                if re.search(r'\[',line):
                    s = re.split(r'\[|\]',line)
                    name = str(re.findall(r'\w+',s[2]))[2:][:-2]
                    if re.search(r'^[A-Za-z]\w*-',s[1]):
                        size=str(re.findall((r'(.*)-'),s[1]))[2:][:-2]
                    else:
                        size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                    signal["name"] = name
                    signal["type"] = 'reg'
                    signal["size"] = size         
                    input_ports.append(signal)
                else:
                    #s = re.split(r'\s+',line)
                    #name = s[s.index('reg')+1]
                    s = re.split(r'\s+reg\s',line)
                    name = str(re.findall(r'\w+',s[1]))[2:][:-2]
                    signal["name"] = name
                    signal["type"] = 'reg'
                    signal["size"] = int(1)
                    input_ports.append(signal)   
            else:
                if re.search(r'\[',line):
                    s = re.split(r'\[|\]',line)
                    #name = str(re.findall((r'\w+,|\w+\)'),s[2]))[2:][:-3]
                    name = str(re.findall(r'\w+',s[2]))[2:][:-2]
                    if re.search(r'^[A-Za-z]\w*-',s[1]):
                        size=str(re.findall((r'(.*)-'),s[1]))[2:][:-2]
                    else:
                        size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                else:
                    s = re.split(r'\s+input\s',line)
                    name = str(re.findall(r'\w+',s[1]))[2:][:-2]
                    size = int(1)

                signal["name"] = name
                signal["type"] = 'wire'
                signal["size"] = size
                input_ports.append(signal)
        elif re.search(r'^output\s|\s+output\s',line):
            if re.search(r'\s+wire\s',line):
                if re.search(r'\[',line):
                    s = re.split(r'\[|\]',line)
                    #name = str(re.findall((r'\w+,|\w+\)'),s[2]))[2:][:-3]
                    name = str(re.findall(r'\w+',s[2]))[2:][:-2]
                    if re.search(r'^[A-Za-z]\w*-',s[1]):
                        size=str(re.findall((r'(.*)-'),s[1]))[2:][:-2]
                    else:
                        size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                    signal["name"] = name
                    signal["type"] = 'wire'
                    signal["size"] = size         
                    output_ports.append(signal)
                else:
                    #s = re.split(r'\s+',line)
                    #name = s[s.index('wire')+1]
                    s = re.split(r'\s+wire\s',line)
                    name = str(re.findall(r'\w+',s[1]))[2:][:-2]
                    signal["name"] = name
                    signal["type"] = 'wire'
                    signal["size"] = int(1)
                    output_ports.append(signal)
            elif re.search(r'\s+reg\s',line):
                if re.search(r'\[',line):
                    s = re.split(r'\[|\]',line)
                    #name = str(re.findall((r'\w+,|\w+\)'),s[2]))[2:][:-3]
                    name = str(re.findall(r'\w+',s[2]))[2:][:-2]
                    if re.search(r'^[A-Za-z]\w*-',s[1]):
                        size=str(re.findall((r'(.*)-'),s[1]))[2:][:-2]
                    else:
                        size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                    signal["name"] = name
                    signal["type"] = 'reg'
                    signal["size"] = size         
                    output_ports.append(signal)
                else:
                    #s = re.split(r'\s+',line)
                    #name = s[s.index('reg')+1]
                    s = re.split(r'\s+reg\s',line)
                    name = str(re.findall(r'\w+',s[1]))[2:][:-2]
                    signal["name"] = name
                    signal["type"] = 'reg'
                    signal["size"] = int(1)
                    output_ports.append(signal)
            else:
                if re.search(r'\[',line):
                    s = re.split(r'\[|\]',line)
                    #name = str(re.findall((r'\w+,|\w+\)'),s[2]))[2:][:-3]
                    name = str(re.findall(r'\w+',s[2]))[2:][:-2]
                    if re.search(r'^[A-Za-z]\w*-',s[1]):
                        size=str(re.findall((r'(.*)-'),s[1]))[2:][:-2]
                    else:
                        size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                else:
                    s = re.split(r'\s+output\s',line)
                    name = str(re.findall(r'\w+',s[1]))[2:][:-2]
                    size = int(1)

                signal["name"] = name
                signal["type"] = 'wire'
                signal["size"] = size
                output_ports.append(signal)

    module_ports = {}
    for p in input_ports:
        #print(p)
        module_ports[p['name']] = {"dir": 'input'}
        module_ports[p['name']]["type"] = p['type']
        module_ports[p['name']]["size"] = p['size']
        print(p['size'])
    for p in output_ports:
        #print(p)
        module_ports[p['name']] = {"dir": 'output'}
        module_ports[p['name']]["type"] = p['type']
        module_ports[p['name']]["size"] = p['size']
        print(p['size'])
    return module_ports

module_ports = get_module_ports(fname)
print(module_ports)
module_name = get_module_name(fname)
module_params = get_module_paramters(fname)


# getting the internal wires and register   //name, type, size
internal_signal = []
file_code = open(fname, 'rt')
for line in file_code:
    signal = {}
    if re.search(r'^\s*wire',line):
        if re.search(r'\[',line):
            s = re.split(r'\[|\]',line)
            name = str(re.findall(r'\s*(.*)\s*;',s[2]))[2:][:-2]
            #print(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2])
            #print(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1])))
            size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
            signal["name"] = name
            signal["type"] = 'wire'
            signal["size"] = size         
            internal_signal.append(signal)
        else:
            s = re.split(r'\s+',line)
            name = str(re.findall(r'\s*(.*);',s[1]))[2:][:-2]
            signal["name"] = name
            signal["type"] = 'wire'
            signal["size"] = 1
            internal_signal.append(signal)
    elif re.search(r'^reg',line):
        if re.search(r'\[',line):
            s = re.split(r'\[|\]',line)
            name = str(re.findall(r'\s*(.*)\s*;',s[2]))[2:][:-2]
            #print(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2])
            #print(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1])))
            size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
            signal["name"] = name
            signal["type"] = 'reg'
            signal["size"] = size         
            internal_signal.append(signal)
        else:
            s = re.split(r'\s+',line)
            name = str(re.findall(r'\s*(.*);',s[1]))[2:][:-2]
            signal["name"] = name
            signal["type"] = 'reg'
            signal["size"] = 1
            internal_signal.append(signal)
print('\n\n')
print("****************************************************************The internal signals****************************************************************")
print(internal_signal)
print('\n\n')


# getting the continuous assignment
# 1. search for assign at the beginning of the line
# 2. get the output 
# 3. check if it's conditional assignment
# 4. get the inputs 
continuous_parameters = []
file_code = open(fname, 'rt')
i = 0
for line in file_code:                  #assign data_out = op1 [+\-\*/%&|^]  op2;
    if re.search(r'assign', line):
        cont = {}
        i = i + 1
        s =re.split(r'\s+',line)
        print(s)
        if not re.search(r':',line) :       #assign out = (expr)
            if len(s) == 7:                 # 2 operands operation
                cont['type'] = 'double'
                cont['output'] = s[1] 
                cont['op1'] = s[3]
                cont['op2'] = s[5][:-1]
                cont['operation'] = s[4]
            if len(s) == 5:                     # 1 operand operation (! ~ & | ^ ~& ~| ~^)
                cont['type'] = 'single'
                if re.search('~[&|^]',s[3]):    # if it contains negating operator
                    cont['output'] = s[1] 
                    cont['op1'] = s[3][2:][:-1]
                    cont['operation'] = s[3][:2]
                else:
                    cont['output'] = s[1] 
                    cont['op1'] = s[3][1:][:-1]
                    cont['operation'] = s[3][0]
        else:                   #assign out = cond ? a : b;
            cont['type'] = 'double conditional'
            cont['output'] = s[1]
            cont['condition'] = s[3]
            cont['op1'] = s[5]
            cont['op2'] = s[7][:-1]
            cont['operation'] = 'conditional'
        continuous_parameters.append(cont)
print("****************************************************************The continuous assignments****************************************************************")
print(continuous_parameters)
print('\n\n')

# getting the always statement
# 1. get the type and excitation signals of the always block
# 2. find a way to get the output signals associated to this always block
always_parameters = []
file_code = open(fname, 'rt')
i = 0
count = 0
for line in file_code:
    if re.search(r'always',line):
        always = {}
        i = i + 1
        always['always_no'] = i
        #print(re.split(r'always\s*@\s*\(',line))
        s = re.split(r'always\s*@\s*\(',line)[1]
        s = re.split(r'\s*\)',s)[0]
        _str = ''.join(re.split(r',',s))
        if(re.search("posedge|negedge",_str)):
           always["type"] = "sequential"
           always["clk"]  = re.findall(r'posedge\s(.*)\snegedge',_str)
           #always["clk"]  = re.findall(r'posedge\s(\w+)[,\)]',_str)
           always["rst"]  = re.findall(r'negedge\s*(.*)',_str)
           always_parameters.append(always)
        else:
            always["type"] = "combinational"
            if(re.search(r'\*',_str)):
                always["signals"] = "*"
            else:
                s = re.split(r',\s',s)
                always["signals"] = s
            always_parameters.append(always)
print("****************************************************************always parameters****************************************************************")
print(always_parameters)

print('\n\n')

always_locations = []
always_locations_dict = {}
always_operations_list = []
single_always_operations_list = []
always_operation_dict = {}
always_no = 0
in_always = False
line_no = 0
file_code = open(fname, 'rt')
for line in file_code:
    line_no = line_no + 1
    if re.search(r'if',line) or re.search(r'if',line):
        continue
    if re.search(r'always',line):
        in_always = True
        always_no = always_no + 1
        always_locations_dict = {}
        always_locations_dict["always_no"] = always_no
        always_locations_dict["start_line"] = line_no
    elif re.search(r'end[\s|\n]',line):
        always_locations_dict["end_line"] = line_no
        always_locations.append(always_locations_dict)
        in_always = False
        always_operations_list.append(single_always_operations_list)
    else:
        if in_always == True and re.search(r'[^=]=[^=]',line) :     # contains assignment out <= x + b; 
            s =re.split(r'\s+',line)
            always_operation_dict = {}
            always_operation_dict['always_no'] = always_no
            if len(s) == 7:                 # 2 operands operation
                always_operation_dict['type'] = 'double'
                always_operation_dict['output'] = s[1] 
                always_operation_dict['assign'] = s[2]
                always_operation_dict['op1'] = s[3]
                always_operation_dict['op2'] = s[5][:-1]
                always_operation_dict['operation'] = s[4]
                single_always_operations_list.append(always_operation_dict)
            elif len(s) == 5:                     # 1 operand operation (! ~ & | ^ ~& ~| ~^)
                always_operation_dict['type'] = 'single'
                if re.search('~[&|^]',s[3]):    # if it contains negating operator
                    always_operation_dict['output'] = s[1] 
                    always_operation_dict['assign'] = s[2]
                    always_operation_dict['op1'] = s[3][2:][:-1]
                    always_operation_dict['operation'] = s[3][:2]
                elif re.search('~',s[3]):
                    always_operation_dict['output'] = s[1]
                    always_operation_dict['assign'] = s[2] 
                    always_operation_dict['op1'] = s[3][1:][:-1]
                    always_operation_dict['operation'] = s[3][0]
                else:
                    always_operation_dict['output'] = s[1]
                    always_operation_dict['assign'] = s[2] 
                    always_operation_dict['op1'] = s[3][:-1]
                    always_operation_dict['operation'] = 'nop'
                single_always_operations_list.append(always_operation_dict)
            
                
                
            
print("****************************************************************always operations****************************************************************")
print(always_operations_list) 
print('\n')
print("****************************************************************always locations****************************************************************")
print(always_locations)

print('\n\n')

# parsing the case statement
case_no = 0
line_no = 0
in_case = False
case_locations = []
case_locations_dict = {}
case_dict = {}
case_list = []
case_operation_dict = {}
case_operation_list = []


file_code = open(fname, 'rt')
for line in file_code:
    line_no = line_no + 1
    if re.search(r'\Wcase\s*',line):
        num_cases = 0
        case_no = case_no + 1
        case_dict = {}
        case_locations_dict = {}
        case_locations_dict['case_no'] = case_no
        case_locations_dict['start_line'] = line_no
        in_case = True
        case_dict['case_no'] = case_no
        case_dict['parameter'] = re.findall(r'case\s*\(\s*(.*)\s*\)', line)[0]
        print(case_dict['parameter'])
    elif re.search(r'endcase',line):
        in_case = False
        case_locations_dict['end_line'] = line_no
        #print(case_locations_dict)
        case_locations.append(case_locations_dict)
        case_dict['num_cases'] = num_cases
        case_dict['operations'] = case_operation_list
        #print(case_dict)
        #print('\n\n')
        case_list.append(case_dict)
    else:
        if in_case == True and re.search(r':',line):
            num_cases = num_cases + 1
            case_operation_dict = {}
            #print(line)
            s =re.split(r'\s+',line)
            #print(s)
            if len(s) == 8:                 # 2 operands operation
                case_operation_dict['case'] = s[1]
                case_operation_dict['output'] = s[2]
                case_operation_dict['assign'] = s[3]
                case_operation_dict['op1'] = s[4]
                case_operation_dict['operation'] = s[5]
                case_operation_dict['op2'] = s[6][:-1]
                #print(case_operation_dict)
                case_operation_list.append(case_operation_dict)
            if len(s) == 6:
                if re.search('~[&|^]',s[4]):    # if it contains negating operator
                    case_operation_dict['case'] = s[1]
                    case_operation_dict['output'] = s[2]
                    case_operation_dict['assign'] = s[3]
                    case_operation_dict['op1'] = s[4][2:][:-1]
                    case_operation_dict['operation'] = s[4][:2]
                elif re.search('~',s[4]):
                    case_operation_dict['case'] = s[1]
                    case_operation_dict['output'] = s[2]
                    case_operation_dict['assign'] = s[3]
                    case_operation_dict['op1'] = s[4][1:][:-1]
                    case_operation_dict['operation'] = s[4][0]
                else:
                    case_operation_dict['case'] = s[1]
                    case_operation_dict['output'] = s[2]
                    case_operation_dict['assign'] = s[3]
                    case_operation_dict['op1'] = s[4][:-1]
                    case_operation_dict['operation'] = 'nop'
                #print(case_operation_dict)
                case_operation_list.append(case_operation_dict)

print("****************************************************************case operations****************************************************************")
print(case_list)
print('\n\n')
print("****************************************************************case locations****************************************************************")
print(case_locations)
print('\n\n')

## parsing if statement
if_no = 0
line_no = 0
num_conditions = 0
else_if_counter = 0
in_if = False
if_locations = []
if_locations_dict = {}
if_dict = {}
if_list = []
if_operations_dict = {}
if_operations_list = []

file_code = open(fname, 'rt')
for line in file_code:
    line_no = line_no + 1
    if re.search(r'\W\s+if\s*',line) and not re.search(r'else',line):
        if_no = if_no + 1
        num_conditions = num_conditions + 1
        if_locations_dict = {}
        if_locations_dict['if_no'] = if_no
        if_locations_dict['start_line'] = line_no
        in_if = True
        if_dict = {}
        if_dict['if_no'] = if_no
        print(line)
        if_dict['if_condition'] = re.findall(r'if\s*\(\s*(.*)\s*\)',line)[0]
        print(if_dict['if_condition'])
        s = re.findall(r'\s*if\s\(.*\)\s*(.*);',line)
        #print('printing s')
        print(s)
        s = re.split(r' ',s[0])
        print(s)
        if_operation_dict = {}
        #if_operation_dict['if_condition'] = re.findall(r'if\s*\(\s*(.*)\s*\)',line)[0]
        if_operation_dict['outout'] = s[0]
        if len(s) == 5:                 # 2 operands operation
            if_operation_dict['condition'] = re.findall(r'if\s*\(\s*(.*)\s*\)',line) 
            if_operation_dict['type'] = 'double'
            if_operation_dict['output'] = s[0] 
            if_operation_dict['assign'] = s[1]
            if_operation_dict['op1'] = s[2]
            if_operation_dict['op2'] = s[5]
            if_operation_dict['operation'] = s[4]
        elif len(s) == 3:                     # 1 operand operation (! ~ & | ^ ~& ~| ~^)
            if_operation_dict['type'] = 'single'
            if re.search('~[&|^]',s[2]):    # if it contains negating operator
                if_operation_dict['output'] = s[0] 
                if_operation_dict['assign'] = s[1]
                if_operation_dict['op1'] = s[2][2:]
                if_operation_dict['operation'] = s[2][:2]
            elif re.search('~',s[2]):
                if_operation_dict['output'] = s[0]
                if_operation_dict['assign'] = s[1] 
                if_operation_dict['op1'] = s[2][1:]
                if_operation_dict['operation'] = s[2][0]
            else:
                if_operation_dict['output'] = s[0]
                if_operation_dict['assign'] = s[1] 
                if_operation_dict['op1'] = s[2]
                if_operation_dict['operation'] = 'nop'
        if_dict['if'] = if_operation_dict
        #print(if_dict)
    elif in_if:
        if re.search(r'\W*else\s+if',line):
            num_conditions = num_conditions + 1
            else_if_counter = else_if_counter + 1 
            if_dict['elif_'+str(else_if_counter)+'_condition']  = re.findall(r'if\s*\(\s*(.*)\s*\)',line)[0]
            #print(if_dict['elif_'+str(else_if_counter)+'_condition'])   
            #print(line)
            s = re.findall(r'\s*else if\s*\(.*\)\s*(.*);',line)
            #print(s)
            s = re.split(r' ',s[0])
            print(s)
            if_operation_dict = {}
            #if_operation_dict['elif_condition'] = re.findall(r'if\s*\(\s*(.*)\s*\)',line)[0]
            if_operation_dict['outout'] = s[0]
            if len(s) == 5:                 # 2 operands operation
                if_operation_dict['condition'] = re.findall(r'if\s*\(\s*(.*)\s*\)',line) 
                if_operation_dict['type'] = 'double'
                if_operation_dict['output'] = s[0] 
                if_operation_dict['assign'] = s[1]
                if_operation_dict['op1'] = s[2]
                if_operation_dict['op2'] = s[4]
                if_operation_dict['operation'] = s[3]
            elif len(s) == 3:                     # 1 operand operation (! ~ & | ^ ~& ~| ~^)
                if_operation_dict['type'] = 'single'
                if re.search('~[&|^]',s[2]):    # if it contains negating operator
                    if_operation_dict['output'] = s[0] 
                    if_operation_dict['assign'] = s[1]
                    if_operation_dict['op1'] = s[2][2:]
                    if_operation_dict['operation'] = s[2][:2]
                elif re.search('~',s[2]):
                    if_operation_dict['output'] = s[0]
                    if_operation_dict['assign'] = s[1] 
                    if_operation_dict['op1'] = s[2][1:]
                    if_operation_dict['operation'] = s[2][0]
                else:
                    if_operation_dict['output'] = s[0]
                    if_operation_dict['assign'] = s[1] 
                    if_operation_dict['op1'] = s[2]
                    if_operation_dict['operation'] = 'nop'
            if_dict['elif_'+str(else_if_counter)] = if_operation_dict
        elif re.search(r'\W*else\s+',line):
            num_conditions = num_conditions + 1
            s = re.findall(r'\s*else \s*(.*);',line)
            print(s)
            s = re.split(r' ',s[0])
            print(s)
            if_operation_dict = {}
            #if_operation_dict['elif_condition'] = re.findall(r'if\s*\(\s*(.*)\s*\)',line)[0]
            if_operation_dict['outout'] = s[0]
            if len(s) == 5:                 # 2 operands operation
                if_operation_dict['condition'] = re.findall(r'if\s*\(\s*(.*)\s*\)',line) 
                if_operation_dict['type'] = 'double'
                if_operation_dict['output'] = s[0] 
                if_operation_dict['assign'] = s[1]
                if_operation_dict['op1'] = s[2]
                if_operation_dict['op2'] = s[5]
                if_operation_dict['operation'] = s[4]
            elif len(s) == 3:                     # 1 operand operation (! ~ & | ^ ~& ~| ~^)
                if_operation_dict['type'] = 'single'
                if re.search('~[&|^]',s[2]):    # if it contains negating operator
                    if_operation_dict['output'] = s[0] 
                    if_operation_dict['assign'] = s[1]
                    if_operation_dict['op1'] = s[2][2:]
                    if_operation_dict['operation'] = s[2][:2]
                elif re.search('~',s[2]):
                    if_operation_dict['output'] = s[0]
                    if_operation_dict['assign'] = s[1] 
                    if_operation_dict['op1'] = s[2][1:]
                    if_operation_dict['operation'] = s[2][0]
                else:
                    if_operation_dict['output'] = s[0]
                    if_operation_dict['assign'] = s[1] 
                    if_operation_dict['op1'] = s[2]
                    if_operation_dict['operation'] = 'nop'
            if_dict['else'] = if_operation_dict
            #print(if_dict)
        elif re.search(r'\s*end',line):
            in_if = False
            if_dict['num_conditions'] = num_conditions
            if_list.append(if_dict)
            if_locations_dict['end_line'] = line_no

print("****************************************************************if operations****************************************************************")
print(if_list)
print('\n\n')



            
parameters_dict = {}
for i in module_params:
    parameters_dict[i] = int(input('Enter the value of paramter ('+i+')'))
print(parameters_dict)


module_ports_size = {}
for i in module_ports:
    if module_ports[i]['size'] in module_params:
        module_ports_size[i] = parameters_dict[module_ports[i]['size']]
    else:
        module_ports_size[i] = module_ports[i]['size']
        
    
print(module_ports_size)

biggest_size = 0
for i in module_ports_size.values():
    if biggest_size < i:
        biggest_size = i

if 'clk' in module_ports:
    clk_period = int(input("Enter Clock period: "))




input_ports = [x for x in module_ports if module_ports[x]['dir'] == 'input' and x != 'clk' and x != 'rst']
output_ports = [x for x in module_ports if module_ports[x]['dir'] == 'output']
internal_pins = [x['name'] for x in internal_signal ]
print(input_ports)
## adding the testbench content
refexists = False
choice = input('Do you want to add a reference model? y/n')
if choice == 'y':
    refexists = True
    refname = input('Enter the name of the reference model: ')
    with open(refname, 'r') as fp:
        line_count = len(fp.readlines())
TB_content = ""
TB_content += '`timescale 1us/1ns\n'
TB_content += 'module ' + module_name + '_tb ();\n'

# adding the TB parameters
for param in parameters_dict:
    TB_content += '\tparameter\t'+param+'_tb = {};\n'.format(parameters_dict[param])

# adding the TB header ports
for port in module_ports:
    if module_ports[port]['dir'] == 'input':
        TB_content += '\treg '
    elif module_ports[port]['dir'] == 'output':
        TB_content += '\twire '
    if module_ports[port]['size'] != 1:
        if module_ports[port]['size'] in module_params:
            TB_content += '\t[' + module_ports[port]['size'] + '_tb - 1 : 0]\t'
        else: 
            TB_content += '\t[{}:0]\t\t\t\t'.format(module_ports[port]['size'] - 1)
    elif module_ports[port]['size'] == 1:
        TB_content += '\t\t\t\t\t\t'
    TB_content += port + '_tb;\n'   
if biggest_size > 1:
    TB_content += '\treg\t\t[{}:0]\t\t\t\tinitial_state;\n'.format(biggest_size)
if choice == 'y':
    for port in module_ports:
        if module_ports[port]['dir'] == 'output':
            TB_content += '\treg '
            if module_ports[port]['size'] != 1:
                if module_ports[port]['size'] in module_params:
                    TB_content += '\t[' + module_ports[port]['size'] + '_tb - 1 : 0]\t'
                else: 
                    TB_content += '\t[{}:0]\t\t\t\t'.format(module_ports[port]['size'] - 1)
            elif module_ports[port]['size'] == 1:
                TB_content += '\t\t\t\t\t\t'
            TB_content += port + '_exp;\n' 



if choice == 'y':
    #adding the test vector
    total_input_size = 0
    for i in input_ports:
        if module_ports[i]['size'] in module_params:
            total_input_size += parameters_dict[module_ports[i]['size']]  
        else:  
            total_input_size += module_ports[i]['size']
    TB_content += '\n\n\treg\t\t[{}:0]\ttest_vect [{}:0];\n'.format(total_input_size - 1, line_count - 1) # we need to parameterize this using user input
    TB_content += '\treg\t\t[31:0]\tvecnum, errors;\n'


TB_content += '\n\n'

# adding the clock generator
if 'clk' in module_ports:
    TB_content += 'always #({})  clk_tb = ~clk_tb;\n'.format(clk_period/2)
    TB_content += '\n\n'

i = 0
# adding the DUT instantiation
TB_content += module_name + ' #(\n'
for param in parameters_dict:
    if i < len(module_params) - 1:
        TB_content += '.'+param+'('+param+'_tb),\n'
    else:
        TB_content += '.'+param+'('+param+'_tb)\n) DUT (\n'
    i += 1
i = 0
for port in module_ports:
    if i < len(module_ports) - 1:
        TB_content += '\t.'+port+'('+port+'_tb),\n'
    else:
        TB_content += '\t.'+port+'('+port+'_tb)\n\t);'
    i += 1

TB_content += '\n\n'






# Initial the clock, reset and the inputs
TB_content += 'initial begin \n\t$dumpfile(\"'+ module_name +'.vcd\");\n\t$dumpvars;\n\n'
if choice == 'y':
    TB_content += '\t$readmemb("' + refname + '",test_vect);'
    TB_content += '\tvecnum = 32\'d0; errors = 32\'d0;\n'
if 'clk' in module_ports:   
    TB_content += '\tclk_tb = 1\'d0;\n\trst_tb = 1\'d1;\n'
    TB_content += '#{}\n'.format(0.2*clk_period)
    TB_content += '\trst_tb = 1\'d0;\n'
    TB_content += '#{}\n'.format(0.5*clk_period)
    TB_content += '\trst_tb = 1\'d1;\n\n'
    TB_content += ''


for port in module_ports:
    if module_ports[port]['dir'] == 'input' and port != 'clk' and port != 'rst':
        if module_ports[port]['size'] in module_params:
            TB_content += '\t' + port + '_tb = ' + '\'b0 ;\n'    
        else:
            TB_content += '\t' + port + '_tb = ' + str(module_ports[port]['size']) + '\'b0 ;\n'
TB_content += '\n\n'

# directed testing
tested_outputs = []
TB_content += '//parsing the case statements\n'
for i in case_list:
    case_parameter = i['parameter'] 
    for j in i['operations']:
        if j['output'] not in tested_outputs:
            tested_outputs.append(j['output'])        
        if j['case'][:-1] not in 'default':
            if j['op1'] in input_ports:
                op1_value = random.randint(0,pow(2,module_ports_size[j['op1']]-1))
                TB_content += '\t'+ str(case_parameter) + '_tb = ' + j['case'][:-1] + '; ' + j['op1'] + '_tb = ' + str(op1_value) + ';'
            elif j['op1'] in output_ports:
                TB_content += '\t'+ str(case_parameter) + '_tb = ' + j['case'][:-1] + '; initial_state = ' + j['op1'] + '_tb;'
            else:
                TB_content += '\t'+ str(case_parameter) + '_tb = ' + j['case'][:-1] + '; '
            if 'op2' in j.keys():
                if j['op2'] in input_ports:
                    op2_value = random.randint(0,pow(2,module_ports_size[j['op2']]-1))
                    TB_content += ' ' + j['op2'] + '_tb = ' + str(op2_value) + ';\n'
            else:
                TB_content += '\n'
            if 'clk' in module_ports:  
                TB_content += '#{}\n'.format(clk_period)
            else:
                TB_content += '#1\n'

            TB_content += '\tif(' + j['output'] + '_tb == ('
            if j['op1'] in input_ports:
                if j['operation'] == '~':
                    TB_content += j['operation'] + j['op1'] + '_tb '
                else:
                    TB_content += j['op1'] + '_tb '
            elif j['op1'] in output_ports:
                TB_content += 'initial_state'
            else:
                TB_content += j['op1']
            if 'op2' in j.keys():
                if j['op2'] in input_ports:
                    TB_content += j['operation'] + ' ' + j['op2'] + '_tb'
                else:
                    TB_content += j['operation'] + ' ' + j['op2']
            
            TB_content += '))\n'
            TB_content += '\t\t$display("Successful Test!");\n'
            TB_content += '\telse\n\t\t$display("Failed Test!");\n'




TB_content += '\n\n'
TB_content += '//parsing the if statements\n'
for i in if_list:
    # get the if operation directed test
    if i['if_condition'][0] != '~':
        TB_content += '\t' + i['if_condition'] + '_tb = 1; '
    else:
        TB_content += '\t' + i['if_condition'][1:] + '_tb = 0; '
    if i['if']['op1'] in input_ports:
        op1_value = random.randint(0,pow(2,module_ports_size[i['if']['op1']]-1))
        TB_content += '\t' + i['if']['op1'] + '_tb = ' + str(op1_value) + ';'
    elif i['if']['op1'] in output_ports:
        TB_content += '\t' + 'initial_state = ' + i['if']['op1'] + '_tb;'
    if 'op2' in i['if'].keys():
        if i['if']['op2'] in input_ports:
            op2_value = random.randint(0,pow(2,module_ports_size[i['if']['op2']]-1))
            TB_content += '\t' + i['if']['op2'] + '_tb = ' + str(op2_value) + ';'
    TB_content += '\n'
    
    if 'clk' in module_ports:  
        TB_content += '#{}\n'.format(clk_period)
    else:
        TB_content += '#1\n'
    
    TB_content += '\tif(' + i['if']['output'] + '_tb == ('
    if i['if']['op1'] in input_ports:
        if i['if']['operation'] == '~':
            TB_content += i['if']['operation'] + i['if']['op1'] + '_tb '
        else:
            TB_content += i['if']['op1'] + '_tb '
    elif i['if']['op1'] in output_ports:
        TB_content += 'initial_state'
    else:
        TB_content += i['if']['op1']
    if 'op2' in i['if'].keys():
        if i['if']['op2'] in input_ports:
            TB_content += i['if']['operation'] + ' ' + i['if']['op2'] + '_tb'
        else:
            TB_content += i['if']['operation'] + ' ' + i['if']['op2']
    TB_content += '))\n'
    TB_content += '\t\t$display("Successful Test!");\n'
    TB_content += '\telse\n\t\t$display("Failed Test!");\n'
    if i['if_condition'][0] != '~':
        TB_content += '\t' + i['if_condition'] + '_tb = 0; '
    else:
        TB_content += '\t' + i['if_condition'][1:] + '_tb = 1; '
    TB_content += '\n'


    # get the else if operation directed test
    for m in range (1, i['num_conditions'] - 1):
        if i['elif_'+str(m)+'_condition'][0] != '~':
            TB_content += '\t' + i['elif_'+str(m)+'_condition'] + '_tb = 1; '
        else:
            TB_content += '\t' + i['elif_'+str(m)+'_condition'][1:] + '_tb = 0; '   
        if i['elif_'+str(m)]['op1'] in input_ports:
            op1_value = random.randint(0,pow(2,module_ports_size[i['elif_'+str(m)]['op1']]-1))
            TB_content += '\t' + i['elif_'+str(m)]['op1'] + '_tb = ' + str(op1_value) + ';'
        elif i['elif_'+str(m)]['op1'] in output_ports:
            TB_content += '\t' + 'initial_state = ' + i['elif_'+str(m)]['op1'] + '_tb;'
        if 'op2' in i['elif_'+str(m)].keys():
            if i['elif_'+str(m)]['op2'] in input_ports:
                op2_value = random.randint(0,pow(2,module_ports_size[i['elif_'+str(m)]['op2']]-1))
                TB_content += '\t' + i['elif_'+str(m)]['op2'] + '_tb = ' + str(op2_value) + ';'
        TB_content += '\n'

        if 'clk' in module_ports:  
            TB_content += '#{}\n'.format(clk_period)
            print(clk_period)
        else:
            TB_content += '#1\n'

        TB_content += '\tif(' + i['elif_'+str(m)]['output'] + '_tb == ('
        if i['elif_'+str(m)]['op1'] in input_ports:
            if i['elif_'+str(m)]['operation'] != 'nop':
                TB_content += i['elif_'+str(m)]['operation'] + i['elif_'+str(m)]['op1'] + '_tb '
            else:
                TB_content += i['elif_'+str(m)]['op1'] + '_tb '
        elif i['elif_'+str(m)]['op1'] in output_ports:
            TB_content += 'initial_state'
        else:
            TB_content += i['elif_'+str(m)]['op1']
        if 'op2' in i['elif_'+str(m)].keys():
            if i['elif_'+str(m)]['op2'] in input_ports:
                TB_content += i['elif_'+str(m)]['operation'] + ' ' + i['elif_'+str(m)]['op2'] + '_tb'
            else:
                TB_content += i['elif_'+str(m)]['operation'] + ' ' + i['elif_'+str(m)]['op2']
        TB_content += '))\n'
        TB_content += '\t\t$display("Successful Test!");\n'
        TB_content += '\telse\n\t\t$display("Failed Test!");\n'
        if i['elif_'+str(m)+'_condition'][0] != '~':
            TB_content += '\t' + i['elif_'+str(m)+'_condition'] + '_tb = 0; '
        else:
            TB_content += '\t' + i['elif_'+str(m)+'_condition'][1:] + '_tb = 1; '
        TB_content += '\n'

    # get the else operation directed test
    if i['else']['op1'] in output_ports:
        TB_content += '\t' + 'initial_state = ' + i['else']['op1'] + '_tb;\n'
    
    if 'clk' in module_ports:  
        TB_content += '#{}\n'.format(clk_period)
    else:
        TB_content += '#1\n'

    TB_content += '\tif(' + i['else']['output'] + '_tb == ('
    if i['else']['op1'] in input_ports:
        if i['else']['operation'] != 'nop':
            TB_content += i['else']['operation'] + i['else']['op1'] + '_tb '
        else:
            TB_content += i['else']['op1'] + '_tb '
    elif i['else']['op1'] in output_ports:
        TB_content += 'initial_state'
    else:
        TB_content += i['else']['op1']
    if 'op2' in i['else'].keys():
        if i['else']['op2'] in input_ports:
            TB_content += i['else']['operation'] + ' ' + i['else']['op2'] + '_tb'
        else:
            TB_content += i['else']['operation'] + ' ' + i['else']['op2']
    TB_content += '))\n'
    TB_content += '\t\t$display("Successful Test!");\n'
    TB_content += '\telse\n\t\t$display("Failed Test!");\n'
    TB_content += '\n\n'

# get the continous assignment directed test
TB_content += '// parsing the continuous assignments\n'
for i in continuous_parameters:
    if i['type'] != 'double conditional':
        if i['op1'] in input_ports:
            op1_value = random.randint(0,pow(2,module_ports_size[i['op1']]-1))
            if i['op1'][0] == '~':
                TB_content += '\t' + i['op1'][1:] + '_tb = ' + str(op1_value) + ';'
            else:
                TB_content += '\t' + i['op1'] + '_tb = ' + str(op1_value) + ';'
        elif i['op1'] in output_ports:
            TB_content += '\t initial_state = ' + i['op1'] + '_tb;'
        if i['type'] == 'double':
            if i['op2'] in input_ports:
                op2_value = random.randint(0,pow(2,module_ports_size[i['op2']]-1))
                TB_content += '\t' + i['op2'] + '_tb = ' + str(op2_value) + ';\n'
        TB_content += '#1\n'
        TB_content += '\tif(' + i['output'] + '_tb == ('
        if i['op1'] in input_ports:
            TB_content += i['op1'] + '_tb '
        elif i['op1'] in output_ports:
            TB_content += 'initial_state '
        if i['type'] == 'double':
            TB_content += i['operation'] + ' ' + i['op2']+ '_tb'
        TB_content += '))\n\t\t$display("Successful Test!");\n'
        TB_content += '\telse\n\t\t$display("Failed Test!");\n'
    else:
        TB_content += '\t' + i['condition'] + '_tb = 1; '
        if i['op1'] in input_ports:
            op1_value = random.randint(0,pow(2,module_ports_size[i['op1']]-1))
            if i['op1'][0] == '~':
                TB_content += '\t' + i['op1'][1:] + '_tb = ' + str(op1_value) + ';\n'
            else:
                TB_content += '\t' + i['op1'] + '_tb = ' + str(op1_value) + ';\n'
            TB_content += '#1\n'
            TB_content += '\tif(' + i['output'] + '_tb == ('
            if i['op1'] in input_ports:
                TB_content += i['op1'] + '_tb '
            elif i['op1'] in output_ports:
                TB_content += 'initial_state '
            TB_content += '))\n\t\t$display("Successful Test!");\n'
            TB_content += '\telse\n\t\t$display("Failed Test!");\n'
    

    TB_content += '\n'


# get the always assignment directed test
TB_content += '// parsing the always assignments\n'
for j in always_operations_list:
  for i in j:
    if i['op1'] in input_ports:
        op1_value = random.randint(0,pow(2,module_ports_size[i['op1']]-1))
        if i['op1'][0] == '~':
            TB_content += '\t' + i['op1'][1:] + '_tb = ' + str(op1_value) + ';'
        else:
            TB_content += '\t' + i['op1'] + '_tb = ' + str(op1_value) + ';'
    elif i['op1'] in output_ports:
        TB_content += '\t initial_state = ' + i['op1'] + '_tb;'
    if i['type'] == 'double':
        if i['op2'] in input_ports:
            op2_value = random.randint(0,pow(2,module_ports_size[i['op2']]-1))
            TB_content += '\t' + i['op2'] + '_tb = ' + str(op2_value) + ';'
    TB_content += '\n#1\n'
    TB_content += '\tif(' + i['output'] + '_tb == ('
    if i['op1'] in input_ports:
        TB_content += i['op1'] + '_tb '
    elif i['op1'] in output_ports:
        TB_content += 'initial_state '
    if i['type'] == 'double':
        TB_content += i['operation'] + ' ' + i['op2']+ '_tb'
    TB_content += '))\n\t\t$display("Successful Test!");\n'
    TB_content += '\telse\n\t\t$display("Failed Test!");\n'
    TB_content += '\n'
TB_content += '\n'

if choice == 'y':
    if 'clk' in module_ports:  
        TB_content += '\trepeat({}) @(negedge clk_tb) begin\n'.format(line_count)       #1000 will be parameterized also according to test_vect
    else:
        TB_content += '\trepeat({}) begin\n'.format(line_count)
    TB_content += '\t\t{'
    for i in input_ports:
        TB_content += i + '_tb, '
    #TB_content += input_ports[-1] + '_tb'
    for i in output_ports[:-1]:
        TB_content += i + '_exp, '
    TB_content += output_ports[-1] + '_exp'
    TB_content += '} = test_vect[vecnum];\n'
    TB_content += '#{}\n'.format(clk_period)
    TB_content += '\t\tif('
    for i in output_ports[:-1]:
        TB_content += i + '_exp == ' + i + '_tb &&'
    TB_content += output_ports[-1] + '_exp == ' + output_ports[-1] + '_tb)\n'
    TB_content += '\t\t\t$display("Successful Test Case!");\n'
    TB_content += '\t\telse begin\n'
    TB_content += '\t\t\t$display("Failed Test Case!");\n'
    TB_content += '\t\t\terrors = errors + 1;\n\t\tend\n'
    TB_content += '\t\tvecnum = vecnum + 1;\n'
    TB_content += '\tend'
    TB_content += '\n\n'



biggestSize = 1  #we check on the number of iterations using the max size of the input
for i in module_ports_size:
    
    if biggestSize < pow(2,module_ports_size[i]): 
        biggestSize = pow(2,module_ports_size[i])
iterations = min(biggestSize,30)


if 'clk' in module_ports:  
    TB_content += '\trepeat({}) @(negedge clk_tb) begin\n'.format(iterations)       #1000 will be parameterized also according to test_vect
else:
    TB_content += '\trepeat({}) begin\n'.format(iterations)
TB_content += '\t#1\n' 
for i in input_ports:
    TB_content += '\t\t' + i + '_tb = $random % {};\n'.format(pow(2,module_ports_size[i]))

TB_content += '\tend'
TB_content += '\n\n'

TB_content += '#100 $stop;'
TB_content += '\n\nend\n\n\n\n'


# initial block of the monitor system
TB_content += 'initial begin \n'
TB_content += '\t$monitor($time, \": ' 
for i in input_ports:
    TB_content += i + ' = %d; '
for i in output_ports[:-1]:
    TB_content += i + ' = %d; '
TB_content += output_ports[-1] + ' = %d; '
TB_content += '\"'

for i in input_ports:
    TB_content += ',' + i + '_tb '
for i in output_ports:
    TB_content += ',' + i + '_tb '
TB_content += ');\n'
TB_content += 'end\n'
TB_content += '\n\n\n'
TB_content += 'endmodule'
print(TB_content)


output_file = fname.replace('.v', '_tb.v') 
with open(output_file, 'w') as f:
        f.write(TB_content)




    

    