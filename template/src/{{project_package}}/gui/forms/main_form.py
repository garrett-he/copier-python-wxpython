from .templates import MainFormTemplate
from ..res.images import app_icon


class MainForm(MainFormTemplate):
    def __init__(self, parent):
        super().__init__(parent)

        self.SetIcon(app_icon.GetIcon())
