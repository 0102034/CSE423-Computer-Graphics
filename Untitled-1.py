from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_pos = (0, 0, 1000)
fovY = 60
GRID_LENGTH = 600
rand_var = 423

# Level selection variable
current_level = 0  # 0 for homepage

# Animation variables
time = 0.0

# Planet data: (radius, primary_color, secondary_color, level, name)
planets = [
    (30, (1.0, 1.0, 1.0), (0.5, 0.5, 0.5), 1, "Mercury"),  # White + Ash
    (40, (1.0, 0.9, 0.0), (0.5, 0.0, 0.0), 2, "Venus"),   # Yellow + Maroon
    (45, (0.0, 0.3, 1.0), (0.0, 0.8, 0.0), 3, "Earth"),   # Blue + Green
    (35, (0.8, 0.6, 0.4), None, 4, "Mars"),               # Faded brown
    (60, (0.8, 0.8, 1.0), (0.6, 0.4, 0.2), 5, "Jupiter"), # Blueish white + Brown
    (55, (0.9, 0.8, 0.6), (0.8, 0.7, 0.4), 6, "Saturn"),  # Sand + Lighter sand
    (50, (0.4, 0.7, 0.9), None, 7, "Uranus"),             # Light blue
    (50, (0.0, 0.4, 0.8), None, 8, "Neptune"),            # Ocean blue
]

# Sun data: (position, radius, color)
sun = ((0, 0, 0), 100, (1.0, 0.7, 0.0))  # Bright orangish-yellow

# Random star positions (x, y, z, blink_offset)
stars = [(random.uniform(-1500, 1500), random.uniform(-1500, 1500), random.uniform(-2000, -200), random.uniform(0, 2*math.pi)) for _ in range(100)]

# Asteroid data: (x, y, z, vx, vy, vz, radius)
asteroids = []

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_clock(x, y, size):
    glColor3f(1.0, 0.0, 1.0)  # Bright magenta
    # Draw circle
    glBegin(GL_LINE_LOOP)
    for i in range(20):
        angle = i * (2 * math.pi / 20)
        glVertex2f(x + size * math.cos(angle), y + size * math.sin(angle))
    glEnd()
    # Draw hour hand (shorter)
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + size * 0.5 * math.cos(math.pi / 4), y + size * 0.5 * math.sin(math.pi / 4))
    glEnd()
    # Draw minute hand (longer)
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + size * 0.8 * math.cos(0), y + size * 0.8 * math.sin(0))
    glEnd()

def draw_skull(x, y, size):
    glColor3f(0.0, 1.0, 0.0)  # Neon green
    # Draw skull outline (rounded top, square jaw)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x - size, y - size * 0.5)  # Bottom left
    glVertex2f(x - size, y + size * 0.5)  # Top left
    glVertex2f(x - size * 0.5, y + size)  # Top left curve
    glVertex2f(x + size * 0.5, y + size)  # Top right curve
    glVertex2f(x + size, y + size * 0.5)  # Top right
    glVertex2f(x + size, y - size * 0.5)  # Bottom right
    glEnd()
    # Draw eye sockets
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x - size * 0.4, y + size * 0.2)
    glVertex2f(x + size * 0.4, y + size * 0.2)
    glEnd()

def draw_infinity(x, y, size):
    glColor3f(0.0, 1.0, 1.0)  # Cyan
    # Draw infinity symbol using lemniscate curve
    glBegin(GL_LINE_STRIP)
    for t in range(0, 101):
        theta = t * 2 * math.pi / 100
        scale = size / math.sqrt(2)
        px = x + scale * math.cos(theta) / (1 + math.sin(theta) ** 2)
        py = y + scale * math.sin(theta) * math.cos(theta) / (1 + math.sin(theta) ** 2)
        glVertex2f(px, py)
    glEnd()

