# -*- coding: utf-8 -*-

###########################################################
### CLASE FORM   V1.1                                   ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 05/02/2020                                          ###
### Se carga en el objeto screen en configuracion       ###
### (Para que se pueda dibujar directamente)            ###
###########################################################


import pygame

class Form(object):
    """Ventana
       Son las distintas pantallas (ventanas) del programa
       pertenecen a la Pantalla pricipal
       es el contenedor de los distintos objetos
    """
    def __init__(self, C_Screen, Nombre, Tamano, Posicion, Color =(255,255,255)):

        #datos publicos
        self.nombre     = Nombre
        self.tipo       = "ventana"
        self.tamano     = Tamano
        self.posicion   = Posicion
        self.color      = Color
        self.coef_tamano= C_Screen.coef_tamano
        self.margen     = 10
        self.ventana    = ""
        self.objetos    = [ ]   #lista vacia
        self.enable     = True

        self.cuadro      = (0,0,0,0)
        #datos de uso privado
        self.screen           = C_Screen
        self.superficie       = C_Screen.superficie
        self.coef_tamano      = C_Screen.coef_tamano
        ancho, alto           = self.tamano
        self.ancho_resolucion = int(ancho * self.coef_tamano)
        self.alto_resolucion  = int(alto  * self.coef_tamano)
        self.tamano_real      = self.ancho_resolucion, self.alto_resolucion
        #cargamos el objeto al screen
        self.screen.formularios.append(self)

    def dibujar(self):
        #detalles del cuadro
        x, y        = self.posicion
        ancho, alto = self.tamano_real
        cuadro      = (x, y, ancho, alto)
        #si la ventana es el mismo tamano que la pantalla dibuja sobre la pantalla directamente
        if (self.tamano == self.screen.resolucion):
            self.superficie.fill(self.color)
        else:
            #si es distinto dibuja un cuadro
            pygame.draw.rect(self.superficie, self.color, cuadro)
        #cargamos datos del cuadro
        self.cuadro = cuadro
        self.screen.cuadros.append(self.cuadro)
        #cargamos el objeto al screen
        #self.screen.formularios.append(self)
