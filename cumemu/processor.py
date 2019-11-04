import cumemu.components as comp

from cumemu.int16 import Int16

class Processor:
    def __init__(self):
        self.decoder = comp.InstructionDecoder()
        self.reg_file = comp.RegisterFile()
        self.alu = comp.ALU()
        self.mem = comp.Memory()
        self.ctrl = comp.ControlUnit()

    def call(self):
        sp = self.reg_file.read(14).actual
        ra = self.reg_file.read(13).actual
        self.mem.write(sp, ra)
        self.reg_file.write(14, sp - 2)

        new_ra = self.reg_file.read(12).actual + 2
        self.reg_file.write(13, new_ra)

    def ret(self):
        sp = self.reg_file.read(14).actual
        ra = self.reg_file.read(13).actual
        new_ra = self.mem.read(sp)
        self.reg_file.write(14, sp + 2)

        self.reg_file.write(12, ra)     # pc
        self.reg_file.write(13, new_ra)

    def run(self):
        pc = self.reg_file.read(12).actual
        self.instr = self.mem.read(pc).bytes()
        self.decoder.decode(self.instr[0], self.instr[1])
        self.ctrl.update(self.decoder.op, self.decoder.cond, self.decoder.rt)

        rs_out = self.reg_file.read(self.decoder.rs)
        rt_out = self.reg_file.read(self.decoder.rt)
        imm = [self.decoder.imm, self.decoder.l_imm][self.ctrl.ImmSel]

        alu_b = [rt_out, imm, self.decoder.rt, Int16(1)][self.ctrl.ALUSrc]
        self.alu.update(rs_out, alu_b, self.ctrl.ALUCntr)
        alu_out = self.alu.out
        self.ctrl.updateFlags(alu_out.z, alu_out.n, alu_out.c, alu_out.v)

        sp = self.reg_file.read(14)
        mem_addr = [alu_out, self.decoder.l_imm, sp][self.ctrl.MemSel]
        mem_out = 0
        if self.ctrl.MemRd:
            mem_out = self.mem.read(mem_addr.actual)
        elif self.ctrl.MemWr:
            self.mem.write(mem_addr.actual, self.reg_file.read(15))

        if self.ctrl.RegWr:
            writeback = [mem_out, alu_out, rt_out, imm][self.ctrl.WbSel]
            reg_dst = [15, self.decoder.rs][self.ctrl.RegDst]
            self.reg_file.write(reg_dst, writeback)
        
        if self.ctrl.Push:
            self.reg_file.read(14).set(sp + Int16(-2))
        elif self.ctrl.Pop:
            self.reg_file.read(14).set(sp + Int16(2))
        elif self.ctrl.Call:
            self.call()
        elif self.ctrl.Ret:
            self.ret()
            return

        pc = Int16(pc + 2)
        b_addr = [self.decoder.l_imm, self.decoder.b_address][self.ctrl.BAdd] * Int16(2)
        next_pc = [pc, pc + b_addr, rs_out][self.ctrl.BrSel]
        self.reg_file.write(12, next_pc)

        
