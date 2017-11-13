#>> Server.py
#>> Daniel Walsh
#>> Code not to be used without written permission from Daniel Walsh.
#>> Credit must be given to Daniel Walsh if code is used once permission is given.

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

#>> Create a socket
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
#>> Used to store how many 'turns' have been taken
currTurn = 0

#>> labels[0] to labels[8] = Board places
#>> labels[9] = current turn
#>> labels[10] = data sent type
#>> labels[11] = data sent
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
            #>> The given integer is in the valid range
            if(labels[pos] != "X" and labels[pos] != "O"):
                #>> The space hasn't already been taken by a player
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
        #>> Player one = "X"
        labels[pos] = "X"
    else:
        #>> Player two = "O"
        labels[pos] = "O"

    return labels

def sendGameData(gameData, toWho = "ALL", conn = None):
    ''' This function either sends a game data list to both, or a single player. It can also print messages to the server terminal '''
    if(toWho == "ALL"):
        #>> Send the given data to both players
        for connection in listOfPlayers:
            #>> Encode the array into raw bytes
            sendData = p.dumps(gameData)
            #>> Send the raw bytes to the clients
            connection.send(sendData)
    elif(toWho == "SINGLE"):
        #>> Send the given data to the given connection
        #>> Encode the array into raw bytes
        sendData = p.dumps(gameData)
        #>> Send the raw bytes to the client
        conn.send(sendData)
    else:
        #>> Display error message on the server terminal
        print("ERROR: [sendGameData] :: Invalid string given for toWho")

def checkHor(labels, size):
    ''' The function checks for either player win along all horizontal options '''
    #>> Check rows for wins

    #>> Check for X win
    win = True
    count = 0
    while(count < size):
        count2 = count*size
        while(count2 < (count+1)*size):
            if(labels[count2] != "X" and win == True):
                #>> Player one hasn't won in this line
                win = False
            count2 += 1

        if(win == True):
            #>> Player one has won in this line
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
                #>> Player two hasn't won in this line
                win = False
            count2 += 1

        if(win == True):
            #>> Player two has won in this line
            return "O"
        else:
            win = True
        count += 1
    
    #>> No win has been found
    return "-"

def checkVer(labels, size):
    ''' The function checks for either player win along all vertical options '''
    #>> Check columns for wins

    #>> Check for X win
    win = True
    count = 0
    while(count < size):
        count2 = 0
        while(count2 < size):
            if(labels[count+count2*size] != "X" and win == True):
                #>> Player one hasn't won in this line
                win = False
            count2 += 1
        if(win == True):
            #>> Player one has won in this line
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
                #>> Player two hasn't won in this line
                win = False
            count2 += 1
        if(win == True):
            #>> Player two has won in this line
            return "O"
        else:
            win = True
        count += 1
    
    #>> No win has been found
    return "-"

def checkDia(labels, size):
    ''' The function checks for either player win along all diagonal options '''
    #>> Check diagonals for wins

    #>> Top left to bottom right
    #>> Check for X win
    win = True
    count = 0
    while(count < size):
        if(labels[count*size+count] != "X" and win == True):
            #>> Player one hasn't won in this line
            win = False
        count += 1
    if(win == True):
        #>> Player one has won in this line
        return "X"
    #>> Check for O win
    win = True
    count = 0
    while(count < size):
        if(labels[count*size+count] != "O" and win == True):
            #>> Player two hasn't won in this line
            win = False
        count += 1
    if(win == True):
        #>> Player two has won in this line
        return "O"
    #>> Top right to bottom left
    #>> Check for X win
    win = True
    count = 0
    while(count < size):
        if(labels[(size-1)*(count+1)] != "X" and win == True):
            #>> Player one hasn't won in this line
            win = False
        count += 1
    if(win == True):
        #>> Player one has won in this line
        return "X"
    #>> Check for O win
    win = True
    count = 0
    while(count < size):
        if(labels[(size-1)*(count+1)] != "O" and win == True):
            #>> Player two hasn't won in this game
            win = False
        count += 1
    if(win == True):
        #>> Player two has won in this game
        return "O"
    
    #>> No win has been found
    return "-"

