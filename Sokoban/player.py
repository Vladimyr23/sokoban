#-------------------------------------------------------------------------------
# Name:        Player class
# Purpose:
#
# Author:      Osnovnoy
#
# Created:     15/11/2016
# Copyright:   (c) Osnovnoy 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from move import Action

class Player(Action):
    #add player attributes first!

    def __init__(self,x,r,c):
        """constructor for the player.  Needs to pass in values
        for the character representing the player, the row and the column
        >>>Player("$", 2, 3)
        Nonetype"""
        self.player=[0,0,0]
        self.player[0]=x
        self.player[1]=r
        self.player[2]=c
        self.moves = 0

    def toString(self):
        info = "Player " + str(self.player[0]) + " at row " + str(self.player[1]) + " and column " + str(self.player[2])
        return info

    def getChar(self):
        return self.player[0]

    def getRow(self):
        return self.player[1]

    def getCol(self):
        return self.player[2]

    def setPlayer(self, x,r,c):
        self.player[0]=x
        self.player[1]=r
        self.player[2]=c

    def makeMove(self, x,row,col, r, c):
        move=Action()
        row,col=move.makeMove(row,col,r,c)
        self.player[0] = str(x)
        self.player[1]=row
        self.player[2]=col
        self.moves+=1


    def getMoves(self):
        return self.moves
