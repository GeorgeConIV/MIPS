import wx
import os
import cumemu.processor as proc

class frame(wx.Frame):

    def __init__(self, parent, title):
        super(frame, self).__init__(parent, title=title, size=(1000, 1000))
        self.process = proc.Processor()
        self.UpdateRegs()
        self.InitUI()

    def UpdateRegs(self):
        self.regs = self.process.reg_file.registers
        self.regnames = ["R0 :", "R1 :", "R2 :", "R3 :", "R4 :", "R5 :", "R6 :", "R7 :", "R8 :", "R9 :", "R10:", "R11:",
                         "PC :", "RA :", "SP :", "AR :"]
        self.strings = ["REGISTERS:"]
        for x in range(len(self.regs)):
            string = self.regnames[x] + self.regs[x].__str__()
            #print(string)
            self.strings.append(string)

    def InitUI(self):
        toolbar = self.CreateToolBar()
        runtool = toolbar.AddTool(wx.ID_ANY, 'Step forward', wx.Bitmap('step.png'))
        qtool = toolbar.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap('exit.png'))
        opentool = toolbar.AddTool(wx.ID_ANY, 'Open file', wx.Bitmap('open.png'))
        toolbar.Realize()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)
        otherbox = wx.BoxSizer(wx.VERTICAL)

        self.my_text = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(200, 900))
        lst = wx.ListBox(panel, size = (80, 900), choices = self.strings, style = wx.LB_SINGLE)

        box.Add(lst, 0, wx.EXPAND)

        otherbox.Add(self.my_text, 1, wx.ALL|wx.EXPAND)

        box.Add(otherbox)

        panel.SetSizer(box)
        panel.Fit()

        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)
        self.Bind(wx.EVT_TOOL, self.OnStep, runtool)
        self.Bind(wx.EVT_TOOL, self.onOpen, opentool)

        self.SetSize((1000, 1000))
        self.SetTitle('MIPS GUI thing')
        self.Centre()

    def OnQuit(self, e):
        self.Close()

    def OnStep(self, e):
        self.process.run()
        self.UpdateRegs()
        print("Step once")

    def onOpen(self, event):
        wildcard = "TXT files (*.txt)|*.txt"
        dialog = wx.FileDialog(self, "Open Text Files", wildcard=wildcard,
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return

        path = dialog.GetPath()

        if os.path.exists(path):
            with open(path) as fobj:
                for line in fobj:
                    self.my_text.WriteText(line)

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


