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

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
playerNum = 0
currTurn = -1

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
        printBlankLine(boardSize)
        printLabelController(boardSize, count, labels)
        printBlankLine(boardSize)
        if(count < boardSize - 1):
            printBorderLine(boardSize)

        count += 1

def validatePos(pos, size, labels):
    ''' Checks whether the given position is a valid position within the given list '''
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

def sendMove():
    ''' This function is used to allow the user to enter their move and send it to the server '''
    while(True):
        message = input("")
        sock.send(message.encode())

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

sock.connect((hostIP, port))

iThread = t.Thread(target=sendMove)
iThread.daemon = True
iThread.start()

gameBoardLabels = []*(boardSize**2)

while(True):
    pData = sock.recv(1024)
    if not pData:
        break
    data = p.loads(pData)
    boardLabels = getBoardFromList(data)
    if(boardLabels != gameBoardLabels):
        clearScreen(Os, "on")
        printBoard(boardSize, boardLabels)
        gameBoardLabels = boardLabels

    if(data[10] == "win"):
        if(data[11] == "x"):
            print("Player 1 has won!")
        elif(data[11] == "o"):
            print("Player 2 has won!")
        else:
            print("ERROR:: Winner not recognised!")
        break
print("Press any key to end")
end = False
while(end == False):
    uInput = input()
    end = True
