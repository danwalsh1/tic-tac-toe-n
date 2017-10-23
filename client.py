#>> Client.py
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
sock.connect(('127.0.0.1', 12345))

def sendMessage():
    while(True):
        message = input(">>")
        sock.send(message.encode())

iThread = t.Thread(target=sendMessage)
iThread.daemon = True
iThread.start()

while(True):
    data = sock.recv(1024)
    if not data:
        break
    print(data.decode())
