###########################################################
### CLASE TEXTBOX 1.1                                   ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 11/03/2021                                          ###
### Actualiza elemeto                                   ###
###########################################################

import pygame
from winform.base.objetogral import ObjetoGral

class Textbox(ObjetoGral):
    def __init__(self, C_Form):
        super().__init__(C_Form)                #instanciamos la clase padre
        # internas
        self.cursor_pos = 0
       
    def config(self, text, x, y, ancho, alto):
        super().config(x, y, ancho, alto, text)
        # interno
        self.cursor_pos = len(self.text)
        self.label_int.config(self.text, self.color_text, 
                              self.rectangulo,"izquierda", "centrada", 
                              self.text_size ,4)

    def dibujar(self):
        pygame.draw.rect(self.superficie, self.color, self.rectangulo, 0)   # dibujamos
        self.label_int.dibujar()                                            #texto

    ###################################
    ### EVENTOS                     ###
    ###################################

    def evento_mouse_click(self):
        super().evento_mouse_click()
        self.__dibujar(self.text + "|")

    def evento_mouse_click_out(self):
        super().evento_mouse_click_out()
        # dibujamos
        self.__dibujar(self.text)

    ###################################
    ### EVENTOS TECLAS              ###
    ###################################

    def evento_key(self, cod_caracter, caracter):
        # print("TECLA: " + str(cod_caracter) + " ID: " + str(self.id))
        super().evento_key(cod_caracter, caracter)
        if cod_caracter == 8:       # BORRADO
            if self.cursor_pos > 0:
                texto_ini = self.text[:self.cursor_pos - 1]
            else:
                texto_ini = ""
            texto_fin = self.text[self.cursor_pos:]
            self.text = texto_ini + texto_fin
            self.__mover_cursor(-1)
            self.__dibujar(texto_ini + "|" + texto_fin)

        elif cod_caracter == 127:  # SUPRIMIR
            texto_ini = self.text[:self.cursor_pos]
            texto_fin = self.text[self.cursor_pos+1:]
            self.text = texto_ini + texto_fin
            self.__dibujar(texto_ini + "|" + texto_fin)

        elif cod_caracter == 13:    # ENTER
            pass
        
        elif cod_caracter == 9:     # TAB
            self.__dibujar(self.text)

        elif cod_caracter == 276:  # cursor izq
            self.__mover_cursor(-1)
            texto_ini = self.text[:self.cursor_pos]
            texto_fin = self.text[self.cursor_pos:]
            self.__dibujar(texto_ini + "|" + texto_fin)
        
        elif cod_caracter == 275:  # cursor der
            self.__mover_cursor(1)
            texto_ini = self.text[:self.cursor_pos]
            texto_fin = self.text[self.cursor_pos:]
            self.__dibujar(texto_ini + "|" + texto_fin)

        elif cod_caracter == 278:   # INICIO
            self.cursor_pos = 0
            self.__dibujar("|" + self.text)
        
        elif cod_caracter == 279:   # FIN
            self.cursor_pos = len(self.text)
            self.__dibujar(self.text + "|")

        else:
            # agregar texto
            texto_ini = self.text[:self.cursor_pos]
            texto_fin = self.text[self.cursor_pos:]
            self.text = texto_ini + caracter + texto_fin
            self.__mover_cursor(1)
            self.__dibujar(texto_ini + caracter + "|" + texto_fin)

    ###################################
    ### FUNCIONES INTERNAS          ###
    ###################################
    
    def __mover_cursor(self, valor):
        """mueve el cursor atras o adelante
          utlizanto ej: 1 o -1"""
        self.cursor_pos = self.cursor_pos + valor
        if self.cursor_pos < 0: 
            self.cursor_pos = 0
        elif self.cursor_pos > len(self.text):
            self.cursor_pos = len(self.text)

    def __dibujar(self, texto):
        """Dibujo interno"""
        pygame.draw.rect(self.superficie, self.color, self.rectangulo, 0)
        self.label_int.set_text(texto)
        self.label_int.dibujar()
        self.actualizar()
