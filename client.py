#>> Client.py
#>> Daniel Walsh

###############
### IMPORTS ###
###############

import socket as s
import threading as t
import pickle as p

########################
### GLOBAL VARIABLES ###
########################

playerNum = -1
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
