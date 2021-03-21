# -*- coding: utf-8 -*-

###########################################################
### CLASE DRAWBOX (Para dibujar en pantalla)            ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 15/01/2021                                          ###
### Creacion                                            ###
###########################################################

import pygame
import time
from winform.base.objetogral import ObjetoGral

from winform.base.funciones import posLineRadio
from winform.base.funciones import sumar_angulo

from componentes.thread_admin import ThreadAdmin

from winform.base.funciones import color_a_color

class DrawBox(ObjetoGral):
    def __init__(self, C_Form):
        super().__init__(C_Form)                # instanciamos la clase padre
        # superficie interna - fondo y 4 capas
        self.superficie_fondo = ''  # type: pygame.Surface
        self.superficie_capa1 = ''  # type: pygame.Surface
        self.superficie_capa2 = ''  # type: pygame.Surface
        self.superficie_capa3 = ''  # type: pygame.Surface
        self.superficie_capa4 = ''  # type: pygame.Surface
        self.superficie_capa5 = ''  # type: pygame.Surface
        self.list_puntos      = []
        self.th_punto         = ThreadAdmin()
        self.area = 0, 0, 0, 0

    def config(self, x, y, ancho, alto):
        super().config(x, y, ancho, alto)
        # posicion sobre superficie
        self.area = 0, 0, self.ancho, self.alto
        # crear la superficie interna fondo
        self.superficie_fondo = pygame.Surface((self.ancho, self.alto))

    def dibujar(self):
        """Dibuja fisicamente el objeto en la superficie interna
            y en la sup general, posteriormente se requiere update de la sup
        """
        self.superficie_fondo.fill(self.color)
        # Dibujar la superficie interna en la general
        self.superficie.blit(self.superficie_fondo, (self.x, self.y), self.area)

        # pygame.draw.rect(self.superficie, self.color, self.rectangulo, 0)  # dibujamos

    def __obt_capa__(self, capa_num):
        if capa_num == 0:
            return self.superficie_fondo
        elif capa_num == 1:
            return self.superficie_capa1
        elif capa_num == 2:
            return self.superficie_capa2
        elif capa_num == 3:
            return self.superficie_capa3
        elif capa_num == 4:
            return self.superficie_capa4
        elif capa_num == 5:
            return self.superficie_capa5
    ###################################
    ### METODOS                     ###
    ###################################
    def nueva_capa(self, capa_num):
        # crear la superficie interna fondo
        capa = pygame.Surface((self.ancho, self.alto))
        capa.fill(self.color)
        capa.set_colorkey(self.color)    # capa con mascara oculta
        if   capa_num == 1:
            self.superficie_capa1 = capa
        elif capa_num == 2:
            self.superficie_capa2 = capa
        elif capa_num == 3:
            self.superficie_capa3 = capa
        elif capa_num == 4:
            self.superficie_capa4 = capa
        elif capa_num == 5:
            self.superficie_capa5 = capa

    def limpiar_capa(self, capa_num):
        if   capa_num == 0:
            self.superficie_fondo.fill(self.color)
        elif capa_num == 1:
            self.superficie_capa1.fill(self.color)
        elif capa_num == 2:
            self.superficie_capa2.fill(self.color)
        elif capa_num == 3:
            self.superficie_capa3.fill(self.color)
        elif capa_num == 4:
            self.superficie_capa4.fill(self.color)
        elif capa_num == 5:
            self.superficie_capa5.fill(self.color)

    def draw_punto(self, x, y, tamano, color, capa_num=0):
        capa = self.__obt_capa__(capa_num)
        pygame.draw.circle(capa, color, (int(x), int(y)), tamano)

    def draw_punto_temporal(self, x, y,  tamano, color, tiempo, capa_num=0):
        tiempo_act = 0
        color_act  = color
        parametros = int(x), int(y),  tamano, color, color_act, tiempo, tiempo_act, capa_num
        self.list_puntos.append(parametros)
        if not self.th_punto.state:
            self.th_punto.start(self.__hilo_punto__, '', "PUNTOS")


    def __hilo_punto__(self):
        indice = 0
        lista = self.list_puntos.copy()
        self.list_puntos.clear()
        lista_tmp = []
        while len(lista) > 0:
            lista_tmp.clear()
            lista.sort(reverse=True, key=self.__funcion_sort__)
            for punto in lista:
                x, y, tamano, color, color_act, tiempo, tiempo_act, capa_num = punto
                tiempo_act += 1
                color_act = color_a_color(color_act, color, self.color, tiempo * 10)
                self.draw_punto(x, y, tamano, color_act, capa_num)
                punto = x, y, tamano, color, color_act, tiempo, tiempo_act, capa_num
                if tiempo_act < tiempo * 10:
                    lista_tmp.append(punto)
                else:
                    self.draw_punto(x, y, tamano, self.color, capa_num)
            time.sleep(0.1)
            self.list_puntos.extend(lista_tmp)
            lista = self.list_puntos.copy()
            self.list_puntos.clear()


    def __funcion_sort__(self, punto):
        x, y, tamano, color, color_act, tiempo, tiempo_act, capa_num = punto
        r, g, b = color_act
        return r + g + b


    def draw_punto_distante(self, x, y, angulo, distancia, color, tamano, capa_num=0):
        x1, y1 = posLineRadio(x, y, angulo, distancia)
        capa = self.__obt_capa__(capa_num)
        pygame.draw.circle(capa, color, (int(x1), int(y1)), tamano)

    def draw_linea(self, x1, y1, ancho, alto, color, ancho_linea=1, capa_num=0):
        x2 = x1 + ancho
        y2 = y1 + alto
        capa = self.__obt_capa__(capa_num)
        pygame.draw.line(capa, color, (x1, y1), (x2, y2), ancho_linea)

    def draw_linea_angular(self, x, y, angulo, longitud, color, ancho=1, capa_num=0):
        x2, y2 = posLineRadio(x, y, angulo, longitud)
        capa = self.__obt_capa__(capa_num)
        pygame.draw.line(capa, color, (x, y), (x2, y2), ancho)

    def draw_flecha(self, x, y, angulo, longitud, color, ancho=1, capa_num=0):
        x2, y2 = posLineRadio(x, y, angulo, longitud)
        angulo_flecha1 = sumar_angulo(angulo, 200)
        angulo_flecha2 = sumar_angulo(angulo, 160)
        self.draw_linea_angular(x, y, angulo, longitud, color, ancho, capa_num)
        self.draw_linea_angular(x2, y2, angulo_flecha1, (longitud/2), color, ancho, capa_num)
        self.draw_linea_angular(x2, y2, angulo_flecha2, (longitud/2), color, ancho, capa_num)

    def arco(self, x, y, angulo, longitud, arco, color, ancho=1):
        pass
        #pygame.draw.arc(self.superficie, color, rect,  )


    def pintar(self):
        """Actualizar el dibujo, llamar luego de terminar dibujo
        """
        self.superficie.blit(self.superficie_fondo, (self.x, self.y), self.area)
        if self.superficie_capa1:
            self.superficie.blit(self.superficie_capa1, (self.x, self.y), self.area)
        if self.superficie_capa2:
            self.superficie.blit(self.superficie_capa2, (self.x, self.y), self.area)
        if self.superficie_capa3:
            self.superficie.blit(self.superficie_capa3, (self.x, self.y), self.area)
        if self.superficie_capa4:
            self.superficie.blit(self.superficie_capa4, (self.x, self.y), self.area)
        if self.superficie_capa5:
            self.superficie.blit(self.superficie_capa5, (self.x, self.y), self.area)
        self.actualizar()


