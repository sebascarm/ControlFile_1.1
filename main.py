""" MODULO PRINCIPAL MAIN()
"""

from componentes.logg     import Logg

from winform.screen import Screen
from winform.form   import Form
from forms.formmain import FormMain
from forms.eventos  import Eventos

RESOLUCION  = 900, 600
COLOR_FORM  = 5, 10, 20
POS_VENTANA = 0, 0

LOG = Logg()
LOG.definir()


SCREEN  = Screen("Control File v0.1", RESOLUCION, 1, 1.0)                # enviamos el tamano al inicio (2 veces??)
FORM    = Form(SCREEN, "Control", RESOLUCION, POS_VENTANA, COLOR_FORM)
OBJETOS = FormMain(FORM)
EVENTOS = Eventos(OBJETOS, LOG)

SCREEN.loop()
