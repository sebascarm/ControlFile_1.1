# -*- coding: utf-8 -*-

###########################################################
### EVENTOS V1.1                                        ###
###########################################################
### ULTIMA MODIFICACION DOCUMENTADA                     ###
### 10/03/2021                                          ###
### Se ocultan algunos prints para hacer un mejor dbug  ###
###########################################################


""" SECCION DE EVENTOS, QUIEN DISPARA LOS EVENTOS A LOS OBJETOS
"""
import pygame
from winform.base.funciones import Esta_Adentro 


def eventos(c_screen):
    """ Recorremos los eventos de pygame, eventos que se activan con acciones de apretar, etc.
    """
    for evento in pygame.event.get():
        # Revisamos eventos propietarios de Android
        if evento.type == pygame.QUIT:
            pygame.quit()
            return False # enviamos salida del programa
        # Evento de resize de screen
        if evento.type == pygame.VIDEORESIZE:
            print("Evento resize pendiente")
        # eventos de posicion (recorrer formularios)
        for formu in c_screen.formularios:
            # recorrer objetos
            salir_de_evento = False
            for objeto in formu.objetos:
                if not salir_de_evento:
                    salir_de_evento = evento_objeto(evento, objeto)
                
    #repeticion_tecla()
    return True
    
def evento_objeto(event, objeto):
    # Moviemiento de mouse
    if event.type == pygame.MOUSEMOTION:
        coordenada = event.pos 
        # revisar ESTADO dentro
        if objeto.estado == 0:  # Estaba afuera
            if Esta_Adentro(objeto.rectangulo, coordenada):
                # print("En objeto") # para DEBUG
                try:
                    objeto.estado = 1
                    objeto.evento_mouse_over()
                except:
                    pass
                    # print("objeto sin evento MOUSE MOTION") # para DEBUG
        # revisar fuera
        if objeto.estado == 1:    # Estaba adentro
            if not Esta_Adentro(objeto.rectangulo, coordenada):
                # print("Fuera de Objeto") # para DEBUG
                try:
                    objeto.estado = 0
                    objeto.evento_mouse_out()
                except:
                    pass
                    # print("objeto sin evento MOUSE MOTION") # para DEBUG
    # Evento click
    if event.type == pygame.MOUSEBUTTONDOWN:
        # revisar si esta adentro
        if objeto.estado == 1:  #Estaba adentro
            print("Objeto Presionado ID: " + str(objeto.id) + " " + str(objeto.__class__.__name__))
            try:
                objeto.estado = 2
                objeto.evento_mouse_click()
            except:
                pass
                # print("objeto sin evento BOTON DOWN")
        # revisar si estaba afuera
        if objeto.estado == 0:  # Estaba afuera
            try:
                objeto.evento_mouse_click_out()
            except:
                pass
                # print("objeto sin evento BOTON DOWN")
    # Eventos sulta boton
    if event.type == pygame.MOUSEBUTTONUP:
        # revisar si estaba presionado
        if objeto.estado == 2:  # Estaba presionado
            # revisar en que estado se encuentra
            coordenada = event.pos 
            if Esta_Adentro(objeto.rectangulo, coordenada):
                # print("Objeto suelto - en Objeto ID:" + str(objeto.id) + " " + str(objeto.__class__.__name__))
                try:
                    objeto.estado = 1
                    objeto.evento_mouse_over()
                    # Realizar accion
                    print("accion soltar boton")
                    objeto.evento_mouse_click_release() # para que se ejecute accion al soltar el boton
                except:
                    pass
                    # print("objeto sin evento BOTON UP")
            else:
                print("Objeto suelto - Fuera de Objeto")
                try: 
                    objeto.estado = 0
                    objeto.evento_mouse_out()
                    # Realizar accion
                    print("accion soltar boton")
                    objeto.evento_mouse_click_release()
                except:
                    pass
                    # print("objeto sin evento BOTON UP")
    
    # Eventos de teclado
    if event.type == pygame.KEYDOWN:
        # revsiar si el objeto tiene el foco
        try:
            if objeto.foco:
                objeto.evento_key(event.key, event.unicode)
                print("EVENTO KEY ID: " + str(objeto.id) + " " + str(objeto.__class__.__name__))
                # evitamos que los demas objetos recorrar nos eventos
                return True
        except:
            # print("objeto sin evento KEY")
            pass

    # Evento al soltar la tecla
    if event.type == pygame.KEYUP:
        # revsiar si el objeto tiene el foco
        try:
            if objeto.foco:
                objeto.evento_keyup(event.key) # en key up no hay unicode
                print("EVENTO KEYUP ID: " + str(objeto.id) + " " + str(objeto.__class__.__name__))
                # evitamos que los demas objetos recorrar nos eventos
                return True
        except:
            # print("objeto sin evento KEY UP")
            pass
                
        
    # repeticion de tecla
    
def repeticion_tecla():
    tecla = pygame.key.get_pressed()
    print(tecla)
