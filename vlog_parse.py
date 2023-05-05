import hdlparse.verilog_parser as vlog
import re
import random

vlog_ex = vlog.VerilogExtractor()

# taking the filename as an input
fname = input("Enter the name of the file: ")

with open(fname, 'rt') as fh:
  code = fh.read()

vlog_mods = vlog_ex.extract_objects_from_source(code)
vlog_mods = vlog_ex.extract_objects(fname)

## extracting the module name, parameters and input,output ports
module_params = []
module_ports = {}   
'''module_ports = {
    "clk" : {
        "dir"  : "input",
        "size" : 1
    },
    "data_out" : {
        "dir"  : "output",
        "size" : 8
    }
} 
'''
# method to get the port size
def get_vector_size(data_type):
    if re.search(r'\[',data_type):
        msb = re.findall(r'\[\s*(.*):',data_type)[0]
        lsb = re.findall(r'\[.*:\s*(.*)\]',data_type)[0]
        #print(msb)
        #print(lsb)
        return abs(int(msb) - int(lsb) + 1)
    else:
        #print(1)
        return 1

print('\n\n')
module_name = set()
for m in vlog_mods:
  print('Module "{}":'.format(m.name))
  module_name = m.name
  print('  Parameters:')
  for p in m.generics:
    print('\t{:20}{:8}{}'.format(p.name, p.mode, p.data_type))
    module_params.append(p.name)
  print('  Ports:')
  for p in m.ports:
    print('\t{:20}{:20}{}'.format(p.name, p.mode, p.data_type))
    module_ports[p.name] = {"dir": p.mode, "type": ''.join(re.findall("(.*)\s",(p.data_type + ' '))), "size": get_vector_size(p.data_type)}
print(module_ports)

print("\n\n")


############
# me7tageen n3ml preprocessor using (re.sub) le kol el macros abl ma n3bda2 n3ml parse
############

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
        if in_always == True and re.search(r'=',line) :     # contains assignment out <= x + b; 
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
            elif len(s) == 8:                 # case statement with 2 operands
                always_operation_dict['type'] = 'double'
                always_operation_dict['output'] = s[2] 
                always_operation_dict['assign'] = s[3]
                always_operation_dict['op1'] = s[4]
                always_operation_dict['op2'] = s[6][:-1]
                always_operation_dict['operation'] = s[5]
                single_always_operations_list.append(always_operation_dict)
            elif len(s) == 6:   #case statement with 1 operand
                always_operation_dict['type'] = 'single'
                if re.search('~[&|^]',s[4]):    # if it contains negating operator
                    always_operation_dict['output'] = s[2] 
                    always_operation_dict['assign'] = s[3]
                    always_operation_dict['op1'] = s[4][2:][:-1]
                    always_operation_dict['operation'] = s[4][:2]
                elif re.search('~',s[4]):
                    always_operation_dict['output'] = s[2]
                    always_operation_dict['assign'] = s[3] 
                    always_operation_dict['op1'] = s[4][1:][:-1]
                    always_operation_dict['operation'] = s[4][0]
                else:
                    always_operation_dict['output'] = s[2]
                    always_operation_dict['assign'] = s[3] 
                    always_operation_dict['op1'] = s[4][:-1]
                    always_operation_dict['operation'] = 'nop'
                single_always_operations_list.append(always_operation_dict)
                
                
            
print("****************************************************************always operations****************************************************************")
print(single_always_operations_list) 
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
        case_dict['parameter'] = re.findall(r'case\s*\(\s*(.*)\s*\)', line)
        #print(case_dict['parameter'])
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


clk_period = int(input("Enter Clock period: "))


input_ports = [x for x in module_ports if module_ports[x]['dir'] == 'input' and x != 'clk' and x != 'rst']
output_ports = [x for x in module_ports if module_ports[x]['dir'] == 'output']
internal_pins = [x['name'] for x in internal_signal ]

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
TB_content += 'module ' + m.name + '_tb ();\n'

# adding the TB header ports
for port in module_ports:
    if module_ports[port]['dir'] == 'input':
        TB_content += '\treg '
    elif module_ports[port]['dir'] == 'output':
        TB_content += '\twire '
    if module_ports[port]['size'] > 1:
        TB_content += '\t[{}:0]\t'.format(module_ports[port]['size'] - 1)
    elif module_ports[port]['size'] == 1:
        TB_content += '\t\t\t'
    TB_content += port + '_tb;\n'   



if choice == 'y':
    #adding the test vector
    total_input_size = 0
    for i in input_ports:
        total_input_size += module_ports[i]['size']
    TB_content += '\treg\t\t[{}:0]\ttest_vect [1000:0];\n'.format(total_input_size - 1) # we need to parameterize this using user input
    TB_content += '\treg\t\t[31:0]\tvecnum, errors;\n'


TB_content += '\n\n'

# adding the clock generator
if 'clk' in module_ports:
    TB_content += 'always #({})  clk_tb = ~clk_tb;\n'.format(clk_period/2)
    TB_content += '\n\n'

i = 0
# adding the DUT instantiation
TB_content += m.name + ' DUT(\n'
for port in module_ports:
    if i < len(module_ports) - 1:
        TB_content += '\t.'+port+'('+port+'_tb),\n'
    else:
        TB_content += '\t.'+port+'('+port+'_tb)\n\t);'
    i += 1

TB_content += '\n\n'






