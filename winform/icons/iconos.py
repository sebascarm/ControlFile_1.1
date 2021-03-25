###########################################################
### FUNCIONES ICONOS V1.0                               ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 23/03/2021                                          ###
### Creacion                                            ###
###########################################################

import pygame
from pygame import gfxdraw


def folder_icon(superficie, x, y, ancho, alto, color):
    # coordenadas
    alto -=1
    alto_ico = alto / 4
    ancho_ico = ancho / 1.5
    y1 = y + alto_ico
    x2 = x + ancho_ico - alto_ico
    x4 = x + ancho_ico
    y6 = y + alto
    puntos = [(x, y), (x2, y), (x4, y1), (x + ancho, y1),
              (x + ancho, y6), (x, y6)]
    # dibugar poligonos
    pygame.draw.polygon(superficie, color, puntos)


def drive_icon(superficie, x, y, ancho, alto, color):
    alto -= 1
    alto_ico = (alto/2.5)
    y1 = y + alto_ico
    x2 = x + alto_ico
    x3 = (x + ancho) - alto_ico
    x4 = x + ancho - 1  # raro el -1 pero funciona en iconos chicos
    y5 = y + alto
    # dibugar poligonos base
    puntos = [(x, y1), (x2, y), (x3, y), (x4, y1), (x4, y5), (x, y5)]
    pygame.draw.polygon(superficie, color, puntos)
    # dibugar poligonos cuadro interno
    rect   = x+1, y1+1, ancho-2, alto - (alto/2.5)-1
    pygame.draw.rect(superficie, (0, 0, 0), rect, 0)
    # dibugar poligonos luz
    pos_ini = x+(ancho*3/4), y+(alto*3/4)
    pos_fin = x+(ancho-4), y+(alto*3/4)

    pygame.draw.line(superficie, (0,100,0), pos_ini, pos_fin, 2)


def file_icon(superficie, x, y, ancho, alto, color):
    x1 = x+(alto/4)
    x2 = x+ancho
    y3 = y+alto
    y5 = y + (alto / 4)
    # dibugar poligonos base
    puntos = [(x1, y), (x2, y), (x2, y3), (x, y3), (x, y5)]
    pygame.draw.polygon(superficie, color, puntos)
    # dibugar poligonos de dobles
    pygame.draw.line(superficie, (0, 0, 0), (x, y5), (x1, y5), 1)
    pygame.draw.line(superficie, (0, 0, 0), (x1, y), (x1, y5), 1)


def flecha_right_icon(superficie, x, y, ancho, alto, color):
    # dibugar poligonos
    pygame.draw.line(superficie, color, (x, y), (x+ancho, y+(ancho/2)), 2)
    pygame.draw.line(superficie, color, (x+ancho, y+ancho/2), (x, y+ancho), 2)


def flecha_down_icon(superficie, x, y, ancho, alto, color):
    # dibugar poligonos
    pygame.draw.line(superficie, color, (x, y), (x+(ancho/2), y + alto), 2)
    pygame.draw.line(superficie, color, (x+(ancho/2), y+alto), (x+ancho, y), 2)


def circle_icon(superficie, x, y, ancho, alto, color):
    # dibugar poligonos
    pygame.gfxdraw.aacircle(superficie, int(x+(ancho/2)), int(y+(alto/2)), int(alto/2), color)

