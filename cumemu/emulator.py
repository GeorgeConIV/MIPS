import cumemu.exceptions as ex

from cumemu.processor import Processor

class Emulator:
    def setup(self, filename):
        self.processor = Processor()
        self.mem = self.processor.mem

        with open(filename, "rb") as f:
            bitstr = f.read()
            instr_gen = ((bitstr[i] << 8) | bitstr[i+1] for i in range(0, len(bitstr), 2))
            for i, instr in enumerate(instr_gen):
                self.mem.write(i<<1, instr)

    def run(self):
        try:
            self.processor.run()
        except ex.SyscallInterrupt:
            print("syscall caught!")