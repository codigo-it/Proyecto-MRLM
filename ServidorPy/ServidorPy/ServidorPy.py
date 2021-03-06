"""Servidor en Python que recibe datos y los guarda en una db mysql"""

import select
import socket
import sys
from sys import stdout, stderr
import sqlaccess
from position import Position
import logging
from logging.config import fileConfig
import queue
import time
import threading
import pygame
from pygame.locals import K_ESCAPE

def procesar_teclado(input_queue):
    """Hilo aparte que crea ventana SDL y lee del teclado para cerrar el hilo principal"""
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Ventana SDL')
    screen.fill((216,137,20))
    used_font = pygame.font.Font(None,17)
    done = False
    while not done:
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            done = True
            input_queue.put("ESC presionado en hilo 2")
    

# Create log file
LOGFILE = open("log.txt", "w")
fileConfig('logging_config.ini')
logger = logging.getLogger()

#Crear hilo aparte para leer de teclado y apagar el servidor
input_queue = queue.Queue()
input_thread = threading.Thread(target=procesar_teclado, args=(input_queue,))
input_thread.daemon = True
input_thread.start()


# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('192.168.1.20', 10000)

try:
    print('starting up on {} port {}'.format(server_address[0], server_address[1]), file=stdout)
    logger.info('starting up on {} port {}'.format(server_address[0], server_address[1]))
    server.bind(server_address)
except socket.error as err:
    print("Hubo error, el cual fue \n %s", str(err), file=stderr)
    exit(1)

# Listen for incoming connections
server.listen(5)

# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

#Mientras hayan sockets de "entrada" para leer

while inputs:
    # Wait for at least one of the sockets to be ready for processing
    print('\nEsperando el siguiente evento', file=stdout)
    logger.info('Esperando el siguiente evento')
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # Handle inputs
    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connection
            try:
                connection, client_address = s.accept()
                #print('new connection from {}'.format(client_address), file=stdout)
                logger.info('new connection from {}'.format(client_address))
                connection.setblocking(0)
                inputs.append(connection)
            except socket.error as err:
                print("Error al aceptar socket legible. El error fue \n%s", str(err), file=stderr)
                logger.error("Error al aceptar socket legible. El error fue \n%s")

            # Give the connection a queue for data we want to send
            #message_queues[connection] = Queue.Queue()

        #Si no es el server entonces es un socket recibiendo desde cliente
        else:
            try:
                data = s.recv(1024)
                if data:
                    # A readable client socket has data
                    print('received "%s" from %s' % (data, s.getpeername()), file=stdout)
                    logger.info('received "%s" from %s' % (data, s.getpeername()))

                    currentPosition = Position()
                    if not currentPosition.parse_message_to_data(str(data)):
                        try:
                            dbconnector = sqlaccess.DBConnection('root', '', '127.0.0.1', 'gps_db')
                            dbconnector.connect()
                            sqlstring = currentPosition.sql_position_insertion()
                            print(sqlstring, file=LOGFILE)
                            dbconnector.execute_sql(sqlstring)
                        except RuntimeError:
                            logger.error("Error insertando posicion en SQL")

                    #message_queues[s].put(data)
                    # Add output channel for response
                    if s not in outputs:
                        outputs.append(s)
                    else:
                        # Interpret empty result as closed connection
                        print('closing', client_address, 'after reading no data', file=stdout)
                    # Stop listening for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

                    ## Remove message queue
                    #del message_queues[s]
            except socket.error as err:
                logger.error("Error al leer (recv) desde socket. El error fue \n%s")

    # Handle outputs
    #for s in writable:
    #    try:
    #        next_msg = message_queues[s].get_nowait()
    #    except Queue.Empty:
    #        # No messages waiting so stop checking for writability.
    #        print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
    #        outputs.remove(s)
    #    else:
    #        print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
    #        s.send(next_msg)

    # Handle "exceptional conditions"
    for s in exceptional:
        print('handling exceptional condition for', s.getpeername(), file=sys.stderr)
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()


    if not input_queue.empty():
        logger.info("Apagando servidor")
        break

print("Adios")
        ## Remove message queue
        #del message_queues[s]
