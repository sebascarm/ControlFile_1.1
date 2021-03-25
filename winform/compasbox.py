# -*- coding: utf-8 -*-

###########################################################
### CLASE COMPASBOX V1.1                                ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 11/03/2021                                          ###
### Actualizar control                                  ###
###########################################################

import pygame
from pygame import gfxdraw
from winform.base.funciones import posLineRadio
from winform.base.objetogral import ObjetoGral


class Compasbox(ObjetoGral):
    def __init__(self, C_Form):
        super().__init__(C_Form)                #instanciamos la clase padre
        # Propiedades internas
        self.rect_tx      = 0, 0, 0, 0
        self.rect_comp    = 0, 0, 0, 0  # rectangulo del compas
        self.comp_centro  = 0, 0        # centro del compas
        #superficie interna
        self.superficie_comp   = '' 
        self.superficie_flecha = ''

    def config(self, text, x, y, ancho, alto):
        super().config(x, y, ancho, alto, text)
        self.rect_tx = self.x, (self.y + self.alto - self.line_alto), self.ancho, self.line_alto
        self.label_int.config(self.text, self.color_text,
                              self.rect_tx,
                              "centrada", "centrada",
                              self.text_size)
        self.label_int.set_background(self.color_b2)
        if self.ancho > (self.alto - self.line_alto):
            self.rect_comp   = self.x + int((self.ancho-(self.alto-self.line_alto))/2), self.y, (self.alto - self.line_alto),(self.alto - self.line_alto)
        else:
            self.rect_comp = self.x, self.y + int(((self.alto-self.line_alto)-self.ancho)/2), self.ancho, self.ancho
        self.comp_centro = int(self.rect_comp[2]/2), int((self.rect_comp[3])/2)
        # crear la superficie interna
        self.superficie_comp   = pygame.Surface((self.rect_comp[2],self.rect_comp[3]))
        self.superficie_flecha = pygame.Surface((self.rect_comp[2],self.rect_comp[3]), pygame.SRCALPHA, 32) # surface transparente )
        # asignar graficos a la superficie
        self.__crear_sup_comp()
        self.__crear_sup_flecha()

    def dibujar(self):
        # rectangulo
        pygame.draw.rect(self.superficie, self.color, self.rectangulo, 0)
        # texto
        self.label_int.dibujar()
        # Dibujar la superficie interna en la Gral
        self.superficie.blit(self.superficie_comp,   (self.rect_comp[0],self.rect_comp[1]))
        self.superficie.blit(self.superficie_flecha, (self.rect_comp[0],self.rect_comp[1]))

    def rotar(self, grados):
        # texto
        self.label_int.set_text(str(grados))
        self.label_int.dibujar()
        # grafico
        superficie_rot = pygame.transform.rotate(self.superficie_flecha, -grados)
        rect = superficie_rot.get_rect()
        rect.center = self.comp_centro
        # Dibujar la superficie interna en la Gral
        self.superficie.blit(self.superficie_comp,   (self.rect_comp[0],self.rect_comp[1]))
        self.superficie.blit(superficie_rot, (self.rect_comp[0]+ rect[0],self.rect_comp[1]+rect[1]))
        self.actualizar()


    def __crear_sup_comp(self):
        #pygame.draw.rect(self.superficie, (150,150,150), self.rect_tx, 0)
        #pygame.draw.rect(self.superficie, (155,155,155), self.rect_comp, 0)
        self.superficie_comp.fill(self.color)  # Borra y rellena la zona
        #Circulo global
        radio = int(self.rect_comp[2]/2)-5
        pygame.gfxdraw.aacircle(self.superficie_comp,self.comp_centro[0],self.comp_centro[1], radio, self.color_text)
        #Marcas a 0, 90, 180 y 270 Grados
        start_pos = self.comp_centro[0],  1
        end_pos   = self.comp_centro[0],  9
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
        start_pos = self.comp_centro[0], self.rect_comp[3] - 1
        end_pos   = self.comp_centro[0], self.rect_comp[3] - 9
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
        start_pos = 1, self.comp_centro[1]
        end_pos   = 9, self.comp_centro[1]
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
        start_pos = self.rect_comp[2] - 1, self.comp_centro[1]
        end_pos   = self.rect_comp[2] - 9, self.comp_centro[1]
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
        start_pos = self.rect_comp[2] - 1, self.comp_centro[1]
        end_pos   = self.rect_comp[2] - 9, self.comp_centro[1]
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
        #Marcas a 45 Grados
        pos = posLineRadio(self.comp_centro[0],self.comp_centro[1],45, radio+4, radio-4)
        start_pos = pos[0], pos[1]
        end_pos   = pos[2], pos[3]
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
        pos = posLineRadio(self.comp_centro[0],self.comp_centro[1],135, radio+4,radio-4)
        start_pos = pos[0], pos[1]
        end_pos   = pos[2], pos[3]
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
        pos = posLineRadio(self.comp_centro[0],self.comp_centro[1],225, radio+4,radio-4)
        start_pos = pos[0], pos[1]
        end_pos   = pos[2], pos[3]
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
        pos = posLineRadio(self.comp_centro[0],self.comp_centro[1],315, radio+4,radio-4)
        start_pos = pos[0], pos[1]
        end_pos   = pos[2], pos[3]
        pygame.draw.line(self.superficie_comp, self.color_text, start_pos, end_pos, 1)
         # Circulo central
        pygame.gfxdraw.aacircle(self.superficie_comp,self.comp_centro[0],self.comp_centro[1], 4, self.color_text)
        pygame.gfxdraw.filled_circle(self.superficie_comp,self.comp_centro[0],self.comp_centro[1], 4, self.color_text)

    def __crear_sup_flecha(self):
        # Flecha
        start_pos = self.comp_centro[0], self.comp_centro[1]
        end_pos   = self.comp_centro[0], 5
        pygame.draw.line(self.superficie_flecha, self.color_text, start_pos, end_pos, 1)
        # Punta de flecha
        start_pos = self.comp_centro[0], 5
        end_pos   = self.comp_centro[0]-2, 12
        pygame.draw.aaline(self.superficie_flecha, self.color_text, start_pos, end_pos)
        end_pos   = self.comp_centro[0]+2, 12
        pygame.draw.aaline(self.superficie_flecha, self.color_text, start_pos, end_pos)
