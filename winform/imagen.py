# -*- coding: utf-8 -*-

###########################################################
### CLASE IMAGEN                                        ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 30/01/2020                                          ###
### Creacion                                            ###
###########################################################

import time
import pygame
import cv2
from winform.base.objetogral import ObjetoGral

class Imagen(ObjetoGral):
    def __init__(self, C_Form):
        super().__init__(C_Form)                # instanciamos la clase padre

    def config(self, x, y, ancho, alto):
        super().config(x, y, ancho, alto)

    def dibujar(self):
        pygame.draw.rect(self.superficie, self.color, self.rectangulo, 0)  # dibujamos
        
    
        #captura = cv2.VideoCapture(0, cv2.CAP_DSHOW) # si es windows
        #procesado, frame = captura.read()
        #captura.release()
        #time.sleep(1)
        #self.superficie.blit(self.cvimage_to_pygame(frame), (self.x,self.y))

    
    ###################################
    ### METODOS                     ###
    ###################################
    def imagen_cv(self, cv_imagen):
        """Dibuja una imagen en formato FRAME desde CV2 (camara)
        """
        self.superficie.blit(self.__cvimage_to_pygame(cv_imagen), (self.x,self.y))

    ###################################
    ### FUNCIONES INTERNAS          ###
    ###################################
    def __cvimage_to_pygame(self, cv_imagen):
        """Convierte una imagen CV a formato Pygame
        """
        cv_imagen = cv2.cvtColor(cv_imagen, cv2.COLOR_BGR2RGB)
        return pygame.image.frombuffer(cv_imagen.tostring(), cv_imagen.shape[1::-1],"RGB")
        
       