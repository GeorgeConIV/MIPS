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
        self.registers = [Int16(0) for _ in range(16)]

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
        False, False, True, True, True, True, False, True, False,
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
        ][op]

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

        #NOP
        if op == 0x00:
            self.updateSigs()

        #ADD
        elif op == 0x01:
            self.updateSigs(RegWr=True)

        #ADDI
        elif op == 0x02:
            self.updateSigs(RegWr=True, ALUSrc=1)

        #SUB
        elif op == 0x03:
            self.updateSigs(RegWr=True, ALUCntr=1)

        #SUBI
        elif op == 0x04:
            self.updateSigs(RegWr=True, ALUCntr=1, ALUSrc=1)

        #MUL
        elif op == 0x05:
            self.updateSigs(RegWr=True, ALUCntr=2)

        #MULI
        elif op == 0x06:
            self.updateSigs(RegWr=True, ALUCntr=2, ALUSrc=1)

        #DIV
        elif op == 0x07:
            self.updateSigs(RegWr=True, ALUCntr=3)

        #DIVI
        elif op == 0x08:
            self.updateSigs(RegWr=True, ALUCntr=3, ALUSrc=1)

        #LSL,LSR,ASR
        elif op == 0x09:
            if cond == 0:
                self.updateSigs(RegWr=True, ALUCntr=8, ALUSrc=2)
            elif cond == 1:
                self.updateSigs(RegWr=True, ALUCntr=9, ALUSrc=2)
            elif cond == 2:
                self.updateSigs(RegWr=True, ALUCntr=10, ALUSrc=2)

        #TAR
        elif op == 0x0A:
            self.updateSigs(RegWr=True, RegDst=1, WbSel=2)

        #MOV
        elif op == 0x0B:
            self.updateSigs(RegWr=True, RegDst=1, WbSel=2)

        #CMP
        elif op == 0x0C:
            self.updateSigs(ALUCntr=1)

        #AND
        elif op == 0x0D:
            self.updateSigs(RegWr=True, ALUCntr=4)

        #ANDI
        elif op == 0x0E:
            self.updateSigs(RegWr=True, ALUCntr=4, ALUSrc=1)

        #OR
        elif op == 0x0F:
            self.updateSigs(RegWr=True, ALUCntr=5)

        #ORI
        elif op == 0x10:
            self.updateSigs(RegWr=True, ALUCntr=5, ALUSrc=1)

        #XOR
        elif op == 0x11:
            self.updateSigs(RegWr=True, ALUCntr=6)

        #XORI
        elif op == 0x12:
            self.updateSigs(RegWr=True, ALUCntr=6, ALUSrc=1)

        #NOT
        elif op == 0x13:
            self.updateSigs(RegWr=True, WbSel=1, ALUCntr=11)

        #BIC
        elif op == 0x14:
            self.updateSigs(RegWr=True, ALUCntr=7)

        #LDA
        elif op == 0x15:
            self.updateSigs(RegWr=True, ImmSel=1, MemSel=1, MemRd=True, WbSel=0)

        #LDC
        elif op == 0x16:
            self.updateSigs(RegWr=True, ImmSel=1, WbSel=3)

        #LDO
        elif op == 0x017:
            self.updateSigs(RegWr=True, MemRd=True, WbSel=0)

        #STR
        elif op == 0x018:
            self.updateSigs(MemSel=1, ImmSel=1, MemWr=True)

        #STO
        elif op == 0x19:
            self.updateSigs(MemWr=True)

        #B
        elif op == 0x1A:
             self.updateSigs(BrSel=1)

        #BR
        elif op == 0x1B:
            self.updateSigs(BrSel=2)

        #CALL
        #Does nothing right now
        elif op == 0x1C:
            self.updateSigs(Call=True)

        #RET
        # Does nothing right now
        elif op == 0x1D:
            self.updateSigs(Ret=True)

        #PUSH, POP, INC, DEC
        elif op == 0x1E:
            if sel == 1:
                self.updateSigs(Push=True)
            elif sel == 2:
                self.updateSigs(Pop=True)
            elif sel == 4:
                self.updateSigs(ALUSrc=3, RegWr=True)
            elif sel == 8:
                self.updateSigs(ALUSrc=3, RegWr=True, ALUCntr=1)

        #SYSCALL
        elif op == 0x1F:
            self.updateSigs()
            raise ex.SyscallInterrupt