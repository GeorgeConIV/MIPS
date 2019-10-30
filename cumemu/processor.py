import components as comp

class Processor:

    def __init__(self):
        self.instr_dec = comp.InstructionDecoder()
        self.reg_file = comp.RegisterFile()
        self.alu = comp.ALU()
        self.mem = comp.Memory()