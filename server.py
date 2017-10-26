#>> Server.py
#>> Daniel Walsh

###############
### IMPORTS ###
###############

import socket as s
import threading as t
import pickle as p
import time

########################
### GLOBAL VARIABLES ###
########################

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
currTurn = 0
labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', str(currTurn), 'empty', '']

#################
### Functions ###
#################

def validatePos(pos, size, labels):
    ''' This function is used to check if the players move is valid '''
    if(pos.isdigit()):
        #The string is a valid digit
        pos = int(pos)
        if(pos >= 0 and pos < size**2):
            if(labels[pos] != "X" and labels[pos] != "O"):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def playTurn(labels, pos, playerNum):
    ''' This function edits the given list to display the players move '''
    if(playerNum == 1):
        labels[pos] = "X"
    else:
        labels[pos] = "O"

    return labels

def playerThread(conn, addr, playerNum):
    ''' This function deals with a single clients data that the player has sent to the server '''

    global labels
    global currTurn
    
    while(True):
        data = conn.recv(1024).decode()

        if not data:
            break

        if(len(listOfPlayers) > 1):
            #>> The game is currently running
            if(currTurn == playerNum):
                #>> It is this players turn
                if(validatePos(data, 3, labels)):
                    #>> The players move is valid
                    #>> Make the move (edit the labels list)
                    labels = playTurn(labels, int(data), playerNum)
                    print("New Labels: " + str(labels))
                    #>> Move turn onto next player
                    if(currTurn == 1):
                        currTurn = 2
                        print("Player 2's turn!")
                    else:
                        currTurn = 1
                        print("Player 1's turn!")
        else:
            #>> Print to terminal, player data received but ignored
            print("Data recieved from: " + str(addr) + " >> Not enough players >> Data being ignored!")

def sendGameData(gameData, toWho = "ALL", conn = None):
    ''' This function either sends a game data list to both, or a single player. It can also print messages to the server terminal '''
    if(toWho == "ALL"):
        #>> Send the given data to both players
        for connection in listOfPlayers:
            sendData = p.dumps(gameData)
            connection.send(sendData)
            print("Data sent to all players!")
    elif(toWho == "SINGLE"):
        #>> Send the given data to the given connection
        sendData = p.dumps(gaeData)
        conn.send(sendData)
    else:
        #>> Display error message on the server terminal
        print("ERROR: [sendGameData] :: Invalid string given for toWho")

############
### GAME ###
############

######################
#      SETTINGS      #
hostIP = '127.0.0.1'
port = 12345
#                    #
######################

sock.bind((hostIP, port))
sock.listen(1)

listOfPlayers = []
        
while(True):
    if(len(listOfPlayers) < 2):
        conn, addr = sock.accept()
        cThread = t.Thread(target=playerThread, args=(conn, addr, len(listOfPlayers)+1))
        cThread.daemon = True
        cThread.start()
        listOfPlayers.append(conn)
        print("New connection from: " + str(addr))
    else:
        if(currTurn == 0):
            currTurn = 1
        sendGameData(labels)
        time.sleep(1)
