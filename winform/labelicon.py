# -*- coding: utf-8 -*-

###########################################################
### CLASE LABELICON V1.1                                ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 23/03/2021                                          ###
### Admite 2 iconos                                     ###
### Creacion                                            ###
###########################################################

import pygame
from winform.base.objetogral import ObjetoGral
from winform.icons import iconos


class LabelIcon(ObjetoGral):
    def __init__(self, form):
        super().__init__(form)      # instanciamos la clase padre
        # propiedades internas
        self.rect_tx    = 0, 0, 0, 0
        self.icon       = "folder"
        self.icon2      = ''
        self.color_back = ''

    def config(self, text, x, y, ancho, alto, icon='folder', icon2='', color_back=''):
        """ :param icon:  "folder", "drive", "file"
            :param icon2: "flecha_derecha", "flecha_abajo", "circulo"
        """
        super().config(x, y, ancho, alto, text, True, False)
        self.icon  = icon
        self.icon2 = icon2
        self.color_back = color_back
        if icon2:
            desp = (self.alto * 2.5) + 4
            self.rect_tx   = self.x + desp, self.y, (self.ancho - desp), self.alto
        else:
            desp = (self.alto * 1.5) + 4
            self.rect_tx = self.x + desp, self.y, (self.ancho - desp), self.alto
        self.label_int.superficie = self.superficie
        self.label_int.config(self.text, self.color_text,
                              self.rect_tx,
                              "izquierda", "abajo",
                              self.text_size)

    def dibujar(self):
        self.__dibujar__()

    def __dibujar__(self):
        # borramos
        if self.color_back:
            pygame.draw.rect(self.superficie, self.color_back, (self.x, self.y, self.ancho, self.alto))
        x_ico = self.x
        if self.icon2:
            y = self.y + (self.alto / 4)
            alto = self.alto / 2
            if self.icon2 == "flecha_derecha":
                iconos.flecha_right_icon(self.superficie, self.x, y, alto, alto, self.color)
            elif self.icon2 == "flecha_abajo":
                iconos.flecha_down_icon(self.superficie, self.x, y, alto, alto, self.color)
            elif self.icon2 == "circulo":
                iconos.circle_icon(self.superficie, self.x, y, alto, alto, self.color)
            # cambiamos el X para el icono proximo
            x_ico = self.x + self.alto + 2

        if self.icon:
            if self.icon == "folder":
                ancho = self.alto * 1.4
                iconos.folder_icon(self.superficie, x_ico, self.y, ancho, self.alto, self.color)
            elif self.icon == "drive":
                ancho = self.alto * 1.5
                iconos.drive_icon(self.superficie, x_ico, self.y, ancho, self.alto, self.color)
            elif self.icon == "file":
                x_ico += self.alto  * 0.5
                ancho  = self.alto  * 0.9

                iconos.file_icon(self.superficie, x_ico, self.y, ancho, self.alto, self.color)
        self.label_int.superficie = self.superficie
        self.label_int.dibujar()


