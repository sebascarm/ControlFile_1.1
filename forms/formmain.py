from winform.label import Label
from winform.labelicon import LabelIcon
from winform.treeview import TreeView
from winform.button import Button
from winform.textbox import Textbox

class FormMain(object):
    def __init__(self, form):
        """Se Requiere el objeto Formulario
           @type form: Form
        """
        self.labelico       = LabelIcon(form)
        self.labelico2      = LabelIcon(form)
        self.labelico3      = LabelIcon(form)
        self.boton_nuevo    = Button(form)
        self.boton_test     = Button(form)
        self.tree_origen    = TreeView(form)
        self.tree_destino   = TreeView(form)

        # self.text = Textbox(form)
        # CONFIGURACION
        self.labelico.config("Entorno Inicial", 10, 10, 200, 18, "folder")
        self.labelico2.config("Secundario", 320, 10, 200, 14, "folder")
        self.labelico3.config("Terciario", 420, 10, 200, 14, "folder")
        self.labelico.set_textsize(18)
        self.boton_nuevo.config("Agregar folder", 10, 40, 100, 20)
        self.boton_test.config("Borrar folder", 120, 40, 100, 20)

        self.tree_origen.config("titulo", 10, 70, 500, 600)
        # self.tree_destino.config("titulo", 580, 70, 500, 600)



