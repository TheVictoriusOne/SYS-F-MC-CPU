# SYS-F-MC-CPU
A simple repository containing everything to write code in custom assembly and load it directly into the instruction rom of my redstone computer architecture.


## What are the specifications of the computer?
- The computer has 27 registers and one primitive IO port.
- The Minecraft computer can perform 1 instruction every 5-6 seconds (still figuring out at what clockrate it is still stable)
- Despite being slow, it can still do quite a bit due to its 4 byte instruction width.
- There can be a total of up to 256 instructions, however if i somehow figure out a way to utilize the 9th bit, it'll be able to address up to 512 instructions.
- The ALU can perform 8 operations. ADD, SUBTRACT, XOR, XNOR, OR, NOR, AND & NAND.
- A 16x16 matrix screen is directly connected to the IO port, allowing for plotting, or rendering images (very slowly)


## Where can I find/get the computer?
You can find the computer on the Minecraft ORE server, on the build plot of victor_the_king.
However, I'll also provide a schematic containing the entire computer which you can download.


## How do I use the computer?
It comes preprogrammed with a program drawing "Hello World!" onto the screen.
To run it you simply flip the lever named START CLOCK.
To restart the computer, simply press the button named RESET COUNTER, which resets the program counter back to the first instruction.


## How do I write my own code for the computer?
First things first you have to open the text file named "asm_code.txt" and within this text file, you can write your assembly code.
To know which instructions the assembly supports, or even possibly add/edit a few instructions, open the text file named "instruction_map.txt".

After you're done writing the assembly code, simply start the program "assembler.py" and copy paste the resulting binary code into the text file "bin_instructions.txt".
Eventually I'll have modified or constructed my own emulator which you'll be able to simply boot it with the "bin_instructions.txt".
To run it in Minecraft, you'll first have to run the program "v2_schematic.py" and put the resulting .schem file into your worldedit schematics folder.
At the top right of the program memory, there's a single white block with a sign on it. Stand on there while pasting the schematic into the program memory. (Make sure to not forget pasting it with -a at the end!)

