import sys
import os

from instruction import Instruction
from scanner import InstructionGen

def PrintUsage():
    print("426 RISC Computer Assembler")
    print("Usage - python main.py <filename>")

if len(sys.argv) < 2:
    PrintUsage()
    exit()
if not os.path.isfile(sys.argv[1]):
    print(f"Error: {sys.argv[1]} is not a recognized file!")
    exit()

ig = InstructionGen(sys.argv[1])
instr_list = list()
for instr in ig:
    instr_list.append(instr)

binary = bytearray()
for instr in instr_list:
    instr.debug()
    binary.extend(instr.binary())

output_f = open(sys.argv[1].split('.')[0].extend(".xgxe"), "wb")
output_f.write(binary)