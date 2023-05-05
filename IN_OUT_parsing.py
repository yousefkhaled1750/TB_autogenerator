import re
fname = input("Enter the name of the file: ")

with open(fname, 'rt') as fh:
  code = fh.read()
parameters    = []
input_ports   = []
output_ports  = []
file_code = open(fname, 'rt')
for line in file_code:
    if re.search(r'^module\s|\s+module\s',line):
        s = re.split(r'\s',line)
        module_name = str(re.findall(r'\s*\w+\s*',s[-3]))[2:][:-2]        
print(module_name)

file_code = open(fname, 'rt')
for line in file_code:
    if re.search(r'^parameter\s|\s+parameter\s',line):
        s = re.split(r'\s',line)
        name_param = str(re.findall(r'\s*\w+\s*',s[-4]))[2:][:-2]   
        print(name_param)
        parameters.append(name_param)
        
file_code = open(fname, 'rt')
for line in file_code:
    signal = {}
    if re.search(r'^input\s|\s+input\s',line):
        if re.search(r'\s+wire\s',line):
            if re.search(r'\[',line):
                s = re.split(r'\[|\]',line)
                name = str(re.findall(r'\s*(.*)\s*,',s[2]))[2:][:-2]
                if re.search(r'^[A-Za-z]\w*-',s[1]):
                    size = str(re.findall((r'(.*)-'),s[1]))[2:][:-2]
                else:
                    size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                signal["name"] = name
                signal["type"] = 'wire'
                signal["size"] = size         
                input_ports.append(signal)
            else:
                s = re.split(r'\s+',line)
                name = str(re.findall(r'\s*(.*),',s[-2]))[2:][:-2]
                signal["name"] = name
                signal["type"] = 'wire'
                signal["size"] = int(1)
                input_ports.append(signal)
        elif re.search(r'\s+reg\s',line):
            if re.search(r'\[',line):
                s = re.split(r'\[|\]',line)
                name = str(re.findall(r'\s*(.*)\s*,',s[2]))[2:][:-2]
                if re.search(r'^[A-Za-z]\w*-',s[1]):
                    size=str(re.findall((r'(.*)-'),s[1]))
                else:
                    size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                signal["name"] = name
                signal["type"] = 'reg'
                signal["size"] = size         
                input_ports.append(signal)
            else:
                s = re.split(r'\s+',line)
                name = str(re.findall(r'\s*(.*),',s[-2]))[2:][:-2]
                signal["name"] = name
                signal["type"] = 'reg'
                signal["size"] = int(1)
                input_ports.append(signal)
    elif re.search(r'^output\s|\s+output\s',line):
        if re.search(r'\s+wire\s',line):
            if re.search(r'\[',line):
                s = re.split(r'\[|\]',line)
                name = str(re.findall((r'\w+,|\w+\)'),s[2]))[2:][:-3]
                #print(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2])
                #print(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1])))
                if re.search(r'^[A-Za-z]\w*-',s[1]):
                    size=str(re.findall((r'(.*)-'),s[1]))
                else:
                    size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                signal["name"] = name
                signal["type"] = 'wire'
                signal["size"] = size         
                output_ports.append(signal)
            else:
                s = re.split(r'\s+',line)
                name = str(re.findall(r'\w+',s[-2]))[2:][:-2]
                signal["name"] = name
                signal["type"] = 'wire'
                signal["size"] = int(1)
                output_ports.append(signal)
        elif re.search(r'\s+reg\s',line):
            if re.search(r'\[',line):
                s = re.split(r'\[|\]',line)
                name = str(re.findall((r'\w+,|\w+\)'),s[2]))[2:][:-3]
                #print(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2])
                #print(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1])))
                if re.search(r'^[A-Za-z]\w*-',s[1]):
                    size=str(re.findall((r'(.*)-'),s[1]))
                else:
                    size = int(str(re.findall(r'([0-9]*).*:',s[1]))[2:][:-2]) - int(str(re.findall(r'.*:\s*([0-9]*)\s*',s[1]))[2:][:-2]) + 1
                signal["name"] = name
                signal["type"] = 'reg'
                signal["size"] = size         
                output_ports.append(signal)
            else:
                s = re.split(r'\s+',line)
                name = name = str(re.findall(r'\w+',s[-2]))[2:][:-2]
                signal["name"] = name
                signal["type"] = 'reg'
                signal["size"] = int(1)
                output_ports.append(signal)
        
print('\n')
print(input_ports)
print('\n\n')
print(output_ports)
print('\n\n')
print(parameters)
print('\n\n')

    