from random import randint

import cumemu.exceptions as ex

from cumemu.processor import Processor
from cumemu.int16 import Int16

class Emulator:
    def __init__(self):
        self.processor = Processor()
        self.mem = self.processor.mem
        self.regs = self.processor.reg_file

        self.pc = self.regs.read(12)
        self.ar = self.regs.read(15)

    def setup(self, filename):
        with open(filename, "rb") as f:
            bitstr = f.read()
            instr_gen = ((bitstr[i] << 8) | bitstr[i+1] for i in range(0, len(bitstr), 2))
            for i, instr in enumerate(instr_gen):
                self.mem.write(i<<1, instr)

    def setAccumulator(self, x):
        self.ar.set(x)

    def run(self):
        try:
            self.processor.run()
        except ex.SyscallInterrupt:
            cmd = self.ar.actual
            if cmd == 0:
                return "Program has halted."
            elif cmd == 1:
                self.ar.set(randint(-500, 500))
            elif cmd == 2:
                self.pc.set(self.pc + Int16(2))
                return "user entry"
            else:
                return f"Syscall command '{cmd}' not supported."
        except ex.MemoryAccessFault:
            return "Memory access out of bounds."
        except ZeroDivisionError:
            return "Division by zero."