def draw_shapes():
    glPushMatrix()
    # Draw sun
    sun_pos, sun_radius, sun_color = sun
    glPushMatrix()
    glTranslatef(*sun_pos)
    quad = gluNewQuadric()
    glColor3f(*sun_color)
    gluSphere(quad, sun_radius, 20, 20)
    glPopMatrix()

    # Draw planets in circular ring, Mercury at top
    radius_circle = 300
    for i, (radius, primary_color, secondary_color, level, name) in enumerate(planets):
        angle = i * (360 / 8)  # 0° for Mercury, 45° for Venus, ..., 315° for Neptune
        x = radius_circle * math.cos(math.radians(angle))
        y = radius_circle * math.sin(math.radians(angle))
        z = 0
        glPushMatrix()
        glTranslatef(x, y, z)
        quad = gluNewQuadric()
        glColor3f(*primary_color)
        gluSphere(quad, radius, 20, 20)
        if secondary_color:
            glPushMatrix()
            glRotatef(90, 1, 0, 0)
            glColor3f(*secondary_color)
            gluPartialDisk(quad, radius-1, radius, 20, 20, 0, 360)
            glPopMatrix()
        glPopMatrix()
    glPopMatrix()

def keyboardListener(key, x, y):
    if key == b'\x1b':
        glutLeaveMainLoop()

def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    if key == GLUT_KEY_LEFT:
        x = max(-1000, x - 20)
    if key == GLUT_KEY_RIGHT:
        x = min(1000, x + 20)
    if key == GLUT_KEY_UP:
        y = min(1000, y + 20)
    if key == GLUT_KEY_DOWN:
        y = max(-1000, y - 20)
    camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    pass

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 5000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x, y, z = camera_pos
    gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)

def idle():
    global time, asteroids
    time += 0.05
    # Update asteroid positions
    new_asteroids = []
    for x, y, z, vx, vy, vz, radius in asteroids:
        x += vx
        y += vy
        z += vz
        # Remove if out of bounds
        if abs(x) <= 1000 and abs(y) <= 1000 and -500 <= z <= -100:
            new_asteroids.append((x, y, z, vx, vy, vz, radius))
    # Randomly spawn new asteroid (1% chance, if < 3)
    if len(new_asteroids) < 3 and random.random() < 0.01:
        new_asteroids.append((
            random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-500, -100),
            random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1),
            random.uniform(5, 10)
        ))
    asteroids = new_asteroids
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()

    # Draw stars
    glDisable(GL_LIGHTING)
    glDepthMask(GL_FALSE)
    glPointSize(3)
    glBegin(GL_POINTS)
    for x, y, z, offset in stars:
        intensity = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(time + offset))
        glColor3f(intensity, intensity, intensity)
        glVertex3f(x, y, z)
    glEnd()
    glDepthMask(GL_TRUE)
    glEnable(GL_LIGHTING)

    # Enable lighting for planets, sun, asteroids
    glEnable(GL_LIGHT0)
    light_pos = (0, 0, 1000, 1)
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glEnable(GL_COLOR_MATERIAL)

    # Draw asteroids
    glPushMatrix()
    for x, y, z, _, _, _, radius in asteroids:
        glPushMatrix()
        glTranslatef(x, y, z)
        quad = gluNewQuadric()
        glColor3f(0.5, 0.5, 0.5)
        gluSphere(quad, radius, 10, 10)
        glPopMatrix()
    glPopMatrix()

    # Draw planets and sun
    if current_level == 0:
        draw_shapes()

    # Disable lighting for text and symbols
    glDisable(GL_LIGHTING)

    # Draw 2D text labels for menu
    draw_text(10, 770, "Career Mode", GLUT_BITMAP_HELVETICA_18)
    draw_text(10, 740, "Timed Run", GLUT_BITMAP_HELVETICA_18)
    draw_text(10, 710, "Boss Fight", GLUT_BITMAP_HELVETICA_18)
    draw_text(10, 680, "Endless", GLUT_BITMAP_HELVETICA_18)

    # Draw symbols beside menu labels
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    # Clock beside "Timed Run"
    draw_clock(120, 740, 10)
    # Skull beside "Boss Fight"
    draw_skull(130, 710, 10)
    # Infinity beside "Endless"
    draw_infinity(110, 680, 10)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHTING)
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Spaceship Battle")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()