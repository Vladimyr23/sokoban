#-------------------------------------------------------------------------------
# Name:        Level Class
# Purpose:
#
# Author:      Osnovnoy
#
# Created:     24/11/2016
# Copyright:   (c) Osnovnoy 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os


class Level:

    def __init__(self,cur_level):
        self.cur_level=cur_level
        self.level=[]
        self.crates = []
        self.holes = []
        self.load_level(self.cur_level)

    def load_level(self,cur_level):
        """Loads level from the file"""
        print cur_level
        level_name=str('levels\level'+str(cur_level)+".skb")
        level_path=os.path.join(os.getcwd(), level_name)
        with open(level_path) as level_file:
            lines=level_file.read().splitlines()
        for i in range (0,len(lines)):
            line=list(lines[i])
            self.level.append(line)


    def toString(self):
	"""prints out the level
	(none) -> none"""
        printme = ""
        for i in range (0,len(self.level)):
            for j in self.level[i]:
                printme = printme + j
            printme = printme + "\n"
        return printme

    def getPlayer(self):
        """Returns player parameters"""
        for i,lst in enumerate(self.level):
            for j,char in enumerate(lst):
                if char == 'P' or char == 'R':
                    self.row = i
                    self.col = j
                    self.pl_ch = char
                    return self.pl_ch,self.row,self.col
        return (None, None, None)

    def getCrates(self):
        #define crates positions
        for i,lst in enumerate(self.level):
            for j,char in enumerate(lst):
                if char =='*' or char =='@':
                    self.crates.append([i,j])
        return self.crates

    def getHoles(self):
        #define Holes positions
        for i,lst in enumerate(self.level):
            for j,char in enumerate(lst):
                if char=='o' or char=='@':
                    self.holes.append([i,j])
        return self.holes

    def placeChar (self, char, row, column):
	"""places player or crate at a specified row and column in the level
	(char, int, int) -> none
    >>>placeChar("$", 2, 2)
    NoneType"""
        self.level[row][column] = char

    def clearAtPos(self, row, col):
        self.level[row][col] = " "

    def getCharAtPos(self, row, col):
        """This method allows you to check for
        walls, crates, holes...
        '#'"""
        return self.level[row][col]

    def setCharAtPos(self,char, row, col):
        """This method allows you to move
        crates and player
        '#'"""
        self.level[row][col]=char

    def getWidth(self):
        self.width=len(max(self.level,key=len))
        return self.width

    def getHeight(self):
        self.height=len(self.level)
        return self.height

    def getLineWidth(self,h):
        self.lwidth=len(self.level[h])
        return self.lwidth

    def isExceptionalFail(self):
        """here I'll make some exceptional tests such as is the one player on the map and only one
         and is the amount of crates equal to the amount of holes"""
        pl_am=0
        for i,lst in enumerate(self.level):
            for j,char in enumerate(lst):
                if char == 'P' or char == 'R':
                    pl_am+=1

        if len(self.crates)==len(self.holes) and pl_am==1:
            return False
        else:
            return True

