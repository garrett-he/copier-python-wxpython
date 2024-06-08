import wx

from .forms.main_form import MainForm


class App(wx.App):
    main_form: MainForm

    def __init__(self):
        super().__init__(useBestVisual=True)

        self.main_form = MainForm(None)

    def run(self):
        self.main_form.Show(True)
        self.main_form.Centre()

        self.MainLoop()
