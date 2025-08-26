import mcschematic
import random
import math as m

schem = mcschematic.MCSchematic()

with open('./bin_instructions.txt','r') as file:
    instructions = [line.strip() for line in file if line.strip()]

x = 2
z = -2
facing = 'north'
x_offs = 0
mem_line = 0

for instruction in instructions:
    y = 0
    for byte in instruction.split():
        for bit in byte:
            block = f"minecraft:repeater[facing={facing}]" if bit == '1' else "minecraft:black_wool"
            schem.setBlock((x + x_offs, y, z), block)
            y -= 2
        y -= 2
    if facing == 'north':
        z += 4
        facing = 'south'
    else:
        z += 5
        x_offs ^= 1
        facing = 'north'
    if mem_line == 15:
        mem_line = 0
        z = -2
        x += 2
    else:
        mem_line += 1

Name = 'v2ROM' + str(random.randint(1000,1999))
print(Name)
schem.save("schematics", Name, mcschematic.Version.JE_1_20_1)