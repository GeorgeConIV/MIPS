import sys
import os
import argparse
import pprint

import cumasm.globals as g

from cumasm.instruction import Instruction
from cumasm.scanner import InstructionGen

p = argparse.ArgumentParser()
p.add_argument("-v", "--verbose", help="prints step-by-step output", action="store_true")
p.add_argument("-o","--output", help="output filename (defaults to a.cum)")
p.add_argument("filename", help="assembly file to assemble")

args = p.parse_args()

g.verbose = args.verbose

ig = InstructionGen(args.filename)
instr_list = list()
for instr in ig:
    instr_list.append(instr)

binary = bytearray()
for instr in instr_list:
    if g.verbose:
        instr.debug()
    binary.extend(instr.binary())

out_name = (args.output if args.output is not None else "a") + ".cum"
if g.verbose:
    print(f"Output name: {out_name}")
output_f = open(out_name, "wb")
output_f.write(binary)

if g.verbose:
    print("\nLabel Map:\n{")
    for key in g.label_map:
        print(f"\t{key}\t:\t{hex(g.label_map[key])}")
    print("}")