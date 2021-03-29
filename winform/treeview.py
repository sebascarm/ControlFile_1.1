# -*- coding: utf-8 -*-

###########################################################
### CLASE Tree View V1.1                                ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 29/03/2021                                          ###
### Correcciones y correcta eliminacion de elementos    ###
### Creacion                                            ###
###########################################################
import string
from ctypes import windll
import os
import time
import pygame
from winform.base.objetogral import ObjetoGral
from winform.textbox import Textbox
from winform.labelicon import LabelIcon
from winform.base.thread_admin import ThreadAdmin
from winform.base.funciones import AutoBrillo

class TreeView(ObjetoGral):
    def __init__(self, form):
        super().__init__(form)  # instanciamos la clase padre
        # propiedades internas
        self.folder = ""
        self.drives = []  # lista de unidades
        self.ref_label = []  # lista de labeliconos
        self.info_icons = []  # columna, id_control, texto, ruta, icon, icon2, color // sacamos la fila ,color en caso de requerir distinto
        self.superficie_int = ''  # type: pygame.Surface # modificamos la surface para usar una propia
        self.area_int = (0, 0, 0, 0)  # para definir el area interna relativa, distito a recuadro
        self.y_int = 0  # para desplazar
        self.th_espera = ThreadAdmin()
        self.tmp_carpetas = []
        self.tmp_archivos = []
        self.datos_obtenidos = False
        self.max_alto = 5000

    def config(self, text, x, y, ancho, alto, folder=''):
        super().config(x, y, ancho, alto, text, False)
        self.folder = folder
        self.area_int = (0, 0, self.ancho, self.alto)
        self.superficie_int = pygame.Surface((self.ancho, self.max_alto))  # dibujamos (cambiar el 1000 todo
        self.y_int = self.y
        self.color_b3 = AutoBrillo(self.color, 150)
        self.funcion = ''

    def dibujar(self):
        self.__limpiar_ojetos__()
        self.__cargar_unidades__()
        self.__dibujar__()

    def __dibujar__(self):
        # borrar todos
        pygame.draw.rect(self.superficie_int, self.color, (0, 0, self.ancho, self.max_alto), 0)
        # generar y cagar labelincon
        for indice in range(len(self.info_icons)):
            columna, id_control, texto, ruta, icon, icon2, color = self.info_icons[indice]
            # creamos y dibujamos el label
            objeto_id = self.__crear_labelicon__(indice, columna, icon, icon2, texto, color)
            # actualizamos el el info_icon con el id del control
            self.info_icons[indice] = [columna, objeto_id, texto, ruta, icon, icon2, color]
        # Dibujar la superficie interna en la general
        self.superficie.blit(self.superficie_int, (self.x, self.y), self.area_int)
        self.actualizar()

    def __cargar_unidades__(self):
        columna = 0
        drives = self.get_drives()
        self.info_icons.clear()
        for fila in range(len(drives)):
            unidad = drives[fila]
            self.info_icons.append([columna, -1, unidad, unidad, "drive", "circulo", ''])

    def __limpiar_ojetos__(self):
        for indice in range(len(self.ref_label)):
            self.ref_label[0].delete()    # siempre es 0 porque el delete saca la referencia
            self.form.objetos.remove(self.ref_label[0])
            del self.ref_label[0]
        self.ref_label.clear()

    def evento_accion(self, id_control):
        # borrar objetos
        self.__limpiar_ojetos__()
        fila, columna, id_objeto, texto, ruta, ico, icon2, color = self.__obtener_info__(id_control)
        # almacenar incial
        info_tmp = self.__caga_inicial__(fila)
        # determinar modificacion
        if icon2 == "flecha_abajo":     # cerrar directorio
            # almacena objeto modificado
            info_tmp.append([columna, id_objeto, texto, ruta, ico, "flecha_derecha", self.color_b3])
            # realizar accion
            if self.funcion != '':
                self.funcion(self.id, ruta)
            # almacenar final
            info_tmp.extend(self.__cargar_final2__(fila + 1, columna))
        else:
            if icon2:   # no es un archivo
                # almacena objeto modificado
                info_tmp.append([columna, id_objeto, texto, ruta, ico, "flecha_abajo", self.color_b3])
                # realizar accion
                if self.funcion != '':
                    self.funcion(self.id, ruta)
                # cargar nuevos
                info_tmp.extend(self.__cargar_nuevos__(ruta, columna + 1))
            else:       # es un archivo
                info_tmp.append([columna, id_objeto, texto, ruta, ico, "", self.color_b3])

            # almacenar final
            info_tmp.extend(self.__cargar_final__(fila + 1))
        self.info_icons = []
        self.info_icons.extend(info_tmp)
        self.__dibujar__()

    def __caga_inicial__(self, fila_final):
        info_tmp = []
        for indice in range(len(self.info_icons)):
            if indice < fila_final:
                self.info_icons[indice][6] = ''           # vaciamos el color
                info_tmp.append(self.info_icons[indice])  # devuelve la fila
        return info_tmp

    def __cargar_final__(self, fila_inicial):
        info_tmp = []
        for indice in range(len(self.info_icons)):
            if indice >= fila_inicial:
                self.info_icons[indice][6] = ''  # vaciamos el color
                info_tmp.append(self.info_icons[indice])  # devuelve la fila
        return info_tmp

    def __cargar_final2__(self, fila_inicial, columna_menor):
        info_tmp = []
        for indice in range(len(self.info_icons)):
            if indice >= fila_inicial:
                if self.info_icons[indice][0] <= columna_menor:
                    info_tmp.append(self.info_icons[indice])  # devuelve la fila
        return info_tmp

    def __cargar_nuevos__(self, ruta, columna):
        info_tmp = []
        self.datos_obtenidos = False
        self.th_espera.start(self.__th_carpetas_archivos__, ruta, 'OBTENER_ARCHIVOS')
        # esperamos x 2 segundos
        for tiempo in range(10):
            if self.datos_obtenidos:
                break
            time.sleep(0.1)
        self.th_espera.close()
        for carpeta in self.tmp_carpetas:
            info_tmp.append([columna, -1, carpeta[0], carpeta[1], "folder", "circulo", ''])
        for archivo in self.tmp_archivos:
            info_tmp.append([columna, -1, archivo[0], archivo[1], "file", "", ''])
        return info_tmp

    def __th_carpetas_archivos__(self, ruta):
        self.tmp_carpetas = []
        self.tmp_archivos = []
        try:
            self.tmp_carpetas = self.get_folders(ruta)
            self.tmp_archivos = self.get_files(ruta)
        except:
            print("No se pueden cargar los archivos y carpetas")
        self.datos_obtenidos = True

    def __crear_labelicon__(self, fila, columna, icon, icon2, texto, color=''):
        """ Al crear el objeto devolvemos el ID creado
        """
        labelicon = LabelIcon(self.form)
        labelicon.set_hijo()

        if icon2: x = (columna * 20) + 4
        else:     x = (columna * 20) + 20
        y = (fila * 20) + 10
        ancho = 200
        alto = 14
        labelicon.config(texto, x, y, ancho, alto, icon, icon2, self.color)
        if color:
            labelicon.color = color
        labelicon.superficie = self.superficie_int
        # cambiamos el rectangulo para cuando revisa el click (posicion real)
        self.__actualizar_poslabel__(labelicon)
        # si es archivo no se asigna accion:

        #if icon2:
        labelicon.accion(self.evento_accion)

        labelicon.dibujar()
        objeto_id = labelicon.id
        # agregamos a la referencia
        self.ref_label.append(labelicon)
        return objeto_id

    def __obtener_info__(self, id_control):
        # retorna la fila y el objeto
        resul = -1
        # buscar control
        for fila, info in enumerate(self.info_icons):
            columna, id_objeto, texto, ruta, ico, icon2, color = info
            if id_objeto == id_control:
                resul = fila, columna, id_objeto, texto, ruta, ico, icon2, color
                break
        return resul

    def get_drives(self):
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter + ":")
            bitmask >>= 1
        return drives

    def get_folders(self, path):
        """Devuelve una lista con nombres y ruta aparte
        """
        folders = []
        ruta = path + "/"
        print(ruta)
        contenido = os.listdir(ruta)
        for item in contenido:
            if os.path.isdir(ruta + item):
                folders.append([item, ruta + item])
        return folders

    def get_files(self, path):
        """Devuelve una lista con nombres y ruta aparte
        """
        files = []
        ruta = path + "/"
        contenido = os.listdir(ruta)
        for item in contenido:
            if os.path.isfile(ruta + item):
                files.append([item, ruta + item])
        return files

    def __desplazar_area__(self, desplazamiento):
        """ :param desplazamiento: unidades de desplazamiento
        """
        habilitado = False
        desplaza = 20 * desplazamiento
        x, y, ancho, alto = self.area_int
        y += desplaza
        visible = self.alto - 40    # el 60 es un parametro que no se porque
        maximo = len(self.info_icons) * 20 - y
        if (desplazamiento < 0) and (y >= 0):
            habilitado = True
        elif (desplazamiento > 0) and (maximo > visible):
            habilitado = True
        if habilitado:
            self.area_int = (x, y, ancho, alto)
            print(self.area_int)
            for label in self.ref_label:
                self.__actualizar_poslabel__(label)

    def __actualizar_poslabel__(self, label):
        x_real = self.x + label.x - self.area_int[0]
        y_real = self.y + label.y - self.area_int[1]  # obtenemos el y del area interna
        x_max = self.x + self.ancho
        y_max = self.y + self.alto
        # coordenadas reales
        # minimos
        if y_real < self.y:
            y_real = self.y
        if x_real < self.x:
            x_real = self.x
        # maximos
        if x_real > x_max:
            x_real = x_max
        if y_real > y_max:
            y_real = y_max
        # ancho real
        ancho_real = label.ancho
        alto_real = label.alto
        if x_real + label.ancho > x_max:
            ancho_real = x_max - x_real
        if y_real + label.alto > y_max:
            alto_real = y_max - y_real
        # resultados
        label.rectangulo = x_real, y_real, ancho_real, alto_real
        label.rect_foco = x_real - 1, y_real - 1, ancho_real + 1, alto_real + 1

    ###################################
    ### EVENTOS SCROLL              ###
    ###################################
    def evento_mouse_scrollup(self):
        self.__desplazar_area__(-1)
        # redibujar
        self.superficie.blit(self.superficie_int, (self.x, self.y), self.area_int)
        self.actualizar()

    def evento_mouse_scrolldown(self):
        self.__desplazar_area__(1)
        # redibujar
        self.superficie.blit(self.superficie_int, (self.x, self.y), self.area_int)
        self.actualizar()

    ###################################
    ### EVENTOS TECLAS              ###
    ###################################
    # def evento_key(self, cod_caracter, caracter):
        # pasamos el evento al textbox
    #    self.textbox.evento_key(cod_caracter, caracter)
