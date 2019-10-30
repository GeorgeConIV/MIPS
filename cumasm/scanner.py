import re

from cumasm.instruction import Instruction
from cumasm.globals import label_map, ErrorPrint


r_type = r"\s*(\w+)(\.\w+)?\s+(\w{2,3}),\s+(\w{2,3})"
def CreateRType(pc, line, line_num):
    m = re.match(r_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match r-type (Rs, Rt)")
    cond_code = m.group(2)
    if cond_code is not None:
        cond_code = cond_code[1:]
    return Instruction(
        line, line_num, "r", pc,
        opcode  =   m.group(1),
        cond    =   cond_code,
        rs      =   m.group(3),
        rt      =   m.group(4)
    )

i_type = r"\s*(\w+)(\.\w+)?\s+(\w{2,3}),\s+(\d+)"
def CreateIType(pc, line, line_num):
    m = re.match(i_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match i-type (Rs, Imm)")
    if m.group(2) is not None:
        ErrorPrint(line_num, line, "Warning: i-type instructions are not conditional")
    im = int(m.group(4))
    if im < -64 or 63 < im:
        raise AssemblerError("Error: Immediate is too large (range [-64, 63])")
    return Instruction(
        line, line_num, "i", pc,
        opcode  =   m.group(1),
        rs      =   m.group(3),
        imm     =   im
    )

j_type = r"\s*(\w+)(\.\w+)?\s+(\w+)"
def CreateJType(pc, line, line_num):
    m = re.match(j_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match j-type (Rs, Label)")
    if m.group(2) is not None:
        ErrorPrint(line_num, line, "Warning: j-type instructions are not conditional")
    return Instruction(
        line, line_num, "j", pc,
        opcode  =   m.group(1),
        label   =   m.group(3)
    )

s_type = r"\s*(\w+)(\.\w+)?\s+(\w{2,3}),\s+(\d+)"
def CreateSType(pc, line, line_num):
    m = re.match(s_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match s-type (Rs, Imm)")
    if m.group(2) is not None:
        ErrorPrint(line_num, line, "Warning: s-type instructions are not conditional")
    im = int(m.group(4))
    if im < 0 or 31 < im:
        raise AssemblerError("Error: Immediate is too large (range [0, 31])")
    return Instruction(
        line, line_num, "s", pc,
        opcode  =   m.group(1),
        rs      =   m.group(3),
        imm     =   im
    )

n_type = r"\s*(\w+)(\.\w+)?\s+(\w{2,3}(?!,))"
def CreateNType(pc, line, line_num):
    m = re.match(n_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match n-type (Rs)")
    cond_code = m.group(2)
    if cond_code is not None:
        cond_code = cond_code[1:]
    return Instruction(
        line, line_num, "n", pc,
        opcode  =   m.group(1),
        cond    =   cond_code,
        rs      =   m.group(3)
    )

u_type = r"\s*(\w+)(\.\w+)?"
def CreateUType(pc, line, line_num):
    m = re.match(u_type, line)
    if m is None:
        raise AssemblerError("Error on u-type... which shouldn't happen?!?")
    if m.group(2) is not None:
        ErrorPrint(line_num, line, "Warning: u-type instructions are not conditional")
    return Instruction(
        line, line_num, "u", pc,
        opcode  =   m.group(1)
    )

d_type = r"\s*\w{2}\s*(\d+(?!,))"
def CreateDType(pc, line, line_num):
    m = re.match(d_type, line)
    if m is None:
        raise AssemblerError("Error: DW not formatted correctly (dw imm)")
    im = int(m.group(1))
    if im < -32767 or 32766 < im:
        raise AssemblerError("Error: Value is too large (range [-32767, 32766])")
    return Instruction(
        line, line_num, "d", pc,
        imm  =   im
    )

c_type = r"\s*(\w+)(\.\w+)?\s+(\d+(?!,))"
def CreateCType(pc, line, line_num):
    m = re.match(c_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match c-type (Imm)")
    im = int(m.group(3))
    if im < -1024 or 1023 < im:
        raise AssemblerError("Error: Immediate is too large (range [-1024, 1023])")
    return Instruction(
        line, line_num, "c", pc,
        opcode  =   m.group(1),
        cond    =   m.group(2),
        imm     =   im
    )

b_type = r"\s*(\w+)(\.\w+)?\s+(\w+(?!,))"
def CreateBType(pc, line, line_num):
    m = re.match(b_type, line)
    if m is None:
        raise AssemblerError("Error: Operands do not match b-type (Label)")
    cond_code = m.group(2)
    if cond_code is not None:
        cond_code = cond_code[1:]
    return Instruction(
        line, line_num, "b", pc,
        opcode  =   m.group(1),
        cond    =   cond_code,
        label   =   m.group(3)
    )

instr_switch = {
    **dict.fromkeys(["add","sub","mul","div","tar","mov","cmp","and","or","xor","bic","ldo","sto"], CreateRType),
    **dict.fromkeys(["addi","subi","muli","divi","andi","ori","xori"], CreateIType),
    **dict.fromkeys(["lda","str","call"], CreateJType),
    **dict.fromkeys(["lsl","lsr","asr"], CreateSType),
    **dict.fromkeys(["not","br","push","pop","inc","dec"], CreateNType),
    **dict.fromkeys(["nop","ret","syscall"], CreateUType),
    "ldc"   :   CreateCType,
    "b"     :   CreateBType,
    "dw"    :   CreateDType
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
                    yield instr_switch[m.group(1).lower()](pc, line, line_num) # function table that returns an instruction object
                line_num += 1
                pc += 2
            except AssemblerError as ae:
                ErrorPrint(line_num, line, ae.msg)
                exit()
            except:
                ErrorPrint(line_num, line, "Error: Invalid opcode on this line")
                exit()
