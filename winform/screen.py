# -*- coding: utf-8 -*-

###########################################################
### CLASE SCREEN  V1.4                                  ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 25/03/2021                                          ###
### Dibuja solo elementos actualizados y limpia         ###
### Dibuja objetos directamente                         ###
### Llama al metodo dibujar directamente                ###
### Correccion al faltar icono                          ###
###########################################################

import time
import pygame

from winform.base.eventos import eventos

import random   # eliminar

class Screen:
    """Pantalla pricipal
       Solo puede existir una sola pantalla
       Contenedor de las distintas ventanas
       y las ventanas son las que contienen los objetos
    """
    def __init__(self, Nombre, Resolucion=(720, 1280), Resize=False, Coef_Tamano=1, Celular=False):
        """Instancia de creación
           En general los parametros son opcionales
        """
        pygame.init()
        #datos publicos
        self.nombre         = Nombre
        self.resolucion     = Resolucion
        self.coef_tamano    = Coef_Tamano  # porcentaje de tamano de 0 a 1
        self.superficie     = ""
        self.cuadros        = []    # lista  de elementos, tupla es con ()
        self.formularios    = []
        self.resize         = Resize
        self.celular        = Celular

        #datos de uso privado
        ancho, alto           = self.resolucion
        self.ancho_resolucion = int(ancho * self.coef_tamano)
        self.alto_resolucion  = int(alto * self.coef_tamano)
        pygame.key.set_repeat(300, 50)
        # llamamos al metodo dibujar directamente
        self.dibujar()

    def dibujar(self):
        """ Metodo de dibujo, debe ejecutarse previo
            a crear cualquier formulario
        """
        pygame.display.set_caption(self.nombre)
        try:
            icono = pygame.image.load('icono.png')
            pygame.display.set_icon(icono)
        except:
            print("No se pudo cargar el icono")
            pass
        if self.resize:
            self.superficie = pygame.display.set_mode((
                self.ancho_resolucion, self.alto_resolucion), pygame.RESIZABLE)
        else:
            self.superficie = pygame.display.set_mode((self.ancho_resolucion, self.alto_resolucion))

    def transicion(self): 
        for y in range(self.alto_resolucion, -40, -40):
            alto = self.alto_resolucion - y
            cuadro = (0, y, self.ancho_resolucion, alto)
            pygame.display.update(cuadro)
            if not self.celular:
                time.sleep(0.015)

    def transicion_inversa(self, Ventana): #para menu
        for alto in range(0, Ventana.alto_resolucion + 40, 40):
            cuadro = (0, 0, self.ancho_resolucion, alto)
            pygame.display.update(cuadro)
            if not self.celular:
                time.sleep(0.015)

    def update(self):
        # para tests de elementos que se dibujan
        # color = (random.randrange(255), random.randrange(255), random.randrange(255))
        # for cuadro in self.cuadros:
        #    pygame.draw.rect(self.superficie, color, cuadro, 1)
        # for formu in self.formularios:
        #    for objeto in formu.objetos:
        #        pygame.draw.rect(self.superficie, color, objeto.rectangulo, 1)

        # fin de tests
        pygame.display.update(self.cuadros)
        # vaciamos la lista (se debera crear sobre cada elemento que necesite actualizar)
        self.cuadros.clear()

    def dibuja_elementos(self):
        # recorrer formularios
        for formu in self.formularios:
            print("recorrer formu")
            formu.dibujar()
            # recorrer objetos
            for objeto in formu.objetos:
                objeto.dibujar()

    def loop(self):
        # dibujar elementos
        self.dibuja_elementos()
        self.update()
        loope = True
        while loope:
            # eventos devuleve falso cuando hay que salir del programa
            loope = eventos(self)
            if loope:
                self.update()
            time.sleep(0.01)
