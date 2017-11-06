"""Pruebas de uso no bloqueante de teclado ni de pantalla
Se pretende leer desde teclado sin perjuicio de actualizar la informacion en consola/pantalla.
Para esto se probara usar pygame. Anteriormente se usó un thread extra con sys.stdin.read(1)
pero esto impide refrescar la consola hasta presionar Enter."""

import sys
import threading
import time
import queue
import pygame
from pygame.locals import *

def add_input(input_queue):
    """Funcion a ejecutar en nuevo thread, que maneje teclado y quizas pantalla/consola"""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Python numbers')
    screen.fill((159, 182, 205))
    used_font = pygame.font.Font(None, 17)

    def display_text(textString):
        """Crea una ventana SDL con el texto 'str' centrado"""
        text = used_font.render(textString, True, (255, 255, 255), (159, 182, 205))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery
        screen.blit(text, textRect)
        pygame.display.update()

    num = 0
    done = False
    while not done:
        display_text(str(num))
        num += 1

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            done = True
            input_queue.put("ESC presionado en hilo 2")

def foobar():
    input_queue = queue.Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.daemon = True
    input_thread.start()

    last_update = time.time()
    while True:

        if time.time()-last_update > 0.5:
            print(".")
            last_update = time.time()

        if not input_queue.empty():
            print("{}\nEscribe algo".format(input_queue.get()))
            user_input = input()
            print("Escribiste: {}\nSaliendo...".format(user_input))
            break
            

foobar()
