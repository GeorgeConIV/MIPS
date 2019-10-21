import re

from instruction import Instruction
from globals import label_map, ErrorPrint

instr_switch = {
    **dict.fromkeys(["add","sub","mul","div","tar","mov","cmp","and","or","xor","bic","ldo","sto"], CreateRType),
    **dict.fromkeys(["addi","subi","muli","divi","andi","ori","xori"], CreateIType),
    **dict.fromkeys(["lda","ldc","str","call"], CreateJType),
    **dict.fromkeys(["lsl","lsr","asr"], CreateSType),
    **dict.fromkeys(["not","br","push","pop","inc","dec"], CreateNType),
    **dict.fromkeys(["nop","ret","syscall"], CreateUType),
    "ldc"   :   CreateCType,
    "b"     :   CreateBType
}

class AssemblerError(Exception):
    def __init__(self, msg):
        self.msg = msg

label = r"\s*(\w+(?=:))"
instr = r"\s*(\w+)"
def InstructionGen(filename):
    f = open(filename, "r")
    pc = 0
    line_num = 0
    with open(filename, "r") as f:
        for line in f:
            try:
                line = line.split(';')[0]   # remove comment
                if line == "":              # if just a comment, go to next line
                    continue
                m = re.match(label, line)   # check if there's a label  
                if m is not None:
                    label_map[m.group(0)] = pc   # update label table
                    line = line.split(':')[1]       # remove label from string
                m = re.match(instr, line)   # find instr
                if m is not None:
                    yield instr_switch[m.group(0).lower()](pc, line, line_num) # function table that returns an instruction object
                line_num += 1
                pc += 2
            except AssemblerError as ae:
                ErrorPrint(line_num, line, ae.msg)
                exit()
            except:
                ErrorPrint(line_num, line, "Error: Invalid opcode on this line")
                exit()

r_type = r"\s*(\w+)(\.\w+)?\s+(\w{2}),\s+(\w{2})"
def CreateRType(pc, line, line_num):
    m = re.match(r_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match r-type (Rs, Rt)")
    cond_code = m.group(1)
    if cond_code is not None:
        cond_code = cond_code[1:]
    return Instruction(
        line, line_num, "r", pc,
        opcode  =   m.group(0),
        cond    =   cond_code,
        rs      =   m.group(2),
        rt      =   m.group(3)
    )

i_type = r"\s*(\w+)(\.\w+)?\s+(\w{2}),\s+(\d+)"
def CreateIType(pc, line, line_num):
    m = re.match(j_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match i-type (Rs, Imm)")
    if m.group(1) is not None:
        ErrorPrint(line_num, line, "Warning: i-type instructions are not conditional")
    im = int(m.group(3))
    if im < -63 or 127 < im:
        raise AssemblerError("Error: Immediate is too large (range [-63, 127])")
    return Instruction(
        line, line_num, "i", pc,
        opcode  =   m.group(0),
        rs      =   m.group(2),
        imm     =   im
    )

j_type = r"\s*(\w+)(\.\w+)?\s+(\w{2}),\s+(\w+)"
def CreateJType(pc, line, line_num):
    m = re.match(j_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match j-type (Rs, Label)")
    if m.group(1) is not None:
        ErrorPrint(line_num, line, "Warning: j-type instructions are not conditional")
    return Instruction(
        line, line_num, "j", pc,
        opcode  =   m.group(0),
        rs      =   m.group(2),
        label   =   m.group(3)
    )

s_type = r"\s*(\w+)(\.\w+)?\s+(\w{2}),\s+(\d+)"
def CreateSType(pc, line, line_num):
    m = re.match(s_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match s-type (Rs, Imm)")
    if m.group(1) is not None:
        ErrorPrint(line_num, line, "Warning: s-type instructions are not conditional")
    im = int(m.group(3))
    if im < 0 or 31 < im:
        raise AssemblerError("Error: Immediate is too large (range [0, 31])")
    return Instruction(
        line, line_num, "s", pc,
        opcode  =   m.group(0),
        rs      =   m.group(2),
        imm     =   im
    )

n_type = r"\s*(\w+)(\.\w+)?\s+(\w{2}(?!,))"
def CreateNType(pc, line, line_num):
    m = re.match(n_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match n-type (Rs)")
    cond_code = m.group(1)
    if cond_code is not None:
        cond_code = cond_code[1:]
    return Instruction(
        line, line_num, "n", pc,
        opcode  =   m.group(0),
        cond    =   cond_code,
        rs      =   m.group(2)
    )

u_type = r"\s*(\w+)(\.\w+)?"
def CreateUType(pc, line, line_num):
    m = re.match(u_type, line)
    if m is None:
        raise AssemblerError("Error on u-type... which shouldn't happen?!?")
    if m.group(1) is not None:
        ErrorPrint(line_num, line, "Warning: u-type instructions are not conditional")
    return Instruction(
        line, line_num, "u", pc,
        opcode  =   m.group(0)
    )

d_type = r"\s*DB\s*(\d+)"
def CreateDType(pc, line, line_num):
    m = re.match(d_type, line)
    if m is None:
        raise AssemblerError("Error: DB not formatted correctly (db imm)")
    im = int(m.group(0))
    if im < -32767 or 65535 < im:
        raise AssemblerError("Error: Value is too large (range [-32767, 65535])")
    return Instruction(
        line, line_num, "d", pc,
        imm  =   m.group(0)
    )

c_type = r"\s*(\w+)(\.\w+)?\s+(\d+(?!,))"
def CreateCType(pc, line, line_num):
    m = re.match(c_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match c-type (Imm)")
    im = int(m.group(2))
    if im < -1023 or 2047 < im:
        raise AssemblerError("Error: Immediate is too large (range [-1023, 2047])")
    return Instruction(
        line, line_num, "c", pc,
        opcode  =   m.group(0),
        cond    =   m.group(1),
        imm     =   im
    )

b_type = r"\s*(\w+)(\.\w+)?\s+(\w+(?!,))"
def CreateBType(pc, line, line_num):
    m = re.match(b_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match b-type (Label)")
    cond_code = m.group(1)
    if cond_code is not None:
        cond_code = cond_code[1:]
    return Instruction(
        line, line_num, "b", pc,
        opcode  =   m.group(0),
        cond    =   cond_code,
        label   =   m.group(2)
    )