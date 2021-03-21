# -*- coding: utf-8 -*-

###########################################################
### CLASE PROGRESS 1.0                                  ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 05/10/2019                                          ###
###                                                     ###
###########################################################

import pygame
from winform.base.objetogral import ObjetoGral

class Progress(ObjetoGral):
    def __init__(self, C_Form):
        super().__init__(C_Form)    # instanciamos la clase padre
        self.min         = 0
        self.max         = 0
        self.ancho_barra = 0        # ancho de la barra de progreso
        self.rec_barra   = 0,0,0,0  # rectangulo de la barra
        
    def config(self, min, max, text, x, y, ancho, alto):
        # min, max (Valores minimos y maximos que se adoptan)
        # text (Valor inicial para mostrar)
        self.min = min
        self.max = max
        super().config(x, y, ancho, alto, str(text))
        self.label_int.config(self.text, self.color_text, 
                              self.rectangulo,
                              "centrada", "centrada", 
                              self.text_size)
        

    def dibujar(self):
        self.__rect_progress()
        pygame.draw.rect(self.superficie, self.color, self.rectangulo, 0)    # dibujamos
        pygame.draw.rect(self.superficie, self.color_b3, self.rec_barra, 0)  # dibujamos
        self.label_int.dibujar() 

    ###################################################
    ### Obtener el valor del rectangulo de la barra ###
    ###################################################
    def __rect_progress(self):
        proporcion       = (int(self.text)-self.min)/(self.max-self.min)
        self.ancho_barra = self.ancho * proporcion
        self.rec_barra   = self.x, self.y, self.ancho_barra, self.alto
        

