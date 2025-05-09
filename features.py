current_weapon = 0
weapon_color = (1.0, 0.0, 0.0)
boss_gear_color = (0.2, 0.4, 0.2)
start_time = 0
def draw_BIG_BOSS():
    glPushMatrix()
    glTranslatef(200, 200, 0)

    #body
    glColor3f(*boss_gear_color)  # military gear color
    glutSolidCube(80)


    #head
    glPushMatrix()
    glTranslatef(0, 0, 60) #head position
    glColor3f(0.8, 0.6, 0.4)
    glutSolidSphere(25, 10, 10)

    #Helmet
    glColor3f(0.3, 0.5, 0.2) # dark green
    glTranslatef(0, 0, 15)
    glutSolidSphere(28, 12, 12)
    glPopMatrix()

    #legs
    glColor3f(*boss_gear_color)
    glPushMatrix()
    glTranslatef(-20, 0, -60)
    glutSolidCube(30) #left
    glTranslatef(40, 0, 0)
    glutSolidCube(30) #right
    glPopMatrix()

    #arms
    glColor3f(*boss_gear_color)
    #left
    glPushMatrix()
    glTranslatef(-50, 0, 20)
    glRotatef(-30, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 15, 10, 70, 10, 10)
    glPopMatrix()
    #right
    glPushMatrix()
    glTranslatef(60, 0, 20)
    glRotatef(30, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 15, 10, 70, 10, 10)
    glPopMatrix()

    #boots
    glColor3f(0.4, 0.3, 0.1)
    glPushMatrix()
    glTranslatef(-20, 0, -90)
    glutSolidCube(35) #left boot
    glTranslatef(40, 0, 0)
    glutSolidCube(35) #right boot
    glPopMatrix()

    #belt
    glColor3f(0.4, 0.3, 0.1)
    glPushMatrix()
    glTranslatef(0, 0, -20)
    glutSolidCube(50)
    glPopMatrix()

    #wielding weapon
    glPushMatrix()
    glTranslatef(60, 0, 20)
    glColor3f(0.3, 0.3, 0.3)  # metal color
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 8, 8, 50, 10, 10) #barrel
    glTranslatef(0, 0, 50)
    glutSolidSphere(10, 10, 10) #gun tip
    glPopMatrix()

    glPopMatrix()

def draw_weapon():
    glPushMatrix()
    glTranslatef(-200, -200, 0)
    #var value
    #basic weapon: pistol
    if current_weapon == 0:
        glColor3f(*weapon_color)  # metal color
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 8, 8, 50, 10, 10)  # barrel
        glTranslatef(0, 0, 50)
        glutSolidSphere(10, 10, 10)  # gun tip
        glTranslatef(-45, 0, 0)
        glTranslatef(-10, 0, 0)
        glutSolidCube(25) #handle

    #weapon2: rifle
    elif current_weapon == 1:
        glColor3f(*weapon_color)  # metal color
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 10, 100, 10, 10)  # barrel
        glTranslatef(0, 0, 100)
        glutSolidSphere(12, 10, 10)  # gun tip
        glTranslatef(-90, 0, 0)
        glTranslatef(-20, 0, 0)
        glutSolidCube(30)  # handle

    #shotgun
    elif current_weapon == 2:
        glColor3f(*weapon_color)  # metal color
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 15, 15, 70, 10, 10)  # barrel
        glTranslatef(0, 0, 70)
        glutSolidSphere(15, 10, 10)  # gun tip
        glTranslatef(-80, 0, 0)
        glTranslatef(-25, 0, 0)
        glutSolidCube(35)  # handle

    glPopMatrix()

def keyboardListener(key, x, y):
    global current_weapon, weapon_color, boss_gear_color
    #weapon change
    if key == b'1':
        current_weapon = 0
        weapon_color = (0.0, 0.0, 0.0) #black
    elif key == b'2':
        current_weapon = 1
        weapon_color = (0.6, 0.2, 0.0)  #burnt brick
    elif key == b'3':
        current_weapon = 2
        weapon_color = (0.2, 0.2, 0.2)  #gunmetal

    #big boss's gear color change
    if key == b'q':   #c booked for cheat mode
        if boss_gear_color == (0.2, 0.4, 0.2):
            boss_gear_color = (0.0, 0.0, 0.0)
        elif boss_gear_color == (0.0, 0.0, 0.0):
            boss_gear_color = (0.7, 0.7, 0.7)
        else:
            boss_gear_color = (0.2, 0.4, 0.2)

    # # Reset the game if R key is pressed
    if key == b'r':
        current_weapon = 0
        weapon_color = (0.0, 0.0, 0.0) #pistol
        boss_gear_color = (0.2, 0.4, 0.2)  #initial gear color (military green)

def mouseListener(button, state, x, y):
    global game_start, start_time
    # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_start:
        game_start = True
        start_time = time.time()

    # # Right mouse button toggles camera tracking mode
    #if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN: