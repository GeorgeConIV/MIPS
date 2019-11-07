import cumemu.exceptions as ex

from cumemu.int16 import Int16

class InstructionDecoder:
    def bitToInt16(self, x, bit_len):
        if (x & (1 << (bit_len - 1))) != 0:
            x = -((1 << bit_len) - x)
        return Int16(x)

    def decode(self, hi, lo):
        self.op = (hi & 0xF8) >> 3
        self.rs = (hi & 0x7) << 1 | (lo & 0x80) >> 7
        self.rt = (lo & 0x78) >> 3
        self.cond = lo & 0x7

        self.rt_imm = Int16(self.rt)
        self.imm = self.bitToInt16(lo & 0x7F, 7)
        self.l_imm = self.bitToInt16((hi & 0x7) << 8 | lo, 11)
        self.b_address = self.bitToInt16((hi & 0x7) << 5 | (lo & 0xF8) >> 3, 8)

class RegisterFile:
    def __init__(self):
        self.registers = [Int16(0) for _ in range(16)]

    def write(self, reg, x):
        self.registers[reg].set(x)

    def read(self, reg):
        return self.registers[reg]

    def __str__(self):
        return '\n'.join(["Registers: {"]+[f"\tR{i}: " + str(reg) for i, reg in enumerate(self.registers)]+["}"])

class ALU:
    def update(self, a, b, ctrl):
        self.a = a
        self.b = b
        self.ctrl = ctrl
        self.out = [
            lambda x, y : x + y,    # add
            lambda x, y : x - y,    # sub
            lambda x, y : x * y,    # mul
            lambda x, y : x / y,    # div
            lambda x, y : x & y,    # and
            lambda x, y : x | y,    # or
            lambda x, y : x ^ y,    # xor
            lambda x, y : x & ~y,   # bic
            lambda x, y : x << y,   # lsl
            lambda x, y : x >> y,   # lsr
            lambda x, y : Int16(x.actual >> y.actual), # asr 
            lambda x, y : ~x        # not
        ][ctrl](a, b)
    
class Memory:
    def __init__(self):
        self.memspace = [Int16(0) for _ in range(512)]

    def write(self, address, x):
        try:
            if (address % 2) != 0:
                raise ex.MemoryAccessFault("Address not on word boundary")
            self.memspace[address>>1].set(x)
        except IndexError:
            raise ex.MemoryAccessFault("Address outside of memory space")

    def read(self, address):
        try:
            if (address % 2) != 0:
                raise ex.MemoryAccessFault("Address not on word boundary")
            return self.memspace[address>>1]
        except IndexError:
            raise ex.MemoryAccessFault("Address outside of memory space")
            
