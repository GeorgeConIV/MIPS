import cumemu.exceptions as ex

from cumemu.processor import Processor

class Emulator:
    def __init__(self):
        self.processor = Processor()
        self.mem = self.processor.mem
        self.regs = self.processor.reg_file

    def setup(self, filename):
        with open(filename, "rb") as f:
            bitstr = f.read()
            print(len(bitstr))
            instr_gen = ((bitstr[i] << 8) | bitstr[i+1] for i in range(0, len(bitstr), 2))
            for i, instr in enumerate(instr_gen):
                print(instr)
                self.mem.write(i<<1, instr)

    def run(self):
        try:
            return self.processor.run()
        except ex.SyscallInterrupt:
            print("syscall caught!")