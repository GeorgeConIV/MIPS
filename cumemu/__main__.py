import argparse

from cumemu.emulator import Emulator

p = argparse.ArgumentParser()
p.add_argument("filename")
args = p.parse_args()

emu = Emulator()
emu.setup(args.filename)

op_names = ["nop", "add", "addi", "sub", "subi", "mul", "muli", "div",
    "divi", "shift", "li", "mov", "cmp", "and", "andi", "or", "ori",
    "xor", "xori", "not", "bic", "lda", "ldc", "ldo", "str", "sto",
    "b", "br", "call", "ret", "single-op", "syscall"]

if __name__ == "__main__":
    while True:
        instr = emu.run()
        print("Instruction: " + str(instr) + " " + op_names[(instr.bytes()[0] & 0xF8) >> 3])
        print(emu.regs)
        input("Press any key to continue...")