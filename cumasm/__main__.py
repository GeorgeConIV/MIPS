import sys
import os
import argparse

from cumasm.instruction import Instruction
from cumasm.scanner import InstructionGen

p = argparse.ArgumentParser()
p.add_argument("-o","--output")
p.add_argument("filename")

args = p.parse_args()

ig = InstructionGen(args.filename)
instr_list = list()
for instr in ig:
    instr_list.append(instr)

binary = bytearray()
for instr in instr_list:
    # instr.debug()
    binary.extend(instr.binary())

out_name = args.output if args.output is not None else "a"
output_f = open(out_name + ".cum", "wb")
output_f.write(binary)