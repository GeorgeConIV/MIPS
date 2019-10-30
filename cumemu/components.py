import cumemu.exceptions as ex

from cumemu.int16 import Int16

class InstructionDecoder:
    def bitToInt16(self, x, bit_len):
        if (x & (1 << bit_len)) != 0:
            x = -((1 << (bit_len+1)) - x)
        return Int16(x)

    def decode(self, hi, lo):
        self.op = (hi & 0xF8) >> 3
        self.rs = (hi & 0x7) << 1 | (lo & 0x80) >> 7
        self.rt = (lo & 0x78) >> 3
        self.cond = lo & 0x7

        self.imm = self.bitToInt16(lo & 0x7F, 7)
        self.l_imm = self.bitToInt16((hi & 0x7) << 8 | lo, 11)
        self.b_address = self.bitToInt16((hi & 0x7) << 5 | (lo & 0xF8) >> 3, 8)

class RegisterFile:
    def __init__(self):
        self.registers = [Int16(0) for _ in range(15)]

    def write(self, reg, x):
        self.registers[reg].set(x)

    def read(self, reg):
        return self.registers[reg]

class ALU:
    def update(self, a, b, ctrl):
        self.a = a
        self.b = b
        self.ctrl = ctrl
        self.out = [
            lambda x, y : x + y,
            lambda x, y : x - y,
            lambda x, y : x * y,
            lambda x, y : x / y,
            lambda x, y : x & y,
            lambda x, y : x | y,
            lambda x, y : x ^ y,
            lambda x, y : x & ~y
        ][ctrl](a, b)
    
class Memory:
    def __init__(self):
        self.memspace = [Int16(0) for _ in range(512)]

    def writeWord(self, address, x):
        try:
            if (address % 2) != 0:
                raise ex.MemoryAccessFault("Address not on word boundary")
            self.memspace[address>>1].set(x)
        except IndexError:
            raise ex.MemoryAccessFault("Address outside of memory space")

    def readWord(self, address):
        try:
            if (address % 2) != 0:
                raise ex.MemoryAccessFault("Address not on word boundary")
            return self.memspace[address>>1]
        except IndexError:
            raise ex.MemoryAccessFault("Address outside of memory space")
            
class ControlUnit:
    # lookup tables for the various opcodes
    has_cond = [False, True, False, True, False, True, False, True,
        False, False, True, True, True, True, False, True, False,
        True, False, True, True, False, False, True, False, True,
        True, True, False, False, True, False]

    def __init__(self):
        self.z = False
        self.n = False
        self.c = False
        self.v = False

    def updateFlags(self, z, n, c, v):
        self.z = z
        self.n = n
        self.c = c
        self.v = v

    def update(self, op, cond, sel):
        pass
        # 