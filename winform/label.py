# -*- coding: utf-8 -*-

###########################################################
### CLASE LABEL V1.1                                    ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 08/02/2020                                          ###
### Redibujado del rectangulo para borrar fondo al      ###
### cambiar el texto                                    ###
###########################################################

import pygame
from winform.base.objetogral import ObjetoGral #Clase Padre

class Label(ObjetoGral):
    def __init__(self, C_Form):
        super().__init__(C_Form)                #instanciamos la clase padre
        
    def config(self, text, x, y, ancho, alto, alineacion="izquierda"):
        """Configuracion del objeto Requerido previo a toda acccion
           alinacion = izquierda , derecha, centrada
        """
        super().config(x, y, ancho, alto, text, True, False)
        self.label_int.config(self.text, self.color, self.rectangulo, alineacion, "centrada", self.text_size)

    #def set_textSize(self, size):
    #    self.label_int.set_textSize(size)
        
    def set_background(self, color):
        self.label_int.set_background(color)
    
    def dibujar(self):
        pygame.draw.rect(self.superficie, self.color_base, self.rectangulo, 0)  # borramos el fondo para que se borre el texto previo
        self.label_int.dibujar()   
        #agregamos el cuadro al total
        self.cuadros_total.append(self.rectangulo)


