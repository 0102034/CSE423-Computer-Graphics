from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# def draw_triangles():
#     glBegin(GL_TRIANGLES)
#     # floor
#     glColor3f(0.8, 0.52, 0.07)
#     glVertex2f(0, 350) #1
#     glVertex2f(0,0)
#     glVertex2f(500, 0)
#     glVertex2f(0, 350) #2
#     glVertex2f(500, 350)
#     glVertex2f(500, 0)
#     #triangles
#     glColor3f(0, 0.5, 0)
#     glVertex2f(0, 280) #1
#     glVertex2f(50, 280)
#     glVertex2f(25, 340)
#     glVertex2f(50, 280) #2
#     glVertex2f(100, 280)
#     glVertex2f(75, 340)
#     glVertex2f(100, 280) #3
#     glVertex2f(150, 280)
#     glVertex2f(125, 340)
#     glVertex2f(350, 280) #4
#     glVertex2f(400, 280)
#     glVertex2f(375, 340)
#     glVertex2f(400, 280) #5
#     glVertex2f(450, 280)
#     glVertex2f(425, 340)
#     glVertex2f(450, 280) #6
#     glVertex2f(500, 280)
#     glVertex2f(475, 340)
#     #house
#     glColor3f(1.0, 1.0, 1.0)
#     glVertex2f(150, 200)
#     glVertex2f(350, 200)
#     glVertex2f(150, 300)
#     glVertex2f(150, 300)
#     glVertex2f(350, 300)
#     glVertex2f(350, 200)
#     glColor3f(0.0, 0.0, 1.0)
#     glVertex2f(120, 300)
#     glVertex2f(375, 300)
#     glVertex2f(250, 375)
#     #door
#     glColor3f(0.2, 0.4, 1)
#     glVertex2f(233, 200)
#     glVertex2f(233, 267)
#     glVertex2f(267, 200)
#     glVertex2f(233, 267)
#     glVertex2f(267, 200)
#     glVertex2f(267, 267)
#     #left window
#     glColor3f(0, 0, 1)
#     glVertex2f(180, 240) #1
#     glVertex2f(180, 265)
#     glVertex2f(205, 240)
#     glVertex2f(180, 265) #2
#     glVertex2f(205, 265)
#     glVertex2f(205, 240)
#     #right window
#     glColor3f(0, 0, 1)
#     glVertex2f(295, 265) #1
#     glVertex2f(295, 240)
#     glVertex2f(320, 240)
#     glVertex2f(295, 265) #2
#     glVertex2f(320, 265)
#     glVertex2f(320, 240)
#     glEnd()
#
# def draw_points():
#     #doorKnob
#     glPointSize(10) #pixel size. by default 1 thake
#     glBegin(GL_POINTS)  #shapes that needs to be drawn (name always in capitals and "s" at the end)
#     glColor3f(0,0,0)
#     glVertex2f(258, 243) #jekhane show korbe pixel #coordinate of where we are drawing
#     glEnd()
#
#
# def draw_lines():
#     glBegin(GL_LINES)
#     #window left
#     # window cross
#     glColor3f(0, 0, 0)
#     glVertex2f(180, 252.5)
#     glVertex2f(205, 252.5)
#     glVertex2f(192.5, 240)
#     glVertex2f(192.5, 265)
#     # window right
#     # window cross
#     glColor3f(0, 0, 0)
#     glVertex2f(295, 252.5)
#     glVertex2f(320, 252.5)
#     glVertex2f(307.5, 240)
#     glVertex2f(307.5, 265)
#     glEnd()
#
# def iterate():
#     glViewport(0, 0, 500, 500) #width & height same as window(line35)[creates vessels and controls the size of screen]
#     glMatrixMode(GL_PROJECTION) #after mid (syntax for now)
#     glLoadIdentity() #after mid
#     glOrtho(0.0, 500, 0.0,500, 0.0, 1.0) #sets up axis (left n right = x axis(starts from 0, ends to 500)(bottom n top = y axis(starts from 0, ends to 500)) [znear/zfar = z axis (3D]
#     glMatrixMode (GL_MODELVIEW)
#     glLoadIdentity()
#
# def showScreen():   #will do drawing related works here
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()
#     glColor3f(0.1, 0.6, 1.0) #setting colors(RGB)
#     #call the draw methods here
#     draw_triangles()
#     draw_points()
#     draw_lines()
#     glutSwapBuffers()
#
#
# glutInit()   #function call
# glutInitDisplayMode(GLUT_RGBA)     #colorful background
# glutInitWindowSize(500, 500) #window size (program window)
# glutInitWindowPosition(0, 0) #program window opens from top left with this(0,0)value[x value=100pixel right, y value=200pixel down]
# wind = glutCreateWindow(b"CSE423LAB1") #window name (the output window)
# glutDisplayFunc(showScreen)    #glut/gl = OpenGL functions (otherwise the functions we wrote)
# glutMainLoop() #keeps the program running (like the printed program value but keeps running in a loop)
#

#TASK2
import random
from OpenGL.GL import *
from OpenGL.GLUT import *

def draw_points(x, y):
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def mouseListen():
def keyboardlisten():



def iterate():
     glViewport(0, 0, 500, 500) #width & height same as window(line35)[creates vessels and controls the size of screen]
     glMatrixMode(GL_PROJECTION) #after mid (syntax for now)
     glLoadIdentity() #after mid
     glOrtho(0.0, 500, 0.0,500, 0.0, 1.0) #sets up axis (left n right = x axis(starts from 0, ends to 500)(bottom n top = y axis(starts from 0, ends to 500)) [znear/zfar = z axis (3D]
     glMatrixMode (GL_MODELVIEW)
     glLoadIdentity()

def showScreen():   #will do drawing related works here
     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
     glLoadIdentity()
     iterate()
     glColor3f(0.1, 0.6, 1.0) #setting colors(RGB)
     #call the draw methods here

     for i in range(50):
         x = random.uniform(0, 500)
         y = random.uniform(0, 500)
         draw_points(x, y)
     keyboardlisten()
     glutSwapBuffers()

glutInit()   #function call
glutInitDisplayMode(GLUT_RGBA)     #colorful background
glutInitWindowSize(500, 500) #window size (program window)
glutInitWindowPosition(0, 0) #program window opens from top left with this(0,0)value[x value=100pixel right, y value=200pixel down]
wind = glutCreateWindow(b"CSE423LAB1") #window name (the output window)
glutDisplayFunc(showScreen)    #glut/gl = OpenGL functions (otherwise the functions we wrote)
glutMainLoop()