# Initial the clock, reset and the inputs
TB_content += 'initial begin \n\t$dumpfile(\"'+ m.name +'.vcd\");\n\t$dumpvars;\n\n'
if choice == 'y':
    TB_content += '\t$readmemb("' + refname + '",test_vect);'
    TB_content += '\tvecnum = 32\'d0; errors = 32\'d0;\n'   
TB_content += '\tclk_tb = 1\'d0;\n\trst_tb = 1\'d1;\n'
TB_content += '#{}\n'.format(0.2*clk_period)
TB_content += '\trst_tb = 1\'d0;\n'
TB_content += '#{}\n'.format(0.5*clk_period)
TB_content += '\trst_tb = 1\'d1;\n\n'
TB_content += ''


for port in module_ports:
    if module_ports[port]['dir'] == 'input' and port != 'clk' and port != 'rst':
        TB_content += '\t' + port + '_tb = ' + str(module_ports[port]['size']) + '\'b0 ;\n'
TB_content += '\n\n'
if choice == 'y':
    TB_content += '\trepeat({}) @(negedge clk_tb) begin\n'.format(line_count)       #1000 will be parameterized also according to test_vect
    TB_content += '\t\t{'
    for i in input_ports[:-1]:
        TB_content += i + '_tb, '
    TB_content += i + '_tb'
    TB_content += '} = test_vect[vecnum];\n'
    TB_content += '\t\tvecnum = vecnum + 1;\n'
    TB_content += '\tend'
    TB_content += '\n\n'

biggestSize = 1  #we check on the number of iterations using the max size of the input
for i in module_ports:
    
    if biggestSize < pow(2,module_ports[i]['size']): 
        biggestSize = pow(2,module_ports[i]['size'])
iterations = min(biggestSize,30)


TB_content += '\trepeat({}) @(negedge clk_tb) begin\n'.format(iterations)
for i in input_ports:
    TB_content += '\t\t' + i + '_tb = $random % {};\n'.format(pow(2,module_ports[i]['size']))
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



# checking the continuous assignments
all_assignments = {}
for s in continuous_parameters:
    if s['output'] in output_ports:     # first, check if the assignment is for an output port
        all_assignments[s['output']] = [] #initialize a list whose key is the output name and it contains the input ports related to this output
        if s['type'] == 'single':
            if s['op1'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the always assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['op1'] in input_ports:
                all_assignments[s['output']].append(s['op1'])
        elif s['type'] == 'double':
            print(s['output'] + ' ' + s['type'])
            if s['op1'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the always assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['op1'] in input_ports:
                all_assignments[s['output']].append(s['op1'])
            if s['op2'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['op2'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the continuous assignments
                    if s['op2'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['op2'] in input_ports:
                all_assignments[s['output']].append(s['op2'])
        elif s['type'] == 'double conditional':
            if s['op1'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the always assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['op1'] in input_ports:
                all_assignments[s['output']].append(s['op1'])
            if s['op2'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['op2'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the continuous assignments
                    if s['op2'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['op2'] in input_ports:
                all_assignments[s['output']].append(s['op2'])
            if s['condition'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['condition'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the continuous assignments
                    if s['condition'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['condition'] in input_ports:
                all_assignments[s['output']].append(s['condition'])
        # we need to remove the duplicate if exists
        new_list = []
        for i in all_assignments[s['output']]:
            if i not in new_list:
                new_list.append(i)
        all_assignments[s['output']] = new_list





for s in single_always_operations_list:
    if s['output'] in output_ports:     # first, check if the assignment is for an output port
        all_assignments[s['output']] = [] #initialize a set whose key is the output name and it contains the input ports related to this output
        if s['type'] == 'single':
            if s['op1'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                print(s['op1'])
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            print(q['type'])
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the always assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['op1'] in input_ports:
                all_assignments[s['output']].append(s['op1'])
        elif s['type'] == 'double':
            print(s['output'] + ' ' + s['type'] + ' ' + s['op1'] + ' ' + s['op2'])
            if s['op1'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the always assignments
                    if s['op1'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['op1'] in input_ports:
                all_assignments[s['output']].append(s['op1'])
            if s['op2'] in internal_pins:   # if operand 1 is an internal signal, then we need to take its inputs 
                print(s['output'] + ' ' + s['op2'])
                for q in continuous_parameters: # look for the internal singal in the continuous assignments
                    if s['op2'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                        if q['type'] == 'double conditional':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
                            if q['condition'] in input_ports:
                                all_assignments[s['output']].append(q['condition'])
                for q in single_always_operations_list: # look for the internal singal in the continuous assignments
                    if s['op2'] in q['output']: # if it exists as an output, we take its inputs to the all_assignments[output]
                        if q['type'] == 'single':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                        if q['type'] == 'double':
                            if q['op1'] in input_ports:
                                all_assignments[s['output']].append(q['op1'])
                            if q['op2'] in input_ports:
                                all_assignments[s['output']].append(q['op2'])
            elif s['op2'] in input_ports:
                all_assignments[s['output']].append(s['op2'])
        # we need to remove the duplicate if exists
        new_list = []
        for i in all_assignments[s['output']]:
            if i not in new_list:
                new_list.append(i)
        all_assignments[s['output']] = new_list




print(all_assignments)



#def get_input_from_internal_signals():



#TB_content += 
#print(TB_content)