def checkEnd(labels, size):
    ''' This function is used to check if the game has ended in a draw '''
    count = 0
    while(count < size**2):
        if(labels[count] != "X" and labels[count] != "O"):
            #>> Game has not ended in a draw yet
            return "-"
        count += 1
    #>> Game has ended in a draw
    return "DRAW"

def checkWin(labels, size):
    ''' The function uses other function to check for either player win along all options '''
    check = False
    #>> Check horizontal lines
    check = checkHor(labels, size)
    if(check == "X" or check == "O"):
        return check
    #>> Check vertical lines
    check = checkVer(labels, size)
    if(check == "X" or check == "O"):
        return check
    #>> Check diagonal lines
    check = checkDia(labels, size)

    check2 = checkEnd(labels, size)
    if(check2 == "DRAW"):
        return check2
    return check

def playerThread(conn, addr, playerNum, boardSize):
    ''' This function deals with a single clients data that the player has sent to the server '''

    global labels
    global currTurn

    #>> Sends the client, their player number
    labels[10] = "playerNum"
    labels[11] = str(playerNum)
    sendGameData(labels, "SINGLE", conn)
    #>> Resets the additional data elements
    labels[10] = "empty"
    labels[11] = ""
    
    while(True):
        #>> Receive data from the player
        data = conn.recv(1024).decode()

        #>> Failed to receive data
        if not data:
            print("Connection Lost (" + str(addr) + ")")
            #>> Exit the game (while) loop
            break

        if(len(listOfPlayers) > 1):
            #>> The game is currently running
            if(currTurn == playerNum):
                #>> It is this players turn
                if(validatePos(data, 3, labels)):
                    #>> The players move is valid
                    #>> Make the move (edit the labels list)
                    labels = playTurn(labels, int(data), playerNum)
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
                    elif(checkBoardWin == "DRAW"):
                        print("Game has ended in a draw!")
                        labels[10] = "win"
                        labels[11] = "DRAW"
                    else:
                        print("ERROR: playerThread >> checkWin() returned:: " + str(checkBoardWin))
                    #>> Print to the server -> the new board labels array
                    print("New Labels: " + str(labels))
                else:
                    #>> Player input an invalid move
                    print("Player " + str(playerNum) + " played invalid move! Ignoring:: " + data)
            else:
                #>> Player input when it wasn't their turn
                print("Player " + str(playerNum) + " played out of turn! Ignoring:: " + data)
        else:
            #>> Print to terminal, player data received but ignored (not enough players)
            print("Data recieved from: " + str(addr) + " >> Not enough players >> Data being ignored!")

############
### GAME ###
############

######################
#      SETTINGS      #
#>> Host's IP Address
hostIP = '127.0.0.1'
#>> Port to use for socket
port = 12345
#>> Horizontal/vertical size of board
boardSize = 3
#                    #
######################

print("Server starting...")

#>> Bind the server socket to the given IP address and port
sock.bind((hostIP, port))
#>> Start listening for clients
sock.listen(1)

print("Waiting for connections")

listOfPlayers = []
winCount = 0
        
while(True):
    if(len(listOfPlayers) < 2):
        #>> Game can not play -> accepting more connections
        #>> Accept and store connections
        conn, addr = sock.accept()
        #>> Create and start a thread for that client
        cThread = t.Thread(target=playerThread, args=(conn, addr, len(listOfPlayers)+1, boardSize))
        cThread.daemon = True
        cThread.start()
        #>> Store the new connection
        listOfPlayers.append(conn)
        print("New connection from: " + str(addr))
    else:
        #>> Game can play -> not accepting more connections
        if(currTurn == 0):
            #>> Start the game if it hasn't already been started
            currTurn = 1
        if(labels[10] == "win"):
            #>> Send win data if a win has been found
            while(winCount < 10):
                sendGameData(labels)
                time.sleep(1)
                winCount += 1
                print("Server closing in " + str(10 - winCount) + " second(s)")
            break
        sendGameData(labels)
        time.sleep(1)
