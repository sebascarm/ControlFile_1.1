# -*- coding: utf-8 -*-

###########################################################
### CLASE LOGBOX V1.1                                   ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 25/03/2021                                          ###
### Este encabezado                                     ###
###########################################################

import pygame
from winform.base.objetogral import ObjetoGral


class Logbox(ObjetoGral):
    def __init__(self, C_Form):
        super().__init__(C_Form)                #instanciamos la clase padre
        #Propiedades publicas
        self.list_text = []
        #propiedades internas
        self.line_actual      = 0
        self.line_pos_visible = 0           # posicion visible de la linea actual
        self.lines_buffer     = 100         # cantidad de lineas actuales de la superficie interna
        self.lines_buffer_max = 100         # cantidad maxima de lineas por buffer
        self.lines_visibles   = 0
        self.buffer_max       = 10          # cantidade de superficies que se pueden crear
        self.buffer_actual    = 1
        #superficie interna
        self.superficie_alto = 0
        self.superficie_int  = ''
        self.area            = 0,0,0,0
    
    def config(self, text, x, y, ancho, alto):
        """Configuración del objeto
           Requerido previo a toda acccion
        """
        super().config(x, y, ancho, alto, text)
        #agregamos el texto a la lista
        self.list_text.append(text)
        #cantidad de lineas visbles
        self.lines_visibles = int(self.alto / self.line_alto)
        #posicion sobre superficie
        self.area = 0,0, self.ancho, self.alto
        #crear la superficie interna
        self.superficie_alto = self.line_alto * self.lines_buffer
        self.superficie_int  = pygame.Surface((self.ancho, self.superficie_alto)) 
        #crea el label
        self.label_int.config(self.text, self.color_text, 
                              self.line_rect,"izquierda", "centrada", 
                              self.text_size, 4)
        
    def dibujar(self):
        """Dibuja fisicamente el objeto en la superficie interna
           y en la sup general, posteriormente se requiere update de la sup
        """
        self.superficie_int.fill(self.color)
        self.label_int.dibujar(self.superficie_int)
        #Dibujar la superficie interna en la general
        self.superficie.blit(self.superficie_int, (self.x, self.y),self.area)   

    ###################################
    ### METODOS                     ###
    ###################################
    def set_textSize(self, size):
        super().set_textsize(size)
        #modificar cantidad de lineas visbles
        self.lines_visibles = int(self.alto / self.line_alto)
        #modificar la superficie interna
        self.superficie_alto = (self.line_alto * self.lines_buffer) #+ 9 #(Agregado)
        self.superficie_int  = pygame.Surface((self.ancho, self.superficie_alto)) 
        

    def insert(self, text):
        self.text = text
        self.list_text.append(text)
        self.__incrementar_line()
        self.__dibujar(self.text)
        

    ###################################
    ### FUNCIONES INTERNAS          ###
    ###################################

    def __incrementar_line(self):
        """ Cambia la posicion de linea, rectangulo de linea y del label
            relativo a una superficie o posicion interna
        """
        self.line_actual += 1
        self.line_pos_visible += 1
        # revisar si nos pasamos del area visible
        if self.line_pos_visible > (self.lines_visibles-1):
            #revisar si nos quedamos sin buffer
            if self.line_pos_visible > (self.lines_buffer-1):
                #revisar si pasamos el maximo de buffer
                if (self.buffer_actual+1) > self.buffer_max:
                    tmp_alto = self.superficie_alto * self.buffer_actual
                    tmp_surface = pygame.Surface((self.ancho, tmp_alto))
                    tmp_surface.fill(self.color)
                    #pygame.image.save(tmp_surface, "tmp_surface.jpg") #Imagen save test
                    tmp_pos_y = self.superficie_alto
                    tmp_alto  = tmp_alto - self.superficie_alto
                    #cargamos la superficie actual a la superficie temporal
                    tmp_surface.blit(self.superficie_int, (0,0), (0, tmp_pos_y , self.ancho , tmp_alto)) 
                    self.superficie_int = tmp_surface.copy()        #rearmamos la superficie interna
                    self.__limpiar_buffer(self.lines_buffer_max)    #limpiar el buffer
                else:
                    self.buffer_actual += 1
                    self.lines_buffer += self.lines_buffer_max
                    tmp_surface = pygame.Surface((self.ancho, self.superficie_alto * self.buffer_actual))
                    tmp_surface.fill(self.color)  # rellenamos el espacio vacio con el fondo para no tener partes negras al copiar (agregado)
                    tmp_surface.blit(self.superficie_int, (0, 0))
                    self.superficie_int = tmp_surface.copy()
            #desplazar la superficie
            self.__desp_area(1)
        #cambiar pos de label
        self.__cambiar_line_rect(self.line_pos_visible)

    def __limpiar_buffer(self, lines):
        """ limpia la cantidad de lineas especificadas
            del buffer
        """
        self.__desp_area(-lines)      #desplaza el area
        for x in range(0, lines):     #elimina de la lista
            self.list_text.pop(0)     #siempre borra el primero
        self.line_actual -= lines     #actualiza la linea actual
        self.line_pos_visible -= lines

    def __desp_area(self, lines):
        """ Desplaza la posicion visible y actualiza la linea visible
        """
        desp  = lines * self.line_alto
        pos_y = self.area[1] + desp
        self.area = 0, pos_y, self.ancho, self.alto

    def __cambiar_line_rect(self, line):
        """ Cambiar la posicion del rectangulo de linea
        """
        self.line_rect = (0, line * self.line_alto, self.ancho, self.line_alto)
        self.label_int.set_pos(self.line_rect)

    def __dibujar(self, text):
        """Dibujo interno
        solo se dibuja la linea actual
        """
        pygame.draw.rect(self.superficie_int, self.color, self.line_rect, 0)
        self.label_int.set_text(text)
        self.label_int.dibujar(self.superficie_int)
        #Dibujar la superficie interna en la general
        self.superficie.blit(self.superficie_int, (self.x, self.y),self.area)
        