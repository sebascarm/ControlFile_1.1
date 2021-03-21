# -*- coding: utf-8 -*-

###########################################################
### CLASE LABEL INTERNO V1.2                            ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 19/03/2021                                          ###
### Correccion en alineacion vertical                   ###
### Correccion de alineacion en SetText                 ###
###########################################################

import pygame


class LabelInt(object):
    def __init__(self, form):
        self.form       = form
        self.superficie = form.screen.superficie
        self.background = False     # posee background color
        self.tamano     = 11        # tamaño inicial del texto
        self.texto      = ''
        self.rectangulo = ''
        self.x          = 0
        self.y          = 0     
        self.ancho      = 0 
        self.alto       = 0
        self.color      = ''
        self.fuente     = ''
        self.fuente_py  = ''
        
    def config(self, texto, color, rectangulo, alin_horizontal="centrada",
               alin_vertical="centrada", tamano=11, margen = 0,
               fuente="DejaVuSans.ttf"):
        self.texto  = texto
        self.tamano = tamano
        self.rectangulo = rectangulo
        self.x, self.y, self.ancho, self.alto = self.rectangulo
        self.color      = color
        self.fuente     = fuente
        self.fuente_py  = pygame.font.Font(self.fuente, self.tamano)
        self.label      = self.fuente_py.render(texto, True, self.color)
        self.text_ancho, self.text_alto = self.label.get_size()
        self.margen     = margen
        self.alin_horizontal = alin_horizontal
        self.alin_vertical   = alin_vertical
        self.__config_xy()
        self.__control_longitud()

    def __config_xy(self):
        # obtener posicion acordself.e a la alin_horizontal-------------
        if   self.alin_horizontal == "centrada":
            text_x_pos = self.x + ((self.ancho - self.text_ancho) / 2)
        elif self.alin_horizontal == "izquierda":
            # se incluye margen si existe
            text_x_pos = self.x + self.margen
        elif self.alin_horizontal == "derecha":
            text_x_pos = (self.x + self.ancho) - self.text_ancho
        # obtener posicion acorde a la alin_vertical---------------------
        if   self.alin_vertical == "centrada":
            text_y_pos = self.y + ((self.alto - self.text_alto) / 2)
        elif self.alin_vertical == "arriba":
            text_y_pos = self.y
        elif self.alin_vertical == "abajo":
            text_y_pos = (self.y + self.alto) - (self.text_alto * 0.8)
        # aplicamos la posicion
        self.x_y = text_x_pos, text_y_pos
                
    def __control_longitud(self):
        # revisar q no exceda el tamano
        while self.text_ancho + self.margen > self.ancho:
                self.texto = self.texto[: -1] #recorta una letra
                self.label = self.fuente_py.render(self.texto, True, self.color)
                self.text_ancho, self.text_alto = self.label.get_size()
    
    def set_textsize(self, size):
        # Cabiar el tamaño del texto
        self.tamano = size
        self.fuente_py  = pygame.font.Font(self.fuente, self.tamano)
        self.label      = self.fuente_py.render(self.texto, True, self.color)
        self.text_ancho, self.text_alto = self.label.get_size()
        self.__config_xy()
        self.__control_longitud()
    
    def set_background(self, color):
        self.background = True
        self.background_color = color
        
    def set_text(self, texto):
        self.texto = texto
        self.label = self.fuente_py.render(self.texto, True, self.color)
        self.text_ancho, self.text_alto = self.label.get_size()
        if self.alin_horizontal != "izquierda":
            # Si el texto esta centrado o a la derecha hay que reposicionar
            self.__config_xy()
        # revisar q no exceda el tamano
        self.__control_longitud()
    
    def set_pos(self, rectangulo):
        """Cambiar la posicion donde se dibujara el texto
           Se pasa un cuadro (x,y,ancho, alto) como parametro 
        """
        self.rectangulo = rectangulo
        self.x, self.y, self.ancho, self.alto = self.rectangulo
        self.__config_xy()
        
    def dibujar(self, superficie=''):
        """Dibuja fisicamente el texto en la superficie dada
           si no se especifica superfice se dibuja en la 
           superficie de Pantalla
        """
        # dibujar background si es necesario
        if self.background:
            if superficie == '':
                pygame.draw.rect(self.superficie, self.background_color, self.rectangulo, 0)
            else:
                pygame.draw.rect(superficie, self.background_color, self.rectangulo, 0)
        # dibujar directo
        if superficie == '':
            self.superficie.blit(self.label, self.x_y)
        else:
            superficie.blit(self.label, self.x_y)
            
            