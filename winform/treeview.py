# -*- coding: utf-8 -*-

###########################################################
### CLASE Tree View                                    ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 19/03/2021                                          ###
### Creacion                                            ###
###########################################################
import string
from ctypes import windll
import os
import time
import pygame
from winform.base.objetogral import ObjetoGral
from winform.icons.iconos import folder_icon
from winform.textbox import Textbox
from winform.labelicon import LabelIcon
from winform.icons import iconos

class TreeView(ObjetoGral):
    def __init__(self, form):
        super().__init__(form)      # instanciamos la clase padre
        # propiedades internas
        self.folder     = ""
        self.drives     = []    # lista de unidades
        self.folders    = []    # lista de directorios visibles
        self.files      = []    # lista de archivos visibles
        self.iconos     = []    # lista de objetos iconos
        self.labelicon  = []    # lista de objeto labelicon
        self.fila       = 0
        self.columna    = 0
        self.superficie_int = ''    # type: pygame.Surface # modificamos la surface para usar una propia

    def config(self, text, x, y, ancho, alto, folder=''):
        super().config(x, y, ancho, alto, text, False)
        self.folder = folder

        self.textbox = Textbox(self.form)
        self.textbox.config("", x+4, y+4, ancho-8, 20)
        self.superficie_int = pygame.Surface((self.ancho, self.alto))


    def dibujar(self):
        pygame.draw.rect(self.superficie_int, self.color, (0,0,self.ancho, self.alto), 0)  # dibujamos
        self.__dibujar_unidades__()
        self.__dibujar__()

    def __dibujar_unidades__(self):
        self.fila = 0
        self.columna = 0
        self.drives = self.get_drives()
        for drive in self.drives:
            self.columna = 0
            self.__dibujar_label_icon__(self.fila, self.columna, "drive", "circulo", drive)
            self.fila += 1

    def funcion_accion(self, id_control):
        fila, label  = self.__obtener_fila__(id_control)
        path = label.text + "/"
        print(path)
        self.folders = self.get_folders(path)
        self.files   = self.get_files(path)
        print(self.folders)
        print(self.files)
        self.__dibujar_label_icon__(fila, 0, "drive", "flecha_abajo", label.text)
        for folder in self.folders:
            self.columna = 1
            fila += 1
            self.__dibujar_label_icon__(fila, self.columna, "folder", "circulo", folder)
        """
        for file in self.files:
            self.columna = 1
            fila += 1
            self.__dibujar_label_icon__(fila, self.columna, "files", "circulo", file)
        """
        self.__dibujar__()

    def __dibujar_label_icon__(self, fila, columna, icon, icon2, texto):
        labelicon = LabelIcon(self.form)
        x = (columna * 20) + 4
        y = (fila * 20) + 30
        labelicon.config(texto, x, y, 150, 12, icon, icon2, self.color_foco)
        labelicon.superficie = self.superficie_int
        # cambiamos el rectangulo para cuando revisa el click (posicion real)
        labelicon.rectangulo = (self.x + x, self.y+y, self.ancho, self.alto)
        labelicon.accion(self.funcion_accion)
        labelicon.dibujar()
        self.labelicon.append((fila, labelicon))

    def __obtener_fila__(self, id_control):
        # retorna la fila y el objeto
        resul = -1
        # buscar control
        for labels in self.labelicon:
            fila, labelicon = labels
            if labelicon.id == id_control:
                resul = fila, labelicon
                break
        return resul



    def get_drives(self):
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        print("BITMASK: " + str(bitmask))
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter + ":")
            bitmask >>= 1
        return drives

    def get_folders(self, path):
        folders = []
        contenido = os.listdir(path)
        for item in contenido:
            if os.path.isdir(path + item):
                folders.append(item)
        return  folders

    def get_files(self, path):
        files = []
        contenido = os.listdir(path)
        for item in contenido:
            if os.path.isfile(path + item):
                files.append(item)
        return files

    def __dibujar__(self):
        # Dibujar la superficie interna en la general
        self.superficie.blit(self.superficie_int, (self.x, self.y))

    ###################################
    ### EVENTOS TECLAS              ###
    ###################################
    def evento_key(self, cod_caracter, caracter):
        # pasamos el evento al textbox
        self.textbox.evento_key(cod_caracter, caracter)
