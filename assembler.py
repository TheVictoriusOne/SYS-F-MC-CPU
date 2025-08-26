import re

with open('instruction_map.txt') as file:
    instr_map = file.read().split('\n')
with open('asm_code.txt') as file:
    asm_instr= file.read().split('\n')

# Parse registers
for i, word in enumerate(instr_map):
    if word == '[Registers]':
        break
registers = {}
while True:
    i += 1
    while instr_map[i] == '':
        i += 1
    if instr_map[i] == '[Mnemomics]':
        break
    parts = instr_map[i].split(' ')
    registers[parts[0]] = parts[1]

# Parse Mnemomics
OP = []
while i + 1 < len(instr_map):
    i += 1
    while instr_map[i] == '':
        i += 1
        if i >= len(instr_map):
            break
    if i >= len(instr_map):
            break
    parts = instr_map[i].split(' ')
    i += 1
    OP.append([[parts[0], parts[1:]], instr_map[i].split(' ')])

# Parse all labels in the Assembly code

i = 0
labels = {}

for text in asm_instr:
    text = text.strip()
    if not text or text.startswith("#"):
        continue
    if text.endswith(":"):
        labels[text[:-1]] = format(i, "08b")
    else:
        i += 1


def grab_opcode(OPC):
    return [idx for idx, ((mnemonic, _), _) in enumerate(OP) if mnemonic == OPC]

def split_opcode(op):
    parts = op.strip().split(None, 1)
    return [parts[0], [o.strip() for o in parts[1].split(",")]] if len(parts) > 1 else [parts[0], []]

i = -1
instructions = []
while i + 1 < len(asm_instr):
    i += 1
    while i < len(asm_instr) and (asm_instr[i] == '' or asm_instr[i][-1] == ':') or asm_instr[i][0] == '#':
        i += 1
    if i >= len(asm_instr):
        break

    split_op = split_opcode(asm_instr[i])
    indices = grab_opcode(split_op[0])

    operand_forms = []
    for idx in indices:
        specs = OP[idx][0][1]
        form = []
        for val in specs:
            if not val.strip():
                raise SystemExit(f"Empty operand descriptor for {split_op[0]} (idx {idx})")
            m = re.search(r'([A-Za-z])\s*\(\s*([A-Za-z])', val)
            if not m:
                raise SystemExit(f"Invalid operand format '{val}' in {split_op[0]} (idx {idx})!")
            form.append([m.group(1), m.group(2)])
        operand_forms.append(form)

    types = [('l' if op in labels else 'r' if op in registers else 'i') for op in split_op[1]]

    for num, idx in enumerate(operand_forms):
        if [t[1] for t in idx] == types:
            break
    else:
        raise ValueError(f"No viable operand type match for instruction: {split_op[0]} {', '.join(split_op[1])}")
    
    selected_instr = OP[indices[num]]
    
    modes = selected_instr[0][1]
    binary = selected_instr[1]
    values = split_op[1]
    letters = [x[0] for x in operand_forms[num]]
    
    reference_binary = []
    
    for num, type_ in enumerate(types):
        if type_ == 'l':
            reference_binary.append(labels[values[num]])
        elif type_ == 'r':
            reference_binary.append(registers[values[num]])
        elif type_ == 'i':
            if values[num][0] == 'b':
                reference_binary.append(values[num][1:len(values[num])])
            else:
                reference_binary.append(format(int(values[num]), '08b'))
                pass
        else:
            raise SystemExit("There is a reference to an incorrect value type.")
        


    
    instruction = []

    for token in binary:

        if re.search(r'[A-Za-z]', token) and not (len(token) == 8 and token.isalpha()):
            new_token = token

            for group in re.finditer(r'([A-Za-z]+)', token):
                letters_group = group.group(1)

                try:
                    idx_operand = letters.index(letters_group[0])
                except ValueError:
                    raise SystemExit(f"Could not find operand for letter {letters_group[0]}")

                imm_value = int(reference_binary[idx_operand], 2)

                replacement = format(imm_value, f'0{len(letters_group)}b')

                new_token = new_token.replace(letters_group, replacement, 1)
            instruction.append(new_token)
        elif token[0] == '0' or token[1] == '1':
            instruction.append(token)
        else:
            index = letters.index(token[0])
            instruction.append(reference_binary[index])
    instructions.append(instruction)
    
for i in instructions:

    print(i[0], i[1], i[2], i[3])
