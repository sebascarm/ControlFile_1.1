import pygame

from winform.base.objetogral import ObjetoGral
from winform.base.funciones import Brillo


class Checkbox(ObjetoGral):
    def __init__(self, C_Form):
        super().__init__(C_Form)                # instanciamos la clase padre
        # Propieades internas
        self.enable     = False                 # estado del casillero
        self.rect_tx    = 0,0,0,0
        self.rect_ch    = 0,0,0,0               # rectangulo del checkbox
        self.rect_int   = 0,0,0,0               # rectangulo interno del checkbox

    def config(self, text, x, y, ancho, alto, enable=False):
        super().config(x, y, ancho, alto, text)
        self.enable = enable
        self.rect_tx = self.x, self.y, int(self.ancho-self.alto-(4*self.form.coef_tamano)) , self.alto
        self.rect_ch = int(self.x + self.ancho - self.alto), self.y, self.alto, self.alto
        self.rect_foco = self.rect_ch[0]-1 ,self.rect_ch[1]-1, self.rect_ch[2]+2, self.rect_ch[3]+2
        unidad = int(3 * self.form.coef_tamano)
        self.rect_int= self.rect_ch[0]+unidad, self.rect_ch[1]+unidad,self.rect_ch[2]-(2*unidad), self.rect_ch[3]-(2*unidad)
        self.label_int.config(self.text, self.color, 
                              self.rect_tx,
                              "derecha", "centrada", 
                              self.text_size)

    def dibujar(self):
        pygame.draw.rect(self.superficie, self.color, self.rect_ch, 0)  # dibujamos
        self.label_int.dibujar()                                         # texto


    
    ###################################
    ### EVENTOS                     ###
    ###################################

    def evento_mouse_click(self):
        super().evento_mouse_click()
        #print("FOCO ID: " + str(self.id) + " " + str(self.__class__.__name__))
        if self.enable:
            #dibujamos vacio
            pygame.draw.rect(self.superficie, self.color, self.rect_ch, 0)  # dibujamos
            self.enable = False
            self.funcion(False) # Funcion evento
        else:
            pygame.draw.rect(self.superficie, self.color_base, self.rect_int, 0)  # dibujamos
            self.enable = True
            self.funcion(True)  # Funcion evento
        self.actualizar()
        
    ###################################
    ### EVENTOS DE TECLADO          ###
    ###################################

    def evento_key(self, cod_caracter, caracter):
        super().evento_key(cod_caracter, caracter)
        if cod_caracter == 32: # SPACE
            self.evento_mouse_click()

    
    
