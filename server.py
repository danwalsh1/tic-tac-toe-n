#>> Server.py
#>> Daniel Walsh

###############
### IMPORTS ###
###############

import socket as s
import threading as t
import pickle as p

############
### GAME ###
############

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.bind(('127.0.0.1', 12345))
sock.listen(1)

connections = []

def playerThread(conn, addr):
    while(True):
        rawData = conn.recv(1024)

        if not rawData:
            break

        data = str(addr) + ": " + str(rawData.decode())
        
        for connection in connections:
            if(connection != conn):
                connection.send(data.encode())
        
while(True):
    if(len(connections) < 2):
        conn, addr = sock.accept()
        cThread = t.Thread(target=playerThread, args=(conn, addr))
        cThread.daemon = True
        cThread.start()
        connections.append(conn)
        print("New connection from: " + str(conn))
