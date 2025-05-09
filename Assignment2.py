from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
height, width= 500, 500
diamond_size = 20
catcher_width = 70
catcher_height = 10
catcher_x = width//2
catcher_y = 10
diamond_x = random.randint(50, width-50)
diamond_y = height-50
diamond_speed = 0.1
game_status = True
points = 0


def init():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_point(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def midPoint(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = (2 * dy) - dx
    dE = 2*dy
    dNE = 2*(dy-dx)
    x, y = x1, y1
    draw_point(x, y)
    while x < x2:
        if d < 0:
            d +=  dE
        else:
            d += dNE
            y += 1
        x += 1
    draw_point(x, y)

def findZones(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if (dx>0) and (dy>0):
            return 0
        elif (dx<0) and (dy>0):
            return 3
        elif (dx<0) and (dy<0):
            return 4
        elif (dx>0) and (dy>0):
            return 7
    else:
        if (dx>0) and (dy>0):
            return 1
        elif (dx<0) and (dy>0):
            return 2
        elif (dx<0) and (dy<0):
            return 5
        elif (dx<0) and (dy>0):
            return 6

def convertZone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone==1:
        return y, x
    elif zone==2:
        return y, -x
    elif zone==3:
        return -x, y
    elif zone==4:
        return -x, -y
    elif zone==5:
        return -y, -x
    elif zone==6:
        return -y, x
    elif zone==7:
        return x, -y

def convertOG(x, y, zone):
    if zone==0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_diamond(x, y, size):
    glColor3f(1.0, 0.8, 0.0)
    midPoint(x, y-size, x+size//2, y)
    midPoint(x+size//2, y, x, y+size//2)
    midPoint(x, y+size//2, x-size//2, y)
    midPoint(x-size//2, y, x, y-size//2)

def draw_catcher(x, height, width):
    if game_status:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(1.0, 0.0, 0.0)
    midPoint(x-catcher_width//2, catcher_width, x+catcher_width//100, catcher_width)
    midPoint(x-catcher_width//2, catcher_width+catcher_height, x+catcher_width//2, catcher_width+catcher_height)
    midPoint(x-catcher_width//2, catcher_width, x-catcher_width//2, catcher_height+catcher_width)
    midPoint(x+catcher_width//2, catcher_width, x+catcher_width//2, catcher_width+catcher_height)

def keyboardListener(key, x, y):
    global game_status
    if key == b"r":
        game_status = False
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global catcher_x
    if game_status:
        if key == GLUT_KEY_LEFT:
            catcher_x = max(50, catcher_x - 20)
        elif key == GLUT_KEY_RIGHT:
            catcher_x = min(width-50, catcher_x + 20)
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global game_status
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = height - y
        if y > (height-50) and (x<50):
            game_status = False
    glutPostRedisplay()

def updateStatus():
    global diamond_x, diamond_y, game_status, diamond_speed, points
    if game_status:
        diamond_y -=  diamond_speed
        if (diamond_y <= catcher_y+20):  #catcher
            points += 1
            diamond_speed += 0.01
            diamond_x = random.randint(50, width-50)
            diamond_y = height - 50
            print(f"Score: {points}")
    elif (diamond_y <= 0):
            game_status = False
            print(f"Game over!/nScore: {points}")
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    init()
    draw_diamond(diamond_x, diamond_y, diamond_size)
    draw_catcher(catcher_x, 10, 100)
    #call the draw methods here
    glColor3f(1.0, 1.0, 0.0)
    midPoint(10, height-20, 20, height-30)
    midPoint(10, height - 20, 20, height - 10)
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"LabAssignment2") #window name
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(updateStatus)
glutMainLoop()