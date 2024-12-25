import wx

from .gui.forms import MainForm


def main():
    app = wx.App(useBestVisual=True)

    form = MainForm(None)
    form.Show(True)
    form.Centre()

    app.MainLoop()


if __name__ == '__main__':
    main()