class ControlUnit:
    # lookup tables for the various opcodes
    has_cond = [False, True, False, True, False, True, False, True,
        False, False, False, True, True, True, False, True, False,
        True, False, True, True, False, False, True, False, True,
        True, True, False, False, True, False]

    def __init__(self):
        self.z = False
        self.n = False
        self.c = False
        self.v = False

        self.RegWr = False
        self.Push = False
        self.Pop = False
        self.RegDst = 0
        self.ImmSel = 0
        self.ALUSrc = 0
        self.BAdd = 0
        self.BrSel = 0
        self.ALUCntr = 0
        self.MemSel = 0
        self.MemRd = False
        self.MemWr = False
        self.NotSel = 0
        self.WbSel = 0
        self.Call = False
        self.Ret = False

    def updateFlags(self, z, n, c, v):
        self.z = z
        self.n = n
        self.c = c
        self.v = v

    def checkCond(self, op):
        return [
            lambda: True,                               # NULL
            lambda: self.z == 1,                        # EQ
            lambda: self.z != 1,                        # NE
            lambda: self.n != self.v,                   # LT
            lambda: not self.z or not self.n != self.v, # GT
            lambda: self.z or self.n != self.v,         # LTE
            lambda: not self.n != self.v,               # GTE
            lambda: self.z == 1                         # EQZ
        ][op]()

    def updateSigs(self, RegWr = False, Push = False, Pop = False, RegDst = 0, ImmSel = 0,
                   ALUSrc = 0, ALUCntr = 0, BAdd = 0, BrSel = 0, MemSel = 0, MemRd = False,
                   MemWr = False, NotSel = 0, WbSel = 1, Call = False, Ret = False):
        self.RegWr = RegWr
        self.Push = Push
        self.Pop = Pop
        self.RegDst = RegDst
        self.ImmSel = ImmSel
        self.ALUSrc = ALUSrc
        self.ALUCntr = ALUCntr
        self.BAdd = BAdd
        self.BrSel = BrSel
        self.MemSel = MemSel
        self.MemRd = MemRd
        self.MemWr = MemWr
        self.NotSel = NotSel
        self.WbSel = WbSel
        self.Call = Call
        self.Ret = Ret

    def update(self, op, cond, sel):
        if self.has_cond[op] and (not self.checkCond(cond)):
            self.updateSigs()
            return

        [
            lambda: self.updateSigs(),                                  # NOP
            lambda: self.updateSigs(RegWr=True),                        # ADD
            lambda: self.updateSigs(RegWr=True, ALUSrc=1),              # ADDI
            lambda: self.updateSigs(RegWr=True, ALUCntr=1),             # SUB
            lambda: self.updateSigs(RegWr=True, ALUCntr=1, ALUSrc=1),   # SUBI
            lambda: self.updateSigs(RegWr=True, ALUCntr=2),             # MUL
            lambda: self.updateSigs(RegWr=True, ALUCntr=2, ALUSrc=1),   # MULI
            lambda: self.updateSigs(RegWr=True, ALUCntr=3),             # DIV
            lambda: self.updateSigs(RegWr=True, ALUCntr=3, ALUSrc=1),   # DIVI
            lambda: None,                                               # shifts
            lambda: self.updateSigs(RegWr=True, RegDst=1, WbSel=3),     # LI
            lambda: self.updateSigs(RegWr=True, RegDst=1, WbSel=2),     # MOV
            lambda: self.updateSigs(ALUCntr=1),                         # CMP
            lambda: self.updateSigs(RegWr=True, ALUCntr=4),             # AND
            lambda: self.updateSigs(RegWr=True, ALUCntr=4, ALUSrc=1),   # ANDI
            lambda: self.updateSigs(RegWr=True, ALUCntr=5),             # OR
            lambda: self.updateSigs(RegWr=True, ALUCntr=5, ALUSrc=1),   # ORI
            lambda: self.updateSigs(RegWr=True, ALUCntr=6),             # XOR
            lambda: self.updateSigs(RegWr=True, ALUCntr=6, ALUSrc=1),   # XORI
            lambda: self.updateSigs(RegWr=True, WbSel=1, ALUCntr=11),   # NOT
            lambda: self.updateSigs(RegWr=True, ALUCntr=7),             # BIC
            lambda: self.updateSigs(RegWr=True, ImmSel=1, WbSel=3),     # LDA
            lambda: self.updateSigs(RegWr=True, ImmSel=1, WbSel=3),     # LDC
            lambda: self.updateSigs(RegWr=True, MemRd=True, WbSel=0),   # LDO
            lambda: self.updateSigs(MemSel=1, ImmSel=1, MemWr=True),    # STR
            lambda: self.updateSigs(MemWr=True),                        # STO
            lambda: self.updateSigs(BrSel=1),                           # B
            lambda: self.updateSigs(BrSel=2),                           # BR
            lambda: self.updateSigs(Call=True, BrSel=1),                # CALL
            lambda: self.updateSigs(Ret=True),                          # RET
            lambda: None,                                               # single-op
            lambda: self.updateSigs()                                   # SYSCALL
        ][op]()

        #LSL,LSR,ASR
        if op == 0x09:
            if cond == 0:
                self.updateSigs(RegWr=True, ALUCntr=8, ALUSrc=2)
            elif cond == 1:
                self.updateSigs(RegWr=True, ALUCntr=9, ALUSrc=2)
            elif cond == 2:
                self.updateSigs(RegWr=True, ALUCntr=10, ALUSrc=2)

        #PUSH, POP, INC, DEC
        elif op == 0x1E:
            if sel == 1:
                self.updateSigs(Push=True)
            elif sel == 2:
                self.updateSigs(Pop=True)
            elif sel == 4:
                self.updateSigs(ALUSrc=3, RegWr=True, RegDst=1)
            elif sel == 8:
                self.updateSigs(ALUSrc=3, RegWr=True, ALUCntr=1, RegDst=1)

        #SYSCALL
        elif op == 0x1F:
            raise ex.SyscallInterrupt