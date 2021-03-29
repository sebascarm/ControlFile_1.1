from forms.formmain import FormMain
from forms.formfile import FormFile

from winform.form import Form

###########################################################
### Eventos principales                                 ###
###########################################################
class Eventos(object):
    def __init__(self, objetos, log):
        """Se Requiere los objetos y el log
           @type objetos: objetos
           @type log: log
        """
        self.objetos = objetos  # type: FormMain
        self.log     = log
        # Metodos
        self.objetos.boton_nuevo.accion(self.click_nuevo)
    ###########################################################
    ### METODOS (ACCIONES DE LOS BOTONES)                   ###
    ###########################################################
    def click_nuevo(self):
        screen    = self.objetos.boton_nuevo.form.screen
        tamano    = 320, 480
        posicion  = 340, 80
        color     = 5, 40, 20
        form_tree = Form(screen, "Seleccionar Folder", tamano, posicion, color)
        objetos   = FormFile(form_tree)
        eventos   = EventosTree(form_tree, objetos, self.log)


###########################################################
### Eventos Selector                                    ###
###########################################################
class EventosTree(object):
    def __init__(self, form, objetos, log):
        self.form    = form
        self.objetos = objetos  # type: FormFile
        self.log     = log
        # Metodos
        self.objetos.tree.accion(self.cargar_ruta)
        self.objetos.boton_aceptar.accion(self.click_aceptar)
        self.objetos.boton_cancelar.accion(self.click_cancelar)

    def cargar_ruta(self, ids, ruta):
        self.objetos.text.set_text(ruta)

    def click_aceptar(self):
        self.form.delete()

    def click_cancelar(self):
        self.form.delete()

    def __del__(self):
        print("CONST EVENTOS ELIMINADO " + str(self.__class__.__name__))
