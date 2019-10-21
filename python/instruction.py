from globals import label_map, ErrorPrint

class Instruction:
    opcode_table = {
        "nop"   :   0x00,
        "add"   :   0x01,
        "addi"  :   0x02,
        "sub"   :   0x03,
        "subi"  :   0x04,
        "mul"   :   0x05,
        "muli"  :   0x06,
        "div"   :   0x07,
        "divi"  :   0x08,
        "lsl"   :   0x09,
        "lsr"   :   0x09,
        "asr"   :   0x09,
        "tar"   :   0x0A,
        "mov"   :   0x0B,
        "cmp"   :   0x0C,
        "and"   :   0x0D,
        "andi"  :   0x0E,
        "or"    :   0x0F,
        "ori"   :   0x10,
        "xor"   :   0x11,
        "xori"  :   0x12,
        "not"   :   0x13,
        "bic"   :   0x14,
        "lda"   :   0x15,
        "ldc"   :   0x16,
        "ldo"   :   0x17,
        "srt"   :   0x18,
        "sto"   :   0x19,
        "b"     :   0x1A,
        "br"    :   0x1B,
        "call"  :   0x1C,
        "ret"   :   0x1D,
        "pop"   :   0x1E,
        "push"  :   0x1E,
        "inc"   :   0x1E,
        "dec"   :   0x1E,
        "syscall":  0x1F
    }
    cond_table = {
        None    :   0,
        "eq"    :   1,
        "ne"    :   2,
        "lt"    :   3,
        "gt"    :   4,
        "lte"   :   5,
        "gte"   :   6,
        "eqz"   :   7
    }
    reg_table = {
        "r0"    :   0x0,
        "r1"    :   0x1,
        "r2"    :   0x2,
        "r3"    :   0x3,
        "r4"    :   0x4,
        "r5"    :   0x5,
        "r6"    :   0x6,
        "r7"    :   0x7,
        "r8"    :   0x8,
        "r9"    :   0x9,
        "r10"   :   0xA,
        "r11"   :   0xB,
        "pc"    :   0xC,
        "r12"   :   0xC,
        "ra"    :   0xD,
        "r13"   :   0xD,
        "sp"    :   0xE,
        "r14"   :   0xE,
        "ar"    :   0xF,
        "r15"   :   0xF
    }
    single_op_table = {
        "push"  :   1,
        "pop"   :   2,
        "inc"   :   4,
        "dec"   :   8
    }
    def __init__(self, line, line_num, typ, pc, opcode=None, rs=None, rt=None, imm=None, label=None, cond=None):
        self.line = line
        self.ln = line_num
        self.type = typ
        self.pc = pc
        self.opcode = opcode.lower()
        self.rs = rs.lower()
        self.rt = rt.lower()
        self.imm = imm
        self.label = label
        self.cond = cond.lower()

    def relative(self, label):
        try:
            address = label_map[label]
            return (address - self.pc + 2) >> 1
        except:
            ErrorPrint(self.ln, self.line, "Error: Label was not defined")
            exit()

    bit_jump_table = {
        'r' : rType,
        'i' : iType,
        'j' : jType,
        's' : sType,
        'n' : nType,
        'u' : uType,
        'c' : cType,
        'b' : bType
    }
    def binary(self):
        return self.bit_jump_table[self.type]

    def rType(self):
        op = self.opcode_table[self.opcode]
        rs = self.reg_table[self.rs]
        rt = self.reg_table[self.rt]
        cond = self.cond_table[self.cond]
        
        hi = op << 3 | (rs & 0b1110) >> 1
        lo = (rs & 1) << 7 | rt << 3 | cond
        return bytearray([hi,lo])

    def iType(self):
        op = self.opcode_table[self.opcode]
        rs = self.reg_table[self.rs]
        
        hi = op << 3 | (rs & 0b1110) >> 1
        lo = (rs & 1) << 7 | self.imm
        return bytearray([hi,lo])

    def jType(self):
        op = self.opcode_table[self.opcode]
        address = self.relative(self.label)

        hi = op << 3 | (address & 0x700) >> 8
        lo = address & 0xFF
        return bytearray([hi,lo])
        