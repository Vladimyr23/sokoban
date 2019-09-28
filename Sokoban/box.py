#-------------------------------------------------------------------------------
# Name:        Box class
# Purpose:
#
# Author:      Vladimir Yesipov
#
# Created:     15/11/2016
# Copyright:   (c) Osnovnoy 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from move import Action

class Crate(Action):
    #inherit main attributes from move

    def __init__(self,cr,h):
        self.crates=[]
        self.holes=[]
        self.crates=cr
        self.holes=h

    '''def addCrate(self,i,j):
        self.crates.append([i,j])

    def addHole(self,i,j):
        self.holes.append([i,j])'''

    def getCrates(self):
        return self.crates

    def getHoles(self):
        return self.holes

    #def moveCrate(self, r, c, mr, mc):
    def makeMove(self, ind,row,col, r, c):
        move=Action()
        row,col=move.makeMove(row,col,r,c)
        #ind=int(ind)
        self.crates[ind] = [row, col]

    def setCrates(self, cr, h):
        self.crates=cr
        self.holes=h

    def isLevelComplete(self):
        """Returns True if all the holes have crates in them."""
        for hole in self.holes:
            if hole not in self.crates:
                # Found a space with a hole but no box on it.
                return False
        return True

