import wx
import os

from cumasm.instruction import Instruction
from cumemu.emulator import Emulator
from cumemu.int16 import Int16

class MemWindow(wx.Frame):
    def __init__(self, title, em, parent=None):
        super(MemWindow, self).__init__(parent, title=title, size=(500, 500))
        self.parent = parent

        self.address_list = [Int16(0) for _ in range(512)]
        self.mem_list = [Int16(0) for _ in range(513)]
        self.mem_list[0] = 'ADDRESS    VALUES'

        self.em = em

        for x in range(len(self.em.processor.mem.memspace)):
            self.mem_list[x+1] = str(Int16(2*x)) + ':  ' + str(Int16(self.em.processor.mem.memspace[x]))

        self.initUI()
        self.Show()

    def updateMem(self):
        for x in range(len(self.em.processor.mem.memspace)):
            self.mem_list[x+1] = str(Int16(2*x)) + ':  ' + str(Int16(self.em.processor.mem.memspace[x]))
        self.lst.Set(self.mem_list)

    def initUI(self):
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)

        self.lst = wx.ListBox(panel, size=(300, 900), choices=self.mem_list, style=wx.LB_SINGLE)

        box.Add(self.lst, 0, wx.EXPAND)

        panel.SetSizer(box)
        panel.Fit()

        self.SetSize((500, 500))
        self.SetTitle('Memory Panel')
        self.Centre()


class frame(wx.Frame):

    def __init__(self, parent, title):
        super(frame, self).__init__(parent, title=title, size=(500, 500))
        self.process = None
        self.strings = ["REGISTERS:", "R0 :", "R1 :", "R2 :", "R3 :", "R4 :", "R5 :", "R6 :", "R7 :", "R8 :", "R9 :", "R10:", "R11:",
                         "PC :", "RA :", "SP :", "AR :"]
        self.InitUI()
        self.currentop = 0
        self.opstr = ""
        self.newFrame = None

    def UpdateRegs(self):
        self.regs = self.process.processor.reg_file.registers
        self.regnames = ["R0 :", "R1 :", "R2 :", "R3 :", "R4 :", "R5 :", "R6 :", "R7 :", "R8 :", "R9 :", "R10:", "R11:",
                         "PC :", "RA :", "SP :", "AR :"]
        self.strings = ["REGISTERS:"]
        for x in range(len(self.regs)):
            string = self.regnames[x] + str(self.regs[x])
            #print(string)
            self.strings.append(string)
        
        if self.process.processor.instr:
            opnames = ["nop", "add", "addi", "sub", "subi", "mul", "muli", "div",
                "divi", "shift", "li", "mov", "cmp", "and", "andi", "or", "ori",
                "xor", "xori", "not", "bic", "lda", "ldc", "ldo", "str", "sto",
                "b", "br", "call", "ret", "single-op", "syscall"]
            self.opstr = opnames[(self.process.processor.instr[0] & 0xF8) >> 3]

            self.currentop = Int16(int.from_bytes(self.process.processor.instr, "big"))
        else:
            self.opstr = '\t'
        #print(self.currentop.__str__())
        # print(key_list[val_list.index(value)])

    def SetStrings(self):
        self.UpdateRegs()
        self.lst.Set(self.strings)
        self.my_text.SetLabel("Current opcode: " + self.opstr
                              + "              Current instr: " + str(self.currentop))
        if self.newFrame != None:
            self.newFrame.updateMem()

    def InitUI(self):
        toolbar = self.CreateToolBar()
        runtool = toolbar.AddTool(wx.ID_ANY, 'Step forward', wx.Bitmap('resources\\step.png'))
        qtool = toolbar.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap('resources\\exit.png'))
        opentool = toolbar.AddTool(wx.ID_ANY, 'Open file', wx.Bitmap('resources\\open.png'))
        memtool = toolbar.AddTool(wx.ID_ANY, 'mem viewer', wx.Bitmap('resources\\mem.png'))
        toolbar.Realize()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        otherbox = wx.BoxSizer(wx.VERTICAL)

        self.my_text = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(200, 900))
        self.lst = wx.ListBox(panel, size = (80, 900), choices = self.strings, style = wx.LB_SINGLE)

        box.Add(self.lst, 0, wx.EXPAND)

        otherbox.Add(self.my_text, 1, wx.ALL|wx.EXPAND)

        box.Add(otherbox)

        panel.SetSizer(box)
        panel.Fit()

        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)
        self.Bind(wx.EVT_TOOL, self.OnStep, runtool)
        self.Bind(wx.EVT_TOOL, self.onOpen, opentool)
        self.Bind(wx.EVT_TOOL, self.onMem, memtool)

        self.SetSize((500, 500))
        self.SetTitle('Computation Utility Machine EMUlator')
        self.Centre()

    def onMem(self, e):
        if self.process is None:
            msg = wx.MessageDialog(self, "No executable has been loaded", style=wx.OK)
            msg.ShowModal()
            return
        self.newFrame = MemWindow('mem win', self.process)

    def OnQuit(self, e):
        self.Close()

    def OnStep(self, e):
        if self.process is None:
            msg = wx.MessageDialog(self, "No executable has been loaded", style=wx.OK)
            msg.ShowModal()
            return

        error = self.process.run()
        if error:
            msg = wx.MessageDialog(self, error, style=wx.OK)
            msg.ShowModal()

        self.SetStrings()

    def onOpen(self, event):
        wildcard = "Executables (*.cum)|*.cum"
        dialog = wx.FileDialog(self, "Open Executable", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            self.process = Emulator()
            self.process.setup(path)
            self.SetStrings()
        else:
            msg = wx.MessageDialog(self, "File does not exist!", style=wx.OK)
            msg.ShowModal()
        
        

def main():
    app = wx.App()
    ex = frame(None, title='Sizing')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()


class MyPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)


