# -*- coding: utf-8 -*-

###########################################################
### Objeto Padre General V2.1                           ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 19/03/2021                                          ###
### Correccion inicial de foco (sin foco)               ###
### Correcciones generales y type.                      ###
### Se agrega el update para actualizar cuando es llam. ###
###########################################################

"""OBJETO PADRE DE CONTROLES
"""

import pygame
# objetos internos
from winform.base.labelint import LabelInt
# funciones
from winform.base.funciones import AutoBrillo
# from winform.base.funciones import Esta_Adentro
from winform.form import Form   # para Type


class ObjetoGral(object):
    def __init__(self, form):
        # Propieades publicas comunes
        self.text = ''
        # Propiedades publicas de posicion
        self.x = 0
        self.y = 0
        self.ancho = 0
        self.alto  = 0
        self.rectangulo = 0, 0, 0, 0   # rectangulo general
        self.rect_foco  = 0, 0, 0, 0   # rectangulo del foco 1 pixel mas
        # propiedades de color
        self.altoContraste = True
        self.color         = (0, 0, 0)
        self.color_base    = (0, 0, 0)
        self.color_b2      = (0, 0, 0)
        self.color_b3      = (0, 0, 0)
        self.color_text    = (150, 150, 150)
        self.color_foco    = (120, 120, 220)
        # funcion al realizar click
        self.funcion = self.evento_funcion    # funcion que se activa con click (devulve el id en la funcion)
        # propiedades internas
        self.form = form  # type: Form
        self.label_int = LabelInt(self.form)
        self.text_size = int(self.label_int.tamano * form.coef_tamano)
        self.line_alto = int(self.text_size * 1.3)
        self.line_rect = 0, 0, 0, 0
        # comunes en objetos
        self.foco       = False     # estado actual de foco
        self.sin_foco   = False     # elemento que es foqueable o no
        self.estado     = 0         # 0 fuera 1 dentro 2 precionado
        self.id         = 0         # id del objeto
        self.prev_obj   = ''        # type: ObjetoGral   #puntero hacia el objeto previo
        self.next_obj   = ''        # type: ObjetoGral   # puntero hacia el proximo objeto
        # superficie Gral
        self.superficie = form.screen.superficie
        self.cuadros_total  =  form.screen.cuadros  # revisar si hay q usar
        self.actualizar_cuadro = False

    def __del__(self):
        print("OBJETO ELIMINADO ID: " + str(self.id) + " " + str(self.__class__.__name__))

    def config(self, x, y, ancho, alto, text='', alto_contraste=True, foco=True):
        """Configuracion del objeto
           Requerido previo a toda acccion
           altoContrasto: True para cuadros de texto, False para Botones
           foco: defincion si objeto va atener foco (label por ejemplo no lleva)
        """
        # asignacion de colores
        self.altoContraste = alto_contraste
        if self.altoContraste:
            self.color = AutoBrillo(self.form.color, 100)
        else:
            self.color = AutoBrillo(self.form.color, 30)
        self.color_b2 = AutoBrillo(self.color, 20)
        self.color_b3 = AutoBrillo(self.color, 40)
        self.color_base = self.form.color
        self.color_text = AutoBrillo(self.color, 120, True)
        self.color_foco = (120, 120, 220)
        # asignacion de texto
        self.text = text
        # parametros de posicion
        self.x = int(x * self.form.coef_tamano)
        self.y = int(y * self.form.coef_tamano)
        self.ancho  = int(ancho * self.form.coef_tamano)
        self.alto   = int(alto  * self.form.coef_tamano)
        # posicion general
        self.rectangulo = self.x, self.y, self.ancho, self.alto
        self.rect_foco  = self.x-1, self.y-1, self.ancho+2, self.alto+2
        # Rectangulo de linea relativo
        self.line_rect = 0, 0, self.ancho, self.line_alto
        # agregamos el cuadro al total (revisar ya que tiene q dibujar cuando hay cambios)
        self.cuadros_total.append(self.rectangulo)
        # agregamos el objeto al formulario (revisar en caso q no tenga foco)
        self.form.objetos.append(self)
        # agregar indices solo si es foqueable
        if foco:
            self.sin_foco = False
        else:
            self.sin_foco = True
        self.__agregar_indices__()
        print("OBJETO CREADO ID: " + str(self.id) + " " + str(self.__class__.__name__))


    def __agregar_indices__(self):
        # agregamos el ID
        elementos = len(self.form.objetos)
        self.id   = elementos - 1
        # agregamos los indices
        self.next_obj = self.form.objetos[0]    # al principio apuntamos el siguiente al primer objeto
        if elementos > 1:
            self.prev_obj = self.form.objetos[self.id - 1]  # prev apunta al objeto previo
            self.form.objetos[self.id - 1].next_obj = self  # next previo apunta a este objeto
            self.form.objetos[0].prev_obj = self            # prev del inicial apunta a este objeto

    ########################################
    ### LLAMAR PARA ACTUALIZAR DIBUJADO  ###
    ########################################
    def desactualizar(self):
        del self.cuadros_total[:]
    def actualizar(self):
        # agrega el rectangulo para que sea actualizado por el update del screen
        if self.cuadros_total.count(self.rectangulo) == 0:
            self.cuadros_total.append(self.rectangulo)

    ########################################
    ### METODOS COMUNES                  ###
    ########################################
    def set_text(self, text):
        self.text = text
        self.label_int.set_text(text)
        self.dibujar()
        self.actualizar()

    def set_textsize(self, size):
        self.text_size = int(size * self.form.coef_tamano)
        self.label_int.set_textsize(self.text_size)
        self.line_alto = int(self.text_size * 1.3)
        self.line_rect = 0, 0, self.ancho, self.line_alto

    def dibujar(self):
        # Metodo basico por defecto
        print("Falta metodo dibujar")

    ########################################
    ### FUNCION DE FOCO (DEBEN LLAMARSE) ###
    ########################################

    def evento_foco(self, sedefoco=True):
        if self.sin_foco:
            print("ID: " + str(self.id) + " Elemento sin Foco (saltar)")
            if sedefoco:
                self.next_obj.evento_foco()
        else:
            print("FOCO ID: " + str(self.id) + " " + str(self.__class__.__name__))
            self.foco = True
            # recuadro
            pygame.draw.rect(self.superficie, self.color_foco, self.rect_foco, 1)  # dibujamos
            self.actualizar()

    def evento_lost_foco(self):
        if not self.sin_foco:
            self.foco = False
            pygame.draw.rect(self.superficie, self.form.color, self.rect_foco, 1)  # dibujamos
            # print("Actualizar lf")
            # self.actualizar()

    ###################################
    ### METODOS PARA USUARIO        ###
    ###################################
    # define la funcion a ejecutar al hacer click
    def accion(self, funcion):
        print("acion definida")
        self.funcion = funcion

    ###################################
    ### EVENTOS POR DEFECTO MOUSE   ###
    ###################################
    def evento_mouse_click_out(self):
        self.evento_lost_foco()

    def evento_mouse_click(self):
        self.evento_foco(False)
        self.funcion(self.id)

    ###################################
    ### EVENTOS POR DEFECTO TECLADO ###
    ###################################
    def evento_key(self, cod_caracter, caracter):
        if cod_caracter == 13:  # ENTER
            print("ENTER")
        elif cod_caracter == 32:  # SPACE
            print("SPACE")
        elif cod_caracter == 9:  # TAB
            print("TAB")
            self.evento_lost_foco()
            # Pasar el foco al siguiente objeto
            self.next_obj.evento_foco()

    ###################################
    ### EVENTOS POR DEFECTO FUNCION ###
    ###################################
    def evento_funcion(self, objeto_id):
        print("OBJETO SIN ACCION ID: " + str(objeto_id) + " " + str(self.__class__.__name__))
