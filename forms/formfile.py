
from winform.label import Label
from winform.textbox  import Textbox
from winform.treeview import TreeView
from winform.textbox import Textbox
from winform.button import Button



class FormFile(object):
    def __init__(self, form):
        self.text           = Textbox(form)
        self.tree           = TreeView(form)
        self.boton_aceptar  = Button(form)
        self.boton_cancelar = Button(form)
        # CONFIGURACION
        self.text.config("", 10, 10, 300, 20)
        self.tree.config("titulo", 10, 40, 300, 400)
        self.boton_aceptar.config("Aceptar", 140, 450, 80, 20)
        self.boton_cancelar.config("Cancelar", 230, 450, 80, 20)

        self.text.set_foco()

    def __del__(self):
        print("CONST FORMULARIO ELIMINADO " + str(self.__class__.__name__))
