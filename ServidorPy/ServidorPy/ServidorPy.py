"""Servidor en Python que recibe datos y los guarda en una db mysql"""

import select
import socket
import sys
from sys import stdout, stderr
import sqlaccess
from position import Position
#import Queue


# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)

# Bind the socket to the port
server_address = ('192.168.1.30', 10000)

try:
    print('starting up on %s port %s', server_address[0], server_address[1], file=stdout)
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
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # Handle inputs
    for s in readable:
        if s is server:
            # A "readable" server socket is ready to accept a connection
            try:
                connection, client_address = s.accept()
                print('new connection from', client_address, file=stdout)
                connection.setblocking(0)
                inputs.append(connection)
            except socket.error as err:
                print("Error al aceptar socket legible. El error fue \n%s", str(err), file=stderr)

            # Give the connection a queue for data we want to send
            #message_queues[connection] = Queue.Queue()

        #Si no es el server entonces es un socket recibiendo desde cliente
        else:
            try:
                data = s.recv(1024)
                if data:
                    # A readable client socket has data
                    print('received "%s" from %s' % (data, s.getpeername()), file=stdout)

                    currentPosition = Position()
                    if not currentPosition.parse_message_to_data(str(data)):
                        try:
                            dbconnector = sqlaccess.DBConnection('root', '', '127.0.0.1', 'gps_db')
                            dbconnector.connect()
                            sqlstring = currentPosition.sql_position_insertion()
                            print(sqlstring)
                            dbconnector.execute_sql(sqlstring)
                        except RuntimeError:
                            print("Error insertando posicion en SQL")

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
                print("Error al leer (recv) desde socket. El error fue \n%s", str(err), file=stderr)

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

        ## Remove message queue
        #del message_queues[s]
