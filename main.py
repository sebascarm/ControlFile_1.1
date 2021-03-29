""" MODULO PRINCIPAL MAIN()
"""

from componentes.logg     import Logg

from winform.screen import Screen
from winform.form   import Form
from forms.formmain import FormMain
from forms.formfile import FormFile
from forms.eventos  import Eventos

RESOLUCION  = 1090, 800
COLOR_FORM  = 5, 10, 20
COLOR_FORM2  = 5, 40, 20
POS_VENTANA = 0, 0

LOG = Logg()
LOG.definir()


SCREEN    = Screen("Control File v0.1", RESOLUCION, 1, 1.0)                # enviamos el tamano al inicio (2 veces??)
FORM    = Form(SCREEN, "Control", RESOLUCION, POS_VENTANA, COLOR_FORM)
# FORM2     = Form(SCREEN, "form2", (320, 400), (50, 50), COLOR_FORM2)
OBJETOS = FormMain(FORM)
# OBJETOS2 = FormFile(FORM2)
EVENTOS = Eventos(OBJETOS, LOG)


SCREEN.loop()
