#-------------------------------------------------------------------------------
# Name:        Sokoban Top level
# Purpose:
#
# Author:      Osnovnoy
#
# Created:     24/11/2016
# Copyright:   (c) Osnovnoy 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#classes import
from level import Level
from player import Player
from box import Crate

#menu class and libraries for menu creation import
import random, sys, copy, os, pygame
from pygame.locals import *

cur_level=1
crates=[]
holes=[]
level=Level(cur_level)
char, row, col = level.getPlayer()
player=Player(char, row, col)
crates,holes=level.getCrates(),level.getHoles()
crate=Crate(crates,holes)

FPS = 30                    # frames per second to update the screen
WINWIDTH = 800              # width of the program's window, in pixels
WINHEIGHT = 600             # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2) #you need to know 1/2 sizes so you can
HALF_WINHEIGHT = int(WINHEIGHT / 2) #place things centrally


# The total width and height of each tile in pixels.
TILEWIDTH = 50
TILEHEIGHT = 50
TILEFLOORHEIGHT = 50

BRIGHTBLUE = (  0, 170, 255)
WHITE      = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

IMAGESDICT = {'floor': pygame.image.load("Images/floor.png"),
              'wall': pygame.image.load('images/wall.png'),
              'box': pygame.image.load("Images/thief.png"),
              'player': pygame.image.load("Images/cop.png"),
              'spacer': pygame.image.load("Images/spacer.png"),
              'hole': pygame.image.load("Images/cell.png"),
              'player_hole': pygame.image.load("Images/cop_cell.png"),
              'box_hole': pygame.image.load("Images/thief_cell.png"), }

TILEMAPPING = { '#':IMAGESDICT['wall'],
                ' ':IMAGESDICT['floor'],
                '*':IMAGESDICT['box'],
                '/':IMAGESDICT['spacer'],
                'P':IMAGESDICT['player'],
                'o':IMAGESDICT['hole'],
                'R':IMAGESDICT['player_hole'],
                '@':IMAGESDICT['box_hole']}


def drawMap(level):
    """draw the tile sprites onto this surface.
    this creates the visual map!"""
    mapSurfWidth = level.getWidth() * TILEWIDTH
    mapSurfHeight = level.getHeight() * TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR)
    for h in range(0,level.getHeight()):
        for w in range(0,level.getLineWidth(h)):
            thisTile = pygame.Rect((w * TILEWIDTH, h * TILEFLOORHEIGHT, TILEWIDTH, TILEHEIGHT))
            if level.getCharAtPos(h, w) in TILEMAPPING:
                #checks in the TILEMAPPING directory above to see if there is a
                #matching picture, then renders it
                baseTile = TILEMAPPING[level.getCharAtPos(h,w)]
            # Draw the tiles for the map.
            mapSurf.blit(baseTile, thisTile)
    return mapSurf

def restart(cur_level):
    """Restart level"""
    level.__init__(cur_level)
    print level.toString()
    char, row, col = level.getPlayer()
    player.__init__(char, row, col)
    crate.__init__(level.getCrates(),level.getHoles())
    drawMap(level)

def terminate():
    """quit game routine"""
    mapNeedsRedraw = False
    pygame.quit()
    sys.exit()

def nextlevel(cur_level):
    """Start next level"""
    level.__init__(cur_level)
    print level.toString()
    char, row, col = level.getPlayer()
    player.__init__(char, row, col)
    crates=[]
    holes=[]
    crates,holes=level.getCrates(),level.getHoles()
    crate.__init__(crates,holes)
    drawMap(level)


def isWall(next_place, row, col):
    """Returns True if the (row, col) position on
    the map is a wall, otherwise returns False."""
    if row < 0 or row >= level.getHeight() or col < 0 or col >= level.getLineWidth(row):
        print "row and col aren't actually on the map."
        return False # row and col aren't actually on the map.
    elif next_place == "#":
        print "This is a wall!"
        return True # wall is blocking
    return False

def isBlocked(next_next, crates, rr, cc):
    """Returns True if the (x, y) position on the map is
    blocked by a wall or box, otherwise returns False."""
    if rr < 0 or rr >= level.getHeight() or cc < 0 or cc >= level.getLineWidth(rr):
        print "row and col aren't actually on the map."
        return False # row and col aren't actually on the map.

    elif isWall(next_next, rr, cc):
        print "Road blocked"
        return True

    elif [rr, cc] in crates:
        print "a box is blocking"
        return True # a box is blocking

    return False

