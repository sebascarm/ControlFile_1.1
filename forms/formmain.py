from winform.label import Label
from winform.labelicon import LabelIcon
from winform.treeview import TreeView
from winform.textbox import Textbox

class FormMain(object):
    def __init__(self, form):
        """Se Requiere el objeto Formulario
           @type form: Form
        """
        self.icon         = LabelIcon(form)
        self.tree         = TreeView(form)

        # self.text = Textbox(form)
        # CONFIGURACION
        self.icon.config("Entorno Inicial", 10, 10, 200, 18, "folder")
        self.icon.set_textsize(18)
        self.tree.config("titulo",10,40,300,500)

        # self.text.config("", 200, 20,100,20)