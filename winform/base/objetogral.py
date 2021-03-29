# -*- coding: utf-8 -*-

###########################################################
### Objeto Padre General V2.3                           ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 25/03/2021                                          ###
### Generacion de indice correcta                       ###
### Borrado correcto                                    ###
### Generacion de objeto tipo hijo                      ###
### opcion set focus                                    ###
### Se agrega metodo Delete para borrar correctamente   ###
### Se agrega metodo de actualizacion                   ###
### Correccion inicial de foco (sin foco)               ###
### Correcciones generales y type.                      ###
### Se agrega el update para actualizar cuando es llam. ###
###########################################################

"""OBJETO PADRE DE CONTROLES
"""

import pygame
from winform.base.labelint import LabelInt
from winform.base.funciones import AutoBrillo
from winform.form import Form   # para Type


class ObjetoGral(object):
    def __init__(self, form):
        # Propieades publicas comunes
        self.text = ''
        self.hijo = False              # Propiedad para establecer si pertenece a un objeto compuesto
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
        self.estado     = -1        # -1: recien creado 0: fuera 1: dentro 2: precionado
        self.id         = -1         # id del objeto
        self.prev_obj   = ''        # type: ObjetoGral   #puntero hacia el objeto previo
        self.next_obj   = ''        # type: ObjetoGral   # puntero hacia el proximo objeto
        # superficie Gral
        self.superficie = form.screen.superficie
        self.cuadros_total  =  form.screen.cuadros  # revisar si hay q usar
        self.actualizar_cuadro = False

    def __del__(self):
        print("OBJETO ELIMINADO ID: " + str(self.id) + " " + str(self.__class__.__name__) + " " + self.text + " Form: " + self.form.nombre)


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
        # obtener posicion real en base al formulario. X siempre es la posicion real
        if not self.hijo:
            self.x += self.form.posicion[0]
            self.y += self.form.posicion[1]
        self.ancho  = int(ancho * self.form.coef_tamano)
        self.alto   = int(alto  * self.form.coef_tamano)
        # posicion general
        self.rectangulo = self.x, self.y, self.ancho, self.alto
        self.rect_foco  = self.x-1, self.y-1, self.ancho+2, self.alto+2
        # Rectangulo de linea relativo
        self.line_rect = 0, 0, self.ancho, self.line_alto
        # agregamos el cuadro al total (revisar ya que tiene q dibujar cuando hay cambios)
        # self.cuadros_total.append(self.rectangulo)
        # agregamos el objeto al formulario (revisar en caso q no tenga foco)
        self.form.objetos.append(self)
        # agregar indices solo si es foqueable
        if foco:
            self.sin_foco = False
        else:
            self.sin_foco = True
        self.__agregar_indices__()

        print("OBJETO CREADO ID: " + str(self.id) + " " + str(self.__class__.__name__) + " " + str(self.text) + " Form: " + self.form.nombre)


    def __agregar_indices__(self):
        # buscamos id libre
        indice_libre = -1
        for indice in range(len(self.form.objetos)):
            ids = self.form.objetos[indice].id
            if indice != ids:
                indice_libre = indice
                break
        self.id   = indice_libre
        # agregamos los indices
        # Elemento NEXT
        # print("ID: " + str(self.id))
        if len(self.form.objetos) < 2:  # unico elemeto
            self.next_obj = self
            self.prev_obj = self
        else:                           # mas de 1 elemeto
            # siempre es el ultimo elemento, va a apuntar al primero
            self.next_obj = self.form.objetos[0]  # apuntamos al primero
            self.form.objetos[0].prev_obj = self
            # Elemento PREV
            if self.id == 0:                                    # solo si el id = 0
                self.prev_obj = self.form.objetos[-2]           # apuntamos al ultimo
                self.form.objetos[-1].next_obj = self
            else:
                self.prev_obj = self.form.objetos[self.id - 1]  # apuntamos al anterior
                self.form.objetos[self.id - 1].next_obj = self

    def delete(self):
        """ Permite eliminar el objeto, realiza desasociacion de los
            elementos para poder borrar el objeto
        """
        # Eliminar indice
        # print("ELIMINAR OBJETO ID: " + str(self.id) + " " + str(self.text) + " Form: " + str(self.form.nombre))
        # print("RECONECTAR OBJETO PREV ID: " + str(self.prev_obj.id) + " A NEXT " + str(self.next_obj.id))
        self.prev_obj.next_obj = self.next_obj
        # print("RECONECTAR OBJETO NEXT ID: " + str(self.next_obj.id) + " A PREV " + str(self.prev_obj.id))
        self.next_obj.prev_obj = self.prev_obj
        self.next_obj = None
        self.prev_obj = None
        # Eliminar label
        del self.label_int
        # Eliminar refencia en lista Form objetos
        # print("ELIMINAR REFERENCIA EN FORM OBJETOS: " + str(self.id))
        # self.form.objetos.remove(self)  # no usar sino no se puede sacar del form
        self.funcion = None
        self.cuadros_total = None
        # eliminar superficie
        self.superficie = None


    ########################################
    ### LLAMAR PARA ACTUALIZAR DIBUJADO  ###
    ########################################
    def actualizar(self):
        # Se utiliza el cuadro de foco para incluir el margen
        if self.cuadros_total.count(self.rect_foco) == 0:
            self.cuadros_total.append(self.rect_foco)

    ########################################
    ### METODOS COMUNES                  ###
    ########################################
    def set_hijo(self):
        # establece el objeto como hijo (se debe realizar antes del config)
        self.hijo = True

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

    def set_foco(self):
        self.evento_foco()

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
            print("FOCO ID: " + str(self.id) + " " + str(self.__class__.__name__) + " Form: " + str(self.form.nombre))
            self.foco = True
            # recuadro
            pygame.draw.rect(self.superficie, self.color_foco, self.rect_foco, 1)  # dibujamos
            self.actualizar()

    def evento_lost_foco(self):
        if not self.sin_foco:
            # print("LOST FOCO ID: " + str(self.id) + " " + str(self.__class__.__name__) + " Form: " + str(self.form.nombre))
            self.foco = False
            pygame.draw.rect(self.superficie, self.form.color, self.rect_foco, 1)  # dibujamos
            self.actualizar()

    ###################################
    ### METODOS PARA USUARIO        ###
    ###################################
    # define la funcion a ejecutar al hacer click
    def accion(self, funcion):
        # print("acion definida")
        self.funcion = funcion

    ###################################
    ### EVENTOS POR DEFECTO MOUSE   ###
    ###################################
    def evento_mouse_click_out(self):
        self.evento_lost_foco()

    def evento_mouse_click(self):
        self.evento_foco(False)
        self.funcion(self.id)

    def evento_mouse_scrollup(self):
        print("Scroll up")

    def evento_mouse_scrolldown(self):
        print("Scroll down")

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
