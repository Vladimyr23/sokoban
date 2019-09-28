#-------------------------------------------------------------------------------
# Name:        Class move which moves Crates and player
# Purpose:
#
# Author:      Osnovnoy
#
# Created:     23/11/2016
# Copyright:   (c) Osnovnoy 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#from level import Level

class Action:

    def makeMove(self,row,col, r, c):
        self.col = col+c
        self.row = row+r
        return self.row, self.col


