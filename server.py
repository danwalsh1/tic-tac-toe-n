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

def checkHor(labels, size):
    #>> Check rows for wins

    #>> Check for X win
    win = True
    count = 0
    while(count < size):
        count2 = count*size
        while(count2 < (count+1)*size):
            if(labels[count2] != "X" and win == True):
                win = False
            count2 += 1

        if(win == True):
            return "X"
        else:
            win = True
        count += 1
    #>> Check for O win
    win = True
    count = 0
    while(count < size):
        count2 = count*size
        while(count2 < (count+1)*size):
            if(labels[count2] != "O" and win == True):
                win = False
            count2 += 1

        if(win == True):
            return "O"
        else:
            win = True
        count += 1
    #>> No win has been found
    return "-"

def checkVer(labels, size):
    #>> Check columns for wins

    #>> Check for X win
    win = True
    count = 0
    while(count < size):
        count2 = 0
        while(count2 < size):
            #print(str(count+count2*size) + ":" + str(count) + ":" + str(count2))
            if(labels[count+count2*size] != "X" and win == True):
                win = False
            count2 += 1
        if(win == True):
            return "X"
        else:
            win = True
        count += 1
    #>> Check for O win
    win = True
    count = 0
    while(count < size):
        count2 = 0
        while(count2 < size):
            if(labels[count+count2*size] != "O" and win == True):
                win = False
            count2 += 1
        if(win == True):
            return "O"
        else:
            win = True
        count += 1
    #>> No win has been found
    return "-"

def checkDia(labels, size):
    #>> Check diagonals for wins

    #>> Top left to bottom right
    #>> Check for X win
    win = True
    count = 0
    while(count < size):
        if(labels[count*size+count] != "X" and win == True):
            win = False
        count += 1
    if(win == True):
        return "X"
    #>> Check for O win
    win = True
    count = 0
    while(count < size):
        if(labels[count*size+count] != "O" and win == True):
            win = False
        count += 1
    if(win == True):
        return "O"
    #>> Top right to bottom left
    #>> Check for X win
    win = True
    count = 0
    while(count < size):
        if(labels[(size-1)*(count+1)] != "X" and win == True):
            win = False
        count += 1
    if(win == True):
        return "X"
    #>> Check for O win
    win = True
    count = 0
    while(count < size):
        if(labels[(size-1)*(count+1)] != "O" and win == True):
            win = False
        count += 1
    if(win == True):
        return "O"
    
    
    return "-"

def checkWin(labels, size):
    check = False
    check = checkHor(labels, size)
    if(check == "X" or check == "O"):
        return check
    check = checkVer(labels, size)
    if(check == "X" or check == "O"):
        return check
    check = checkDia(labels, size)
    return check

def playerThread(conn, addr, playerNum, boardSize):
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
                    extentionList = ['', 'empty', '']
                    #print(labels)
                    labels = playTurn(labels, int(data), playerNum)
                    labels.extend(extentionList)
                    #print(labels)
                    checkBoardWin = checkWin(labels, boardSize)
                    if(checkBoardWin == "-"):
                        #>> Move turn onto next player
                        print("No win found!")
                        if(currTurn == 1):
                            currTurn = 2
                            print("Player 2's turn!")
                        else:
                            currTurn = 1
                            print("Player 1's turn!")
                        labels[9] = str(currTurn)
                    elif(checkBoardWin == "X"):
                        print("Player 1 has won!")
                        labels[10] = "win"
                        labels[11] = "x"
                    elif(checkBoardWin == "O"):
                        print("Player 2 has won!")
                        labels[10] = "win"
                        labels[11] = "o"
                    else:
                        print("ERROR: playerThread >> checkWin() returned:: " + str(checkBoardWin))

                    print("New Labels: " + str(labels))
        else:
            #>> Print to terminal, player data received but ignored
            print("Data recieved from: " + str(addr) + " >> Not enough players >> Data being ignored!")

############
### GAME ###
############

######################
#      SETTINGS      #
hostIP = '127.0.0.1'
port = 12345
boardSize = 3
#                    #
######################

sock.bind((hostIP, port))
sock.listen(1)

listOfPlayers = []
winCount = 0
        
while(True):
    if(len(listOfPlayers) < 2):
        conn, addr = sock.accept()
        cThread = t.Thread(target=playerThread, args=(conn, addr, len(listOfPlayers)+1, boardSize))
        cThread.daemon = True
        cThread.start()
        listOfPlayers.append(conn)
        print("New connection from: " + str(addr))
    else:
        if(currTurn == 0):
            currTurn = 1
        if(labels[10] == "win"):
            while(winCount < 10):
                sendGameData(labels)
                time.sleep(1)
                winCount += 1
            break
        sendGameData(labels)
        time.sleep(1)
