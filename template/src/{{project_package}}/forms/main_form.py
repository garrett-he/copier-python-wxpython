import wx

class MainForm(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, style=wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX, size=(300, 200))
