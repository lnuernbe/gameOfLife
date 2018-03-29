# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 12:18:42 2018

@author: Lea
"""
import numpy as np
import matplotlib.pyplot as pl
from matplotlib.patches import Rectangle
from matplotlib.widgets import *

pl.ion()

class cell(object):
#constructor,cell only knows whether it is live '1' or dead '0'    
    def __init__(self, state = None):
        #if state is given, cell is set to that state
        if not state == None:
            #if state is 1 or 0 all right
            if (state == 0)| (state == 1):
                self._state = state
            #if not exception is raised as state must always be 1 or 0
            else:
                raise Exception ('State of Cell must be 0 for dead or 1 for alive')
        #if no state is given it is set to 0 by default        
        else:
            self._state = 0
    
    #when cell is called in string context state is printed
    def __str__(self):
        return str(self._state)
    
    #returns current state
    def getState(self):
        return self._state
    
    #cell lives, eg state is set to 1
    def live(self):
        self._state = 1
    
    #cell dies, eg state is set to 0
    def die(self):
        self._state = 0
    
    #plots cell at a given position in form of a rectangle, red if live, white if dead
    def plot(self, pos1, pos2, width, event):
        global ax
        print 'hey'
        #measures of the rectangle are calculated
        x = pos1*width
        y = pos2*width
        #if cell lives draw red rectangele
        if self._state == 1:
            localRectangle = Rectangle((x,y), width, width, color= 'r')
        #else white
        else:
            localRectangle = Rectangle((x,y), width, width, color= 'w')
        ax.add_artist (localRectangle)
        pl.draw()

class GameOfLife(object):

#constructor, gameOfLife is defined as a quadratic list of lists of cells, knowing its dimension    
    def __init__(self, dimension):
        self._dimension = dimension
        goL = []
        #gameOfLife is by default costructed as a list of lists of dead cells
        #dimension of list is two higher than dimension, leaving a margin of zeros all around
        #for calculation purposes later
        for i in range(dimension + 2):
            tmp = []
            for j in range(dimension + 2):
                tmp.append(cell())
            goL.append(tmp)
        self._gameOfLife = goL
        

    #if called in a string context, states are written to list of lists and thos one is printed    
    def __str__(self):
        goL = np.eye(self._dimension + 2)
        for i in range (self._dimension + 2):
            for j in range (self._dimension + 2):
                goL[i][j] = self._gameOfLife[i][j]._state
        return str(goL)
    #in a dead game live cells are added at given positions
    def addCell(self, position1, position2):
        self._gameOfLife[position1 + 1][position2 + 1].live()

    #rules are applied once to whole of game of life
    def iterateOnce(self):
        #game of live is saved to a second li'o'li to save former status relevant for calculations
        tmp = GameOfLife(self._dimension)
        #loop through all cells, leaving aside the margin
        for i in range (self._dimension):
            for j in range (self._dimension):
                #indicator measures the number of live cells of the current cell
                indicator = 0
                for k in range (3):
                    for l in range (3):
                        #values of all nine cells are added up
                        indicator += self._gameOfLife[i + k][j + l]._state
                #value of current cell is substracted        
                indicator = indicator - self._gameOfLife[i + 1][j + 1]._state
                #rules are applied. If current cell is dead...
                if self._gameOfLife[i + 1][j + 1].getState() == 0:
                    #...and has exactly three live neighbors, cell is born
                    if indicator == 3:
                        tmp._gameOfLife[i + 1][j + 1].live()
                #if current cell is alive...
                else:
                #and has feweer than two or more than three live neighbors it dies
                    if (indicator < 2) | (indicator > 3):
                        tmp._gameOfLife[i + 1][j + 1].die()
                #else cell continues live
                    if (indicator == 2) | (indicator == 3):
                        tmp._gameOfLife[i + 1][j + 1].live()
        #previous gameofLife is updated and returned                
        self = tmp
       
    
    #rules are applied a given number of times, goL is plotted at each step
    def iterate(self, times):
        print '1'
        for i in range(times):
            #iterate given number of times
            print '2: ' + str(i)
            self.iterateOnce()
            #plot yourself
            print '3'
            self.plot(event)
            print '4'
           
            #pause two seconds as to make changes appreciable
     
            #update self and return
    
            print self
        return self
    
    #plots goL by looping through al cells and plotting them
    def plot(self, event):
        for i in range(self._dimension):
            for j in range(self._dimension):
                #trandformation between images coordinates and list indexes
                self._gameOfLife[i + 1][j + 1].plot(j, self._dimension - i, 1.0/self._dimension, event)
                
    
    #function to be called when start button is pressed
    def start(self, event):
       #when start button is pressed iterate the number of times the slider indicate
       print  '0'
       self.iterate(timesint, event)
       print '5'
       self.plot(event)
    
    
    #clear by murdering all cells
    def clear(self, event):
        #print "1" + str(self)
        self = GameOfLife(self._dimension)
        #print self
        self.plot(event)
        
        
    

#live cell is plotted
def cellLives(event):
    global ax # macht das Objekt local zugaenglich...
    x = int(event.xdata/width)
    y = int(event.ydata/width) 
    localRechteck = Rectangle((x*width,y*width), width, width, color='r')
    ax.add_artist (localRechteck)
    event.canvas.draw()

#dead cell is plotted
def cellDead(event):
    global ax # macht das Objekt local zugaenglich...
    x = int(event.xdata/width)
    y = int(event.ydata/width) 
    localRechteck = Rectangle((x*width,y*width), width, width, color='w')
    ax.add_artist (localRechteck)
    event.canvas.draw()

#goL is initalized and plotted
def handleEvent(event):
    #event data is transformed in list indexes
    print 'ha'
    x = int(event.xdata/width)
    y = int(event.ydata/width) 
    x_new = x + 1
    y_new = dimension - y
    #if cell at clicked position is dead...
    if goL._gameOfLife[y_new][x_new]._state == 0:
        #...plot live cell..
        cellLives(event)
        #...and update goL
        goL._gameOfLife[y_new][x_new].live()
    #if cell at clicked position is dead...
    else:
        #...plot dead cell...
        cellDead(event)
        #...and update goL
        goL._gameOfLife[y_new][x_new].die()
    return goL


#dimension is set and goL created
dimension = 4
goL = GameOfLife(dimension)
timesint = 1
#rectangle width for plotting is calculated
width = 1.0/goL._dimension
#canvas is initalized
figure   = pl.figure()
ax       = figure.add_subplot(111, aspect = 'equal')

pl.subplots_adjust(bottom=0.2)

pl.xlim(0,1) # anpassen der x-Grenzen
pl.ylim(0,1) # anpassen der y-Grenzen

#when a place on the canvas is clicked handleEvent is called, cells are plotted
figure.canvas.mpl_connect('button_press_event', handleEvent )
#axes for Buttons and sliders are set
startax = pl.axes([0.7, 0.01, 0.1, 0.075])
clearax = pl.axes([0.25, 0.01, 0.1, 0.075])
timesax = pl.axes([0.2, 0.1, 0.65, 0.03])
#Buttons and Slider are/is defined
start = Button(startax, 'Start', color = 'w', hovercolor = 'b')
clear = Button(clearax, 'Clear', color = 'w', hovercolor = 'b')
times = Slider(timesax, 'Iterations', 1, 100)
#methods to be called in event of clicking are assigned
start.on_clicked(goL.start)

clear.on_clicked(goL.clear)
#times.on_changed(goL.start(int(times.val)))
#number of iterations is set to slider value

#goL = goL.update()

        
pl.show()

#if __name__ == '__main__':
#    
#    goL = GameOfLife(4) 
#    
#    goL.addCell(0,1)
#    goL.addCell(0,3)
#    goL.addCell(1,0)
#    goL.addCell(1,1)
#    goL.addCell(1,2)
#    goL.addCell(2,0)
#    goL.addCell(2,3)
#    goL.addCell(3,0)
#
#    goL = goL.iterate(4)
#    
#    goL2 = GameOfLife(100)
#    
#    for i in range(goL2._dimension):
#        for j in range(goL2._dimension):
#            goL2._gameOfLife[i + 1][j + 1]._state = np.random.random_integers(0,1)
#    
#    for i in range(100):
#        pl.ion()
#        goL2 = goL2.iterateOnce()
#        goL2.plot()
#        pl.show()
#        pl.pause(1)
#        pl.close()
    
        
    
    