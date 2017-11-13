#>> Client.py
#>> Daniel Walsh

###############
### IMPORTS ###
###############

import socket as s
import threading as t
import pickle as p
import os

########################
### GLOBAL VARIABLES ###
########################

#>> Create a socket
sock = s.socket(s.AF_INET, s.SOCK_STREAM)
#>> Defines whether this client is player one or player two
playerNum = 0

#################
### FUNCTIONS ###
#################

def printBlankLine(num):
    ''' Prints board lines where no label is needed '''
    print("|".join(['   ' for x in range(num)]))

def printLabelLine(labels):
    ''' Prints board lnes where labels are needed '''
    print(" " + " | ".join(labels))

def printLabelController(size, currCount, labels):
    ''' Prepares input list for one row of the board depending upon count '''
    toPrint = [""] * size
    num = currCount*size
    count = 0
    while(count < size):
        toPrint[count] = labels[num]
        count += 1
        num += 1

    printLabelLine(toPrint)

def printBorderLine(num):
    ''' Prints board lines where a horizontal boarder line is needed '''
    count = 0
    strLine = ""
    while(count < num):
        strLine = strLine + "---"
        if(count+1 != num):
            strLine = strLine + "-"
        count += 1
    print(strLine)

def printBoard(boardSize, labels):
    ''' Uses other functions to print the board which has it's size determined by boardSize '''
    count = 0
    while(count < boardSize):
        #>> Prints a line to the screen without labels
        printBlankLine(boardSize)
        #>> Prints a line to the screen with labels
        printLabelController(boardSize, count, labels)
        #>> Prints a line to the screen without labels
        printBlankLine(boardSize)
        if(count < boardSize - 1):
            #>> Print horizontal line
            printBorderLine(boardSize)

        count += 1

def validatePos(pos, size, labels):
    ''' Checks whether the given position is a valid position within the given list '''
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

def sendMove():
    ''' This function is used to allow the user to enter their move and send it to the server '''
    while(True):
        #>> Get the users input
        move = input("")
        #>> Send the encoded version of the player move to the server
        sock.send(move.encode())

def getBoardFromList(gameList, boardSize = 3):
    ''' This function is used to return a list with the game board elements only '''
    labels = [''] * (boardSize**2)
    for i in range(0, boardSize**2):
        labels[i] = gameList[i]

    return labels

def clearScreen(userOs, mode):
    ''' This function is used to clear the terminal '''
    if(mode == "on"):
        if(userOs == "windows"):
            os.system("cls")
        elif(userOs == "linuxMac"):
            os.system("clear")
        else:
            print("Invalid OS!")

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
#>> windows/linuxMac
Os = 'windows'
#                    #
######################

#>> Create the socket connection with the given IP Address and the given port
sock.connect((hostIP, port))

#>> Create a thread that deals with sending a players move to the server
iThread = t.Thread(target=sendMove)
#>> This stops the thread from preventing the program from closing if all other code has finished
iThread.daemon = True
#>> Start the thread
iThread.start()

#>> Create the array used to define the game board
gameBoardLabels = []*(boardSize**2)

#>> Continue looping until the game has finished
while(True):
    #>> Receive data from the server
    pData = sock.recv(1024)

    #>> Failed to receive data
    if not pData:
        #>> Exit the game (while) loop
        break
    #>> Uses 'pickle' to decode the sent data back to an array
    data = p.loads(pData)
    #>> Selects only the board places part of the 'data' array and puts it into a new 'boardLabels' array
    boardLabels = getBoardFromList(data)
    #>> Only update the screen if the board has changed since the screen was last updated
    if(boardLabels != gameBoardLabels):
        #>> Clear the screen
        clearScreen(Os, "on")
        #>> Print the board to the screen
        printBoard(boardSize, boardLabels)
        #>> Store the most up-to-date version of the board
        gameBoardLabels = boardLabels

    #>> Check if the server is sending additional data
    if(data[10] == "win"):
        #>> A player has won
        if(data[11] == "x"):
            #>> Player one has won
            if(playerNum == "1"):
                #>> This client is player one
                print("You have won!")
            else:
                #>> This client is player two
                print("Player 1 has won!")
        elif(data[11] == "o"):
            #>> Player two has won
            if(playerNum == "2"):
                #>> This client is player two
                print("You have won!")
            else:
                #>> This client is player one
                print("Player 2 has won!")
        elif(data[11] == "DRAW"):
            #>> The game ended in a draw
            print("The game has ended in a draw!")
        else:
            #>> Unexpected data has been received in data[11]
            print("ERROR:: Winner not recognised!")
        #>> Exit the game (while) loop
        break
    elif(data[10] == "playerNum"):
        #>> data[11] contains either '1' or '2' defining while player this client is
        playerNum = data[11]
#>> Allow the user to control when the program exits
print("Press [ENTER] to end")
while(True):
    #>> Wait for the user to press enter
    uInput = input()
    #>> Exit the loop (and the program)
    break
