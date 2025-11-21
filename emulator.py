import pygame as pg
RES = (600, 600)
screen = pg.display.set_mode(RES)
lamp_size = RES[0] / 16, RES[1] / 16
screen.fill((0,0,0))

file = open('bin_instructions.txt')
prog = file.read().split('\n')
file.close()

ALU =  [lambda: ARG1 + ARG2,
        lambda: ARG1 - ARG2,
        lambda: ARG1 ^ ARG2,
        lambda: ~(ARG1 ^ ARG2),
        lambda: ARG1 | ARG2,
        lambda:  ~(ARG1 | ARG2),
        lambda: ARG1 & ARG2,
        lambda: ~(ARG1 & ARG2)] 
CMP =  [lambda: ARG1 <  ARG2,
        lambda: ARG1 <= ARG2,
        lambda: ARG1 == ARG2,
        lambda: ARG1 != ARG2,
        lambda: ARG1 >= ARG2,
        lambda: ARG1 >  ARG2,]

RAM = [0]*28
PC = 0
HALT = False
while not HALT:
    data = prog[PC].split(' ')
    if data[0] == '11110011': HALT = True
    if data[0][0] == '1': ARG1 = int(data[1], 2)
    else: ARG1 = RAM[int(data[1], 2)]
    if data[0][1] == '1': ARG2 = int(data[2], 2)
    else: ARG2 = RAM[int(data[2], 2)]
    calc = int(data[0], 2) & 7
    if data[0][2] == '0': RAM[int(data[3], 2)] = ALU[calc]()
    elif CMP[calc](): PC = int(data[3], 2) - 1
    if data[3] == '00011011':
        print(RAM[27])
        x, y = RAM[27] & 15, 16 - (RAM[27] >> 4) & 15
        pg.draw.rect(screen,(200, 170, 60), (x*lamp_size[0], y*lamp_size[1], lamp_size[0]*1.02, lamp_size[1]*1.02))
    PC += 1

enabled = True
pg.display.flip()
while enabled:
    for event in pg.event.get():
        if event.type == pg.QUIT:
           enabled = False