"""===========MOVE MAKING FUNCTION < ^ > v ======="""
def makeMove(r,c):
    #moving player ....
    char, row, col = level.getPlayer()
    crates=crate.getCrates()
    holes=crate.getHoles()
    next_place = level.getCharAtPos(player.getRow()+r, player.getCol()+c)
    # See if the player can move in that direction.
    if isWall(next_place, row + r, col + c):
        return False
    else:
        if [row + r, col + c] in crates:
            next_next = level.getCharAtPos(player.getRow()+(r*2), player.getCol()+(c*2))
            # There is a box in the way, see if the player can push it.
            if not isBlocked(next_next, crates, row + (r*2), col + (c*2)):
                # Move the box.
                if [row + (r*2), col + (c*2)] in holes:
                    level.setCharAtPos("@",row + (r*2), col + (c*2))
                else:
                    level.setCharAtPos("*",row + (r*2), col + (c*2))
                if [row + r, col + c] in holes:
                    level.setCharAtPos("R", row + r, col + c)
                    player.makeMove("R",row,col,r,c)
                    if [row,col] in holes:
                        level.setCharAtPos("o", row,col)
                    else:
                        level.clearAtPos(row,col)
                else:
                    level.setCharAtPos("P", row + r, col + c)
                    player.makeMove("P",row,col,r,c)
                    if [row,col] in holes:
                        level.setCharAtPos("o", row,col)
                    else:
                        level.clearAtPos(row,col)
                ind = crates.index([row + r, col + c])
                crate.makeMove(ind,row + r, col + c,r,c)
            else:
                return False
        # Move the player.
        elif [row + r, col + c] in holes:
            level.setCharAtPos("R", row + r, col + c)
            player.makeMove("R",row,col,r,c)
            if [row,col] in holes:
                level.setCharAtPos("o", row,col)
            else:
                level.clearAtPos(row,col)
        else:
            level.setCharAtPos("P", row + r, col + c)
            player.makeMove("P",row,col,r,c)
            if [row,col] in holes:
                level.setCharAtPos("o", row,col)
            else:
                level.clearAtPos(row,col)
        print level.toString()
        print player.toString()
        return True
"""===========MOVE PLAYER FUNCTION < ^ > v END======="""

"""++++++++++MAIN Program+++++++++"""
def main(cur_level):
    i=0
    while level.isExceptionalFail():
        """Exceptional conditions check, if fails start next level"""
        cur_level+=1
        i=i+1
        if cur_level>5:
            cur_level=1
        if i>5:
            print "No correct level found"
            terminate()
        nextlevel(cur_level)


    # Usual pygame initialization
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Sokoban')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, BASICFONT

    while True: # main game loop
        levelSurf = BASICFONT.render("Level: %s" %(cur_level), 1, TEXTCOLOR)
        levelRect = levelSurf.get_rect()
        levelRect.bottomleft = (20, WINHEIGHT - 35)
        # Reset these variables:
        playerMoveTo = None
        keyPressed = False
        move=False

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                # Player clicked the "X" at the corner of the window.
                exit=1
                terminate()

            elif event.type == KEYDOWN:
                # Direction or restart(SPACE) key press handling
                keyPressed = True

                if event.key == K_RIGHT:
                    move=makeMove(0,1)

                elif event.key == K_LEFT:
                    move=makeMove(0,-1)

                elif event.key == K_UP:
                    move=makeMove(-1,0)

                elif event.key == K_DOWN:
                    move=makeMove(1,0)

                elif event.key == K_SPACE:
                    restart(cur_level)

                elif event.key == K_ESCAPE:
                    terminate() # Esc key quits.

            mapNeedsRedraw = True

        DISPLAYSURF.fill(BGCOLOR) #draws the turquoise background
        #if something has changed, redraw....
        if mapNeedsRedraw:
            mapSurf = drawMap(level)
            mapNeedsRedraw = False

        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

        stepCounter=player.getMoves()
        DISPLAYSURF.blit(levelSurf, levelRect)
        stepSurf = BASICFONT.render('Steps: %s' % (stepCounter), 1, TEXTCOLOR)
        stepRect = stepSurf.get_rect()
        stepRect.bottomleft = (20, WINHEIGHT - 10)
        DISPLAYSURF.blit(stepSurf, stepRect)
        arrowSurf = BASICFONT.render('Arrow keys - move overseer', 1, TEXTCOLOR)
        arrowRect = arrowSurf.get_rect()
        arrowRect.bottomright = (WINWIDTH-20, WINHEIGHT - 60)
        DISPLAYSURF.blit(arrowSurf, arrowRect)
        spaceSurf = BASICFONT.render('Space - restart level', 1, TEXTCOLOR)
        spaceRect = spaceSurf.get_rect()
        spaceRect.bottomright = (WINWIDTH-20, WINHEIGHT - 35)
        DISPLAYSURF.blit(spaceSurf, spaceRect)
        escSurf = BASICFONT.render('Esc - quit the game', 1, TEXTCOLOR)
        escRect = escSurf.get_rect()
        escRect.bottomright = (WINWIDTH-20, WINHEIGHT - 10)
        DISPLAYSURF.blit(escSurf, escRect)


        # Draw the map on the DISPLAYSURF object.
        DISPLAYSURF.blit(mapSurf, mapSurfRect)


        if crate.isLevelComplete():
            """Level complete, start next level"""
            cur_level+=1
            if cur_level>5:
                cur_level=1
            nextlevel(cur_level)
            i=0
            while level.isExceptionalFail():
                """Exceptional conditions check, if fails start next level"""
                cur_level+=1
                i=i+1
                if cur_level>5:
                    cur_level=1
                if i>5:
                    print "No correct level found"
                    terminate()
                nextlevel(cur_level)


        pygame.display.update() # draw DISPLAYSURF to the screen.
        FPSCLOCK.tick()

if __name__ == '__main__':
    main(cur_level)
