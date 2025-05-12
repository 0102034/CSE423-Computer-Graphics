from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import sys
import time as sys_time

# Window dimensions
width, height = 1000, 800

# Camera-related variables
camera_pos = (0, 0, 1000)  # Homepage
fovY = 60  # Homepage
fovY_mode = 45  # Modes 1, 2, 3, 4
GRID_LENGTH = 600  # For homepage asteroids
rand_var = 423
camera_pos_mode = (0, 0, 5)

# Mode selection
current_mode = 0  # 0: Homepage, 1: Career, 2: Timed, 3: Boss, 4: Endless
current_level = 1  # Career mode level (1 to 8)
level_cleared = 0
is_3d_mode = True  # Toggle between 3D and 2D
alt_toggle_cooldown = 0.0  # Cooldown for toggle

# Animation
time = 0.0
frame_count = 0  # For debug
timer = 3600.0  # 60 minutes for Timed Run
alien_bullet_timer = 0.0  # For level 8 alien bullets

# Spaceship
x_pos, y_pos, z_pos = 0, 0, 0
rotation_angle = 0  # Yaw in degrees

# Bullets: [(x, y, z), (dx, dy, dz), is_rocket]
bullets = []
bullet_speed = 0.15
unlimited_bullets = False  # Cheat code toggle

# Boss
boss_active = False  # For even levels in Career Mode
boss_pos = [0, 0, 0]
boss_bullets = []  # [(x, y, z), (dx, dy, dz), bounce_count]
alien_bullets = []  # For level 8: [(x, y, z), (dx, dy, dz), bounce_count]
boss_health = 100
boss_bullet_timer = 0.0

# Game state
game_over = False
health = 5
alien_kill_count = 0
aliens_goal = 200

# Aliens: [(x, y, z), alive]
aliens = []

# Flame colors
flame_colors = [
    (1.0, 0.3, 0.0), (1.0, 0.5, 0.0), (1.0, 0.6, 0.1),
    (1.0, 1.0, 0.0), (0.0, 1.0, 0.5), (0.5, 0.0, 1.0)
]
current_flame_color = 0

# Planets: (radius, primary_color, secondary_color, level, name)
planets = [
    (30, (1.0, 1.0, 1.0), (0.5, 0.5, 0.5), 1, "Mercury"),
    (40, (1.0, 0.9, 0.0), (0.5, 0.0, 0.0), 2, "Venus"),
    (45, (0.0, 0.3, 1.0), (0.0, 0.8, 0.0), 3, "Earth"),
    (35, (0.8, 0.6, 0.4), None, 4, "Mars"),
    (60, (0.8, 0.8, 1.0), (0.6, 0.4, 0.2), 5, "Jupiter"),
    (55, (0.9, 0.8, 0.6), (0.8, 0.7, 0.4), 6, "Saturn"),
    (50, (0.4, 0.7, 0.9), None, 7, "Uranus"),
    (50, (0.0, 0.4, 0.8), None, 8, "Neptune"),
]

# Sun
sun = ((0, 0, 0), 100, (1.0, 0.7, 0.0))

# Star colors
star_colors = [
    (1.0, 1.0, 0.6),  # Light yellow
    (0.9, 0.95, 1.0),  # Ice white
    (0.6, 0.8, 1.0),  # Light blue
    (0.8, 0.6, 1.0),  # Light purple
]

# Stars: (x, y, z, blink_offset, color_idx)
stars = [(random.uniform(-1500, 1500), random.uniform(-1500, 1500), random.uniform(-2000, -200), random.uniform(0, 2*math.pi), random.randint(0, len(star_colors)-1)) for _ in range(100)]

# Asteroids: (x, y, z, vx, vy, vz, radius)
asteroids = []

def init():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def init_mode():
    glClearColor(0.0, 0.0, 0.05, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    global health
    health = 5

def draw_cone(base_radius, height, slices, stacks):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, base_radius, 0, height, slices, stacks)
    gluDeleteQuadric(quad)

def draw_sphere(radius, slices, stacks):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def draw_bullets():
    glColor3f(1.0, 1.0, 0.0)
    for bullet, _, is_rocket in bullets:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], bullet[2])
        radius = 0.125 if is_rocket else 0.05
        glutSolidSphere(radius, 10, 10)
        glPopMatrix()

def draw_boss_bullets():
    glColor3f(1.0, 0.0, 0.0)
    for bullet, _, _ in boss_bullets:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], bullet[2])
        glutSolidSphere(0.08, 10, 10)
        glPopMatrix()

def draw_alien_bullets():
    glColor3f(1.0, 0.0, 0.0)
    for bullet, _, _ in alien_bullets:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], bullet[2])
        glutSolidSphere(0.08, 10, 10)
        glPopMatrix()

def draw_alien_sphere(x, y, z, r, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    glutSolidSphere(r, 32, 32)
    glPopMatrix()

def draw_alien_cone(x, y, z, height, base_radius, color, rot_x=0, rot_y=0, rot_z=0):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(rot_z, 0, 0, 1)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluCylinder(quad, base_radius, 0.0, height, 20, 10)
    gluDeleteQuadric(quad)
    glPopMatrix()

def draw_antenna(x_offset):
    head_top_y = 0.75 * 0.5
    antenna_base_y = head_top_y - 0.01
    glPushMatrix()
    glTranslatef(x_offset, antenna_base_y, 0.0)
    glColor3f(0.5, 0.0, 0.5)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, 0.04, 0.04, 0.45, 12, 5)
    gluDeleteQuadric(quad)
    glPopMatrix()
    draw_alien_sphere(x_offset, antenna_base_y + 0.45, 0.0, 0.08, (1.0, 0.2, 0.8))

def draw_mouth():
    glPushMatrix()
    glTranslatef(0, 0.1, 0.52)
    glColor3f(0.1, 0.1, 0.1)
    num_segments = 40
    radius_x = 0.18
    radius_y = 0.03
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, 0)
    for i in range(num_segments + 1):
        theta = 2.0 * math.pi * i / num_segments
        x = radius_x * math.cos(theta)
        y = radius_y * math.sin(theta)
        glVertex3f(x, y, 0)
    glEnd()
    glPopMatrix()

def draw_eye(x, y, z):
    draw_alien_sphere(x, y, z, 0.07, (0, 0, 0))
    draw_alien_sphere(x + 0.02, y + 0.02, z + 0.03, 0.02, (1, 1, 1))

def draw_alien(pos):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glScalef(0.5, 0.5, 0.5)
    glPushMatrix()
    glScalef(1.0, 1.5, 0.8)
    glColor3f(0.4, 0.8, 0.7)
    glutSolidSphere(0.5, 32, 32)
    glPopMatrix()
    draw_eye(0.15, 0.4, 0.45)
    draw_eye(-0.15, 0.4, 0.45)
    draw_mouth()
    draw_alien_sphere(0.5, 0.15, 0, 0.1, (0.2, 0.8, 0.6))
    draw_alien_cone(0.55, 0.15, 0.05, 0.1, 0.02, (1, 1, 1), -45)
    draw_alien_sphere(-0.5, 0.15, 0, 0.1, (0.2, 0.8, 0.6))
    draw_alien_cone(-0.55, 0.15, 0.05, 0.1, 0.02, (1, 1, 1), -45)
    draw_alien_sphere(0, -0.8, 0, 0.15, (0.2, 0.6, 0.6))
    draw_alien_cone(0.25, -0.85, 0.1, 0.1, 0.03, (1, 1, 1), -30)
    draw_alien_sphere(-0.2, -0.8, 0, 0.15, (0.2, 0.6, 0.6))
    draw_alien_cone(-0.25, -0.85, 0.1, 0.1, 0.03, (1, 1, 1), -30)
    draw_antenna(0.2)
    draw_antenna(-0.2)
    glPopMatrix()

def draw_boss_sphere(x, y, z, radius, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    glutSolidSphere(radius, 36, 36)
    glPopMatrix()

def draw_boss_ellipsoid(x, y, z, rx, ry, rz, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(rx, ry, rz)
    glColor3f(*color)
    glutSolidSphere(1.0, 36, 36)
    glPopMatrix()

def draw_boss_cylinder(x, y, z, height, base_radius, color, rot_x=0, rot_y=0, rot_z=0):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(rot_z, 0, 0, 1)
    glColor3f(*color)
    quad = gluNewQuadric()
    gluCylinder(quad, base_radius, base_radius * 0.7, height, 20, 10)
    gluDeleteQuadric(quad)
    glPopMatrix()

def draw_boss_eyes():
    eye_white_color = (1, 1, 1)
    pupil_color = (0, 0, 0)
    draw_boss_ellipsoid(-0.2, 0.45, 0.52, 0.22, 0.3, 0.1, eye_white_color)
    draw_boss_ellipsoid(0.2, 0.45, 0.52, 0.22, 0.3, 0.1, eye_white_color)
    draw_boss_ellipsoid(-0.2, 0.48, 0.58, 0.1, 0.15, 0.05, pupil_color)
    draw_boss_ellipsoid(0.2, 0.48, 0.58, 0.1, 0.15, 0.05, pupil_color)

def draw_boss_mouth():
    glPushMatrix()
    glTranslatef(0, 0.15, 0.6)
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_LINES)
    glVertex3f(-0.15, 0, 0)
    glVertex3f(0.15, 0, 0)
    glEnd()
    glPopMatrix()

def draw_boss_antennae():
    color = (0.6, 0.4, 0.8)
    draw_boss_cylinder(-0.2, 1.3, 0, 0.4, 0.03, color, -90, 0, 0)
    draw_boss_sphere(-0.2, 1.7, 0, 0.06, color)
    draw_boss_cylinder(0.2, 1.3, 0, 0.4, 0.03, color, -90, 0, 0)
    draw_boss_sphere(0.2, 1.7, 0, 0.06, color)

def draw_boss_alien():
    glPushMatrix()
    glTranslatef(boss_pos[0], boss_pos[1], boss_pos[2])
    glScalef(0.2, 0.2, 0.2)
    colors = [
        (0.6, 0.4, 0.8), (0.4, 0.8, 0.8), (0.8, 0.4, 0.8)
    ]
    color_idx = int(time * 2) % len(colors)
    color = colors[color_idx]
    draw_boss_ellipsoid(0, 0.5, 0, 0.7, 1.0, 0.65, color)
    draw_boss_cylinder(0, 0.0, 0, 0.3, 0.1, color, -90, 0, 0)
    draw_boss_ellipsoid(0, -0.6, 0, 0.7, 1.0, 0.5, color)
    draw_boss_cylinder(-0.75, -0.6, 0, 0.6, 0.08, color, 0, 0, 30)
    draw_boss_cylinder(0.75, -0.6, 0, 0.6, 0.08, color, 0, 0, -30)
    draw_boss_cylinder(-0.3, -1.6, 0, 0.9, 0.12, color, 0, 0, 5)
    draw_boss_cylinder(0.3, -1.6, 0, 0.9, 0.12, color, 0, 0, -5)
    draw_boss_antennae()
    draw_boss_eyes()
    draw_boss_mouth()
    glPopMatrix()

def draw_spaceship():
    global current_flame_color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init_mode()
    glViewport(0, 0, 1000, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY_mode, 1.25, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if is_3d_mode:
        theta = math.radians(rotation_angle)
        cam_x = x_pos - 3 * math.sin(theta)
        cam_y = y_pos - 3 * math.cos(theta)
        cam_z = z_pos + 1
        gluLookAt(cam_x, cam_y, cam_z, x_pos, y_pos, z_pos, 0, 0, 1)
    else:
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glPointSize(3)
    glBegin(GL_POINTS)
    if current_mode in [1, 2, 3, 4]:
        for x, y, z, offset, _ in stars:
            intensity = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(time + offset))
            glColor3f(intensity, intensity, intensity)
            glVertex3f(x, y, z)
    glEnd()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    draw_bullets()
    if current_mode == 3 or (current_mode == 1 and boss_active):
        draw_boss_bullets()
    if current_mode == 1 and current_level == 8:
        draw_alien_bullets()
    glPushMatrix()
    glTranslatef(x_pos, y_pos, z_pos)
    glRotatef(rotation_angle, 0, 0, 1)
    glColor3f(0.3, 0.7, 1.0)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    draw_cone(0.2, 0.8, 20, 20)
    glPopMatrix()
    glColor3f(0.0, 1.0, 0.9)
    glPushMatrix()
    glTranslatef(0, 0.3, 0)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()
    glColor3f(0.6, 0.3, 0.8)
    glPushMatrix()
    glTranslatef(-0.2, 0, 0)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(0, 0.1, 0.05)
    glVertex3f(-0.2, -0.1, 0.05)
    glVertex3f(0.1, -0.1, 0.05)
    glVertex3f(0.1, 0.1, 0.05)
    glNormal3f(0, 0, -1)
    glVertex3f(0, 0.1, -0.05)
    glVertex3f(-0.2, -0.1, -0.05)
    glVertex3f(0.1, -0.1, -0.05)
    glVertex3f(0.1, 0.1, -0.05)
    glNormal3f(0, 1, 0)
    glVertex3f(0, 0.1, 0.05)
    glVertex3f(0, 0.1, -0.05)
    glVertex3f(0.1, 0.1, -0.05)
    glVertex3f(0.1, 0.1, 0.05)
    glNormal3f(0, -1, 0)
    glVertex3f(-0.2, -0.1, 0.05)
    glVertex3f(-0.2, -0.1, -0.05)
    glVertex3f(0.1, -0.1, -0.05)
    glVertex3f(0.1, -0.1, 0.05)
    glEnd()
    glPopMatrix()
    glColor3f(0.8, 0.3, 0.6)
    glPushMatrix()
    glTranslatef(0.2, 0, 0)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(0, 0.1, 0.05)
    glVertex3f(0.2, -0.1, 0.05)
    glVertex3f(-0.1, -0.1, 0.05)
    glVertex3f(-0.1, 0.1, 0.05)
    glNormal3f(0, 0, -1)
    glVertex3f(0, 0.1, -0.05)
    glVertex3f(0.2, -0.1, -0.05)
    glVertex3f(-0.1, -0.1, -0.05)
    glVertex3f(-0.1, 0.1, -0.05)
    glNormal3f(0, 1, 0)
    glVertex3f(0, 0.1, 0.05)
    glVertex3f(0, 0.1, -0.05)
    glVertex3f(-0.1, 0.1, -0.05)
    glVertex3f(-0.1, 0.1, 0.05)
    glNormal3f(0, -1, 0)
    glVertex3f(0.2, -0.1, 0.05)
    glVertex3f(0.2, -0.1, -0.05)
    glVertex3f(-0.1, -0.1, -0.05)
    glVertex3f(-0.1, -0.1, 0.05)
    glEnd()
    glPopMatrix()
    r, g, b = flame_colors[current_flame_color]
    glColor3f(r, g, b)
    glPushMatrix()
    glTranslatef(0, -0.3, 0)
    glRotatef(-90, 1, 0, 0)
    draw_cone(0.05, 0.2 + random.uniform(0, 0.04), 10, 10)
    glPopMatrix()
    glPopMatrix()
    if current_mode in [1, 2, 4] and not boss_active:
        for pos, alive in aliens:
            if alive:
                draw_alien(pos)
    if current_mode == 3 or (current_mode == 1 and boss_active):
        draw_boss_alien()
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, 770, "Go Back", GLUT_BITMAP_HELVETICA_18)
    draw_text(10, 740, "Restart", GLUT_BITMAP_HELVETICA_18)
    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        draw_text(10, 710, "Game Over", GLUT_BITMAP_HELVETICA_18)
    if current_mode in [1, 2, 3, 4]:
        glColor3f(1.0, 1.0, 1.0)
        draw_text(10, 680, f"Aliens Defeated: {alien_kill_count}", GLUT_BITMAP_HELVETICA_18)
        if current_mode == 1:
            planet_name = planets[current_level-1][4]
            draw_text(10, 660, f"Level {current_level}: {planet_name}", GLUT_BITMAP_HELVETICA_18)
            if not boss_active:
                draw_text(10, 640, f"Aliens Left: {max(0, current_level * 10 - alien_kill_count)}", GLUT_BITMAP_HELVETICA_18)
        elif current_mode == 2:
            draw_text(10, 660, f"Aliens Left: {max(0, aliens_goal - alien_kill_count)}", GLUT_BITMAP_HELVETICA_18)
            minutes = int(timer // 60)
            seconds = int(timer % 60)
            draw_text(10, 640, f"Time: {minutes:02d}:{seconds:02d}", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 620, f"Health: {health}", GLUT_BITMAP_HELVETICA_18)
        if current_mode == 3 or (current_mode == 1 and boss_active):
            draw_text(10, 600, f"Boss Health: {boss_health}", GLUT_BITMAP_HELVETICA_18)
    glEnable(GL_LIGHTING)
    glutSwapBuffers()

def update_flame(value):
    global current_flame_color
    current_flame_color = (current_flame_color + 1) % len(flame_colors)
    glutPostRedisplay()
    glutTimerFunc(100, update_flame, 0)

def spawn_alien():
    while True:
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(-10, 10) if is_3d_mode else -5
        dist = math.sqrt((x - x_pos)**2 + (y - y_pos)**2 + (z - z_pos)**2)
        if dist > 3:
            break
    pos = [x, y, z]
    return [pos, True]

def spawn_boss():
    global boss_pos, boss_health, boss_bullets, boss_bullet_timer
    boss_health = 100
    boss_bullets = []
    boss_bullet_timer = 0.0
    if is_3d_mode:
        boss_pos = [random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)]
    else:
        boss_pos = [random.uniform(-10, 10), random.uniform(-10, 10), -5]
    print(f"Frame {frame_count}: Spawned boss at {boss_pos}")

def update_bullets(value):
    global bullets, aliens, alien_kill_count, boss_health, game_over, boss_active, current_mode, level_cleared
    new_bullets = []
    for pos, dir, is_rocket in bullets:
        new_pos = [
            pos[0] + dir[0] * bullet_speed,
            pos[1] + dir[1] * bullet_speed,
            pos[2] + dir[2] * bullet_speed
        ]
        hit = False
        if current_mode in [1, 2, 4] and not boss_active:
            for i, (alien_pos, alive) in enumerate(aliens):
                if alive:
                    dist = math.sqrt(
                        (new_pos[0] - alien_pos[0])**2 +
                        (new_pos[1] - alien_pos[1])**2 +
                        (new_pos[2] - alien_pos[2])**2 if is_3d_mode else 0
                    )
                    if dist < 0.75:
                        aliens[i][1] = False
                        aliens[i] = spawn_alien()
                        alien_kill_count += 1
                        hit = True
                        break
        elif current_mode == 3 or (current_mode == 1 and boss_active):
            dist = math.sqrt(
                (new_pos[0] - boss_pos[0])**2 +
                (new_pos[1] - boss_pos[1])**2 +
                (new_pos[2] - boss_pos[2])**2
            )
            if dist < 1.0:
                boss_health -= 5 if is_rocket else 1
                hit = True
                if boss_health <= 0 and current_mode == 3:
                    game_over = True
                    alien_kill_count += 1
                elif boss_health <= 0 and current_mode == 1:
                    boss_active = False
                    alien_kill_count = 0
                    current_level += 1
                    if current_level > 8:
                        current_mode = 0
                        level_cleared = 8
                        aliens = []
                        print(f"Frame {frame_count}: Completed Career Mode, returned to homepage")
                    else:
                        alien_count = int(3 + (current_level - 1) * (7 / 7))
                        aliens = [spawn_alien() for _ in range(alien_count)]
                        print(f"Frame {frame_count}: Defeated boss, advanced to level {current_level}")
        if not hit and all(-10 <= new_pos[i] <= 10 for i in range(3)):
            new_bullets.append((new_pos, dir, is_rocket))
    bullets = new_bullets
    glutPostRedisplay()
    glutTimerFunc(33, update_bullets, 0)

def update_boss_bullets(value):
    global boss_bullets, boss_bullet_timer, health, game_over
    if (current_mode == 3 or (current_mode == 1 and boss_active)) and not game_over:
        boss_bullet_timer += 0.033
        if boss_bullet_timer >= 2.0:
            boss_bullet_timer = 0.0
            dx = x_pos - boss_pos[0]
            dy = y_pos - boss_pos[1]
            dz = z_pos - boss_pos[2] if is_3d_mode else 0
            dist = math.sqrt(dx**2 + dy**2 + (dz**2 if is_3d_mode else 0))
            if dist > 0:
                dx, dy, dz = dx/dist, dy/dist, dz/dist if is_3d_mode else 0
            else:
                dx, dy, dz = 0, 1, 0
            boss_bullets.append(([boss_pos[0], boss_pos[1], boss_pos[2]], [dx, dy, dz], 0))
            print(f"Frame {frame_count}: Spawned boss bullet at {boss_pos}")
        new_bullets = []
        for pos, dir, bounce_count in boss_bullets:
            new_pos = [
                pos[0] + dir[0] * 0.06,
                pos[1] + dir[1] * 0.06,
                pos[2] + dir[2] * 0.06
            ]
            new_dir = dir[:]
            new_bounce = bounce_count
            if new_pos[0] <= -10 or new_pos[0] >= 10:
                new_dir[0] = -new_dir[0]
                new_bounce += 1
            if new_pos[1] <= -10 or new_pos[1] >= 10:
                new_dir[1] = -new_dir[1]
                new_bounce += 1
            if is_3d_mode and (new_pos[2] <= -10 or new_pos[2] >= 10):
                new_dir[2] = -new_dir[2]
                new_bounce += 1
            if new_bounce <= 2:
                dist = math.sqrt(
                    (new_pos[0] - x_pos)**2 +
                    (new_pos[1] - y_pos)**2 +
                    (new_pos[2] - z_pos)**2 if is_3d_mode else 0
                )
                print(f"Frame {frame_count}: Boss bullet at {new_pos}, spaceship at [{x_pos}, {y_pos}, {z_pos}], dist: {dist}")
                if dist < 1.0 and not game_over:
                    health -= 1
                    print(f"Frame {frame_count}: Health decreased to {health} due to boss bullet hit")
                    if health <= 0:
                        game_over = True
                else:
                    if all(-10 <= new_pos[i] <= 10 for i in range(3)):
                        new_bullets.append((new_pos, new_dir, new_bounce))
        boss_bullets = new_bullets
    glutPostRedisplay()
    glutTimerFunc(33, update_boss_bullets, 0)

def update_alien_bullets(value):
    global alien_bullets, health, game_over
    if current_mode == 1 and current_level == 8 and not game_over and not boss_active:
        global alien_bullet_timer
        alien_bullet_timer += 0.033
        if alien_bullet_timer >= 5.0:
            alien_bullet_timer = 0.0
            for pos, alive in aliens:
                if alive:
                    dx = x_pos - pos[0]
                    dy = y_pos - pos[1]
                    dz = z_pos - pos[2] if is_3d_mode else 0
                    dist = math.sqrt(dx**2 + dy**2 + (dz**2 if is_3d_mode else 0))
                    if dist > 0:
                        dx, dy, dz = dx/dist, dy/dist, dz/dist if is_3d_mode else 0
                    else:
                        dx, dy, dz = 0, 1, 0
                    alien_bullets.append((pos[:], [dx, dy, dz], 0))
                    print(f"Frame {frame_count}: Spawned alien bullet at {pos}")
        new_bullets = []
        for pos, dir, bounce_count in alien_bullets:
            new_pos = [
                pos[0] + dir[0] * 0.06,
                pos[1] + dir[1] * 0.06,
                pos[2] + dir[2] * 0.06
            ]
            new_dir = dir[:]
            new_bounce = bounce_count
            if new_pos[0] <= -10 or new_pos[0] >= 10:
                new_dir[0] = -new_dir[0]
                new_bounce += 1
            if new_pos[1] <= -10 or new_pos[1] >= 10:
                new_dir[1] = -new_dir[1]
                new_bounce += 1
            if is_3d_mode and (new_pos[2] <= -10 or new_pos[2] >= 10):
                new_dir[2] = -new_dir[2]
                new_bounce += 1
            if new_bounce <= 2:
                dist = math.sqrt(
                    (new_pos[0] - x_pos)**2 +
                    (new_pos[1] - y_pos)**2 +
                    (new_pos[2] - z_pos)**2 if is_3d_mode else 0
                )
                print(f"Frame {frame_count}: Alien bullet at {new_pos}, spaceship at [{x_pos}, {y_pos}, {z_pos}], dist: {dist}")
                if dist < 1.0 and not game_over:
                    health -= 1
                    print(f"Frame {frame_count}: Health decreased to {health} due to alien bullet hit")
                    if health <= 0:
                        game_over = True
                else:
                    if all(-10 <= new_pos[i] <= 10 for i in range(3)):
                        new_bullets.append((new_pos, new_dir, new_bounce))
        alien_bullets = new_bullets
    glutPostRedisplay()
    glutTimerFunc(33, update_alien_bullets, 0)

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
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
    glColor3f(1.0, 0.0, 1.0)
    glBegin(GL_LINE_LOOP)
    for i in range(20):
        angle = i * (2 * math.pi / 20)
        glVertex2f(x + size * math.cos(angle), y + size * math.sin(angle))
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + size * 0.5 * math.cos(math.pi / 4), y + size * 0.5 * math.sin(math.pi / 4))
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + size * 0.8 * math.cos(0), y + size * 0.8 * math.sin(0))
    glEnd()

def draw_skull(x, y, size):
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINE_LOOP)
    glVertex3f(x - size, y - size * 0.5, 0)
    glVertex3f(x - size, y + size * 0.5, 0)
    glVertex3f(x - size * 0.5, y + size, 0)
    glVertex3f(x + size * 0.5, y + size, 0)
    glVertex3f(x + size, y + size * 0.5, 0)
    glVertex3f(x + size, y - size * 0.5, 0)
    glEnd()
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex3f(x - size * 0.4, y + size * 0.2, 0)
    glVertex3f(x + size * 0.4, y + size * 0.2, 0)
    glEnd()

def draw_infinity(x, y, size):
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_LINE_STRIP)
    for t in range(0, 101):
        theta = t * 2 * math.pi / 100
        scale = size / math.sqrt(2)
        px = x + scale * math.cos(theta) / (1 + math.sin(theta) ** 2)
        py = y + scale * math.sin(theta) * math.cos(theta) / (1 + math.sin(theta) ** 2)
        glVertex2f(px, py)
    glEnd()

def draw_planets_and_sun():
    glPushMatrix()
    sun_pos, sun_radius, sun_color = sun
    glPushMatrix()
    glTranslatef(*sun_pos)
    quad = gluNewQuadric()
    glColor3f(*sun_color)
    gluSphere(quad, sun_radius, 20, 20)
    glPopMatrix()
    radius_circle = 300
    for i, (radius, primary_color, secondary_color, level, name) in enumerate(planets):
        angle = i * (360 / 8)
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

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if current_mode == 0:
        gluPerspective(fovY, 1.25, 0.1, 5000)
    else:
        gluPerspective(fovY_mode, 1.25, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if current_mode == 0:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)

def restart_mode():
    global x_pos, y_pos, z_pos, rotation_angle, bullets, game_over, health, aliens, alien_kill_count, fovY_mode, timer, boss_pos, boss_bullets, boss_health, boss_bullet_timer, alien_bullets, alien_bullet_timer, current_level, unlimited_bullets, boss_active
    x_pos, y_pos, z_pos = 0, 0, -5 if not is_3d_mode else 0
    rotation_angle = 0
    bullets = []
    boss_bullets = []
    alien_bullets = []
    game_over = False
    health = 5
    alien_kill_count = 0
    fovY_mode = 45
    unlimited_bullets = False
    boss_active = False
    if current_mode == 1:
        current_level = 1
        alien_count = int(3 + (current_level - 1) * (7 / 7))
        aliens = [spawn_alien() for _ in range(alien_count)]
        alien_bullet_timer = 0.0
    elif current_mode in [2, 4]:
        aliens = [spawn_alien() for _ in range(5)]
        timer = 3600.0 if current_mode == 2 else 0.0
    else:  # Mode 3
        aliens = []
        timer = 0.0
        spawn_boss()
    print(f"Frame {frame_count}: Restarted mode {current_mode}, level {current_level}, health: {health}, aliens: {len(aliens)}")
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global fovY, fovY_mode, x_pos, y_pos, z_pos, bullets, game_over, rotation_angle, is_3d_mode, alt_toggle_cooldown, unlimited_bullets
    try:
        key = key.decode("utf-8").lower()
    except:
        if key == b'\x1b':
            glutLeaveMainLoop()
        return
    current_time = sys_time.time()
    if key == 't' and current_mode in [1, 2, 3, 4] and current_time >= alt_toggle_cooldown:
        is_3d_mode = not is_3d_mode
        alt_toggle_cooldown = current_time + 0.5
        if not is_3d_mode:
            z_pos = -5
            if current_mode == 3 or (current_mode == 1 and boss_active):
                boss_pos[2] = -5
            for pos, _ in aliens:
                pos[2] = -5
        print(f"Frame {frame_count}: Switched to {'3D' if is_3d_mode else '2D'} mode, pos: [{x_pos}, {y_pos}, {z_pos}]")
        glutPostRedisplay()
        return
    if key == 'c' and current_mode in [1, 2, 3, 4]:
        unlimited_bullets = not unlimited_bullets
        print(f"Frame {frame_count}: Unlimited bullets {'enabled' if unlimited_bullets else 'disabled'}")
        glutPostRedisplay()
        return
    if current_mode == 0:
        if key == '-':
            fovY = min(120, fovY + 5)
        elif key == '=':
            fovY = max(20, fovY - 5)
    elif current_mode in [1, 2, 3, 4] and not game_over:
        if key == '-':
            fovY_mode = min(120, fovY_mode + 5)
        elif key == '=':
            fovY_mode = max(20, fovY_mode - 5)
        elif key == 'f':
            bullet_start = [x_pos, y_pos, z_pos]
            bullet_dir = (math.sin(math.radians(rotation_angle)), math.cos(math.radians(rotation_angle)), 0) if is_3d_mode else (0, 1, 0)
            if unlimited_bullets or len(bullets) < 10:
                bullets.append((bullet_start, bullet_dir, False))
                print(f"Frame {frame_count}: Fired bullet, total bullets: {len(bullets)}")
        elif key == 'r':
            bullet_start = [x_pos, y_pos, z_pos]
            bullet_dir = (math.sin(math.radians(rotation_angle)), math.cos(math.radians(rotation_angle)), 0) if is_3d_mode else (0, 1, 0)
            if unlimited_bullets or len(bullets) < 10:
                bullets.append((bullet_start, bullet_dir, True))
                print(f"Frame {frame_count}: Fired rocket, total bullets: {len(bullets)}")
        elif key == 'g':
            game_over = True
        if is_3d_mode:
            theta = math.radians(rotation_angle)
            move_speed = 0.3
            if key == 'w':
                new_x = x_pos + move_speed * math.sin(theta)
                new_y = y_pos + move_speed * math.cos(theta)
                if -10 <= new_x <= 10 and -10 <= new_y <= 10:
                    x_pos, y_pos = new_x, new_y
            elif key == 's':
                new_x = x_pos - move_speed * math.sin(theta)
                new_y = y_pos - move_speed * math.cos(theta)
                if -10 <= new_x <= 10 and -10 <= new_y <= 10:
                    x_pos, y_pos = new_x, new_y
            elif key == 'a':
                new_x = x_pos - move_speed * math.cos(theta)
                new_y = y_pos + move_speed * math.sin(theta)
                if -10 <= new_x <= 10 and -10 <= new_y <= 10:
                    x_pos, y_pos = new_x, new_y
            elif key == 'd':
                new_x = x_pos + move_speed * math.cos(theta)
                new_y = y_pos - move_speed * math.sin(theta)
                if -10 <= new_x <= 10 and -10 <= new_y <= 10:
                    x_pos, y_pos = new_x, new_y
        else:
            move_speed = 0.15
            if key == 'a':
                new_x = x_pos - move_speed
                if -10 <= new_x <= 10:
                    x_pos = new_x
            elif key == 'd':
                new_x = x_pos + move_speed
                if -10 <= new_x <= 10:
                    x_pos = new_x
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global x_pos, y_pos, z_pos, rotation_angle, camera_pos
    if current_mode == 0:
        x, y, z = camera_pos
        if key == GLUT_KEY_LEFT:
            x = max(-1000, x - 20)
        elif key == GLUT_KEY_RIGHT:
            x = min(1000, x + 20)
        elif key == GLUT_KEY_UP:
            y = min(1000, y + 20)
        elif key == GLUT_KEY_DOWN:
            y = max(-1000, y - 20)
        camera_pos = (x, y, z)
    elif current_mode in [1, 2, 3, 4] and not game_over:
        if is_3d_mode:
            move_speed = 0.3
            if key == GLUT_KEY_UP:
                new_z = z_pos + move_speed
                if -10 <= new_z <= 10:
                    z_pos = new_z
            elif key == GLUT_KEY_DOWN:
                new_z = z_pos - move_speed
                if -10 <= new_z <= 10:
                    z_pos = new_z
        else:
            move_speed = 0.15
            if key == GLUT_KEY_UP:
                new_y = y_pos + move_speed
                if -10 <= new_y <= 10:
                    y_pos = new_y
            elif key == GLUT_KEY_DOWN:
                new_y = y_pos - move_speed
                if -10 <= new_y <= 10:
                    y_pos = new_y
        if key == GLUT_KEY_LEFT:
            rotation_angle = (rotation_angle + 5) % 360
        elif key == GLUT_KEY_RIGHT:
            rotation_angle = (rotation_angle - 5) % 360
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global current_mode, level_cleared, camera_pos_mode, x_pos, y_pos, z_pos, rotation_angle, bullets, game_over, health, aliens, alien_kill_count, fovY_mode, timer, boss_pos, boss_bullets, boss_health, boss_bullet_timer, current_level, alien_bullets, alien_bullet_timer, unlimited_bullets, boss_active
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        screen_y = 800 - y
        if current_mode == 0 and 0 <= x <= 150:
            if 760 <= screen_y <= 780:
                current_mode = 1
                current_level = 1
            elif 730 <= screen_y <= 750:
                current_mode = 2
            elif 700 <= screen_y <= 720:
                current_mode = 3
            elif 670 <= screen_y <= 690:
                current_mode = 4
            if current_mode in [1, 2, 3, 4]:
                camera_pos_mode = (0, 0, 5)
                x_pos, y_pos, z_pos = 0, 0, -5 if not is_3d_mode else 0
                rotation_angle = 0
                bullets = []
                boss_bullets = []
                alien_bullets = []
                game_over = False
                health = 5
                alien_kill_count = 0
                fovY_mode = 45
                unlimited_bullets = False
                boss_active = False
                timer = 3600.0 if current_mode == 2 else 0.0
                alien_bullet_timer = 0.0
                if current_mode == 1:
                    alien_count = int(3 + (current_level - 1) * (7 / 7))
                    aliens = [spawn_alien() for _ in range(alien_count)]
                elif current_mode in [2, 4]:
                    aliens = [spawn_alien() for _ in range(5)]
                else:  # Mode 3
                    aliens = []
                    spawn_boss()
                print(f"Frame {frame_count}: Switched to mode {current_mode}, level {current_level}, health: {health}, aliens: {len(aliens)}")
        elif current_mode in [1, 2, 3, 4] and 0 <= x <= 100:
            if 760 <= screen_y <= 780:
                current_mode = 0
                bullets = []
                boss_bullets = []
                alien_bullets = []
                game_over = False
                health = 5
                alien_kill_count = 0
                timer = 3600.0
                boss_health = 100
                boss_bullet_timer = 0.0
                alien_bullet_timer = 0.0
                unlimited_bullets = False
                boss_active = False
                print(f"Frame {frame_count}: Returned to homepage, health: {health}")
            elif 730 <= screen_y <= 750:
                restart_mode()
    glutPostRedisplay()

def idle():
    global time, frame_count, asteroids, aliens, health, game_over, timer, boss_pos, current_level, level_cleared, current_mode, alien_kill_count, alien_bullet_timer, boss_active
    time += 0.05
    frame_count += 1
    if game_over:
        glutPostRedisplay()
        return
    if current_mode == 0:
        new_asteroids = []
        for x, y, z, vx, vy, vz, radius in asteroids:
            x += vx
            y += vy
            z += vz
            if abs(x) <= 1000 and abs(y) <= 1000 and -500 <= z <= -100:
                new_asteroids.append((x, y, z, vx, vy, vz, radius))
        if len(new_asteroids) < 3 and random.random() < 0.01:
            new_asteroids.append((
                random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-500, -100),
                random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1),
                random.uniform(5, 10)
            ))
        asteroids = new_asteroids
    elif current_mode in [1, 2, 4]:
        if current_mode == 2:
            timer = max(0, timer - 0.05)
            if timer <= 0:
                game_over = True
        if current_mode == 1 and boss_active:
            dx = x_pos - boss_pos[0]
            dy = y_pos - boss_pos[1]
            dz = z_pos - boss_pos[2] if is_3d_mode else 0
            dist = math.sqrt(dx**2 + dy**2 + (dz**2 if is_3d_mode else 0))
            print(f"Frame {frame_count}: Boss at {boss_pos}, spaceship at [{x_pos}, {y_pos}, {z_pos}], dist: {dist}")
            if dist > 2.0:
                speed = 0.01
                if dist > 0:
                    boss_pos[0] += (dx / dist) * speed
                    boss_pos[1] += (dy / dist) * speed
                    boss_pos[2] += (dz / dist) * speed if is_3d_mode else 0
                boss_pos[0] = max(-10, min(10, boss_pos[0]))
                boss_pos[1] = max(-10, min(10, boss_pos[1]))
                boss_pos[2] = max(-10, min(10, boss_pos[2])) if is_3d_mode else -5
            if dist < 2.0 and not game_over:
                health -= 1
                print(f"Frame {frame_count}: Health decreased to {health} due to boss collision")
                if health <= 0:
                    game_over = True
        else:
            alien_speed = 0.005 if current_mode in [2, 4] else (0.002 + (current_level - 1) * (0.006 / 7))
            for i, (pos, alive) in enumerate(aliens):
                if alive:
                    dx = x_pos - pos[0]
                    dy = y_pos - pos[1]
                    dz = z_pos - pos[2] if is_3d_mode else 0
                    dist = math.sqrt(dx**2 + dy**2 + (dz**2 if is_3d_mode else 0))
                    print(f"Frame {frame_count}: Alien at {pos}, spaceship at [{x_pos}, {y_pos}, {z_pos}], dist: {dist}")
                    if dist > 2.0:
                        if dist > 0:
                            pos[0] += (dx / dist) * alien_speed
                            pos[1] += (dy / dist) * alien_speed
                            pos[2] += (dz / dist) * alien_speed if is_3d_mode else 0
                        pos[0] = max(-10, min(10, pos[0]))
                        pos[1] = max(-10, min(10, pos[1]))
                        pos[2] = max(-10, min(10, pos[2])) if is_3d_mode else -5
                    if dist < 2.0 and not game_over:
                        health -= 1
                        aliens[i] = spawn_alien()
                        print(f"Frame {frame_count}: Health decreased to {health} due to alien collision")
                        if health <= 0:
                            game_over = True
            if current_mode == 1 and alien_kill_count >= current_level * 10 and not game_over and not boss_active:
                if current_level in [2, 4, 6, 8]:
                    boss_active = True
                    aliens = []
                    bullets = []
                    alien_bullets = []
                    spawn_boss()
                    print(f"Frame {frame_count}: Level {current_level} aliens cleared, boss spawned")
                else:
                    current_level += 1
                    if current_level > 8:
                        current_mode = 0
                        level_cleared = 8
                        aliens = []
                        print(f"Frame {frame_count}: Completed Career Mode, returned to homepage")
                    else:
                        alien_kill_count = 0
                        alien_count = int(3 + (current_level - 1) * (7 / 7))
                        aliens = [spawn_alien() for _ in range(alien_count)]
                        alien_bullet_timer = 0.0
                        print(f"Frame {frame_count}: Advanced to level {current_level}, aliens: {alien_count}")
    elif current_mode == 3:
        dx = x_pos - boss_pos[0]
        dy = y_pos - boss_pos[1]
        dz = z_pos - boss_pos[2] if is_3d_mode else 0
        dist = math.sqrt(dx**2 + dy**2 + (dz**2 if is_3d_mode else 0))
        print(f"Frame {frame_count}: Boss at {boss_pos}, spaceship at [{x_pos}, {y_pos}, {z_pos}], dist: {dist}")
        if dist > 2.0:
            speed = 0.01
            if dist > 0:
                boss_pos[0] += (dx / dist) * speed
                boss_pos[1] += (dy / dist) * speed
                boss_pos[2] += (dz / dist) * speed if is_3d_mode else 0
            boss_pos[0] = max(-10, min(10, boss_pos[0]))
            boss_pos[1] = max(-10, min(10, boss_pos[1]))
            boss_pos[2] = max(-10, min(10, boss_pos[2])) if is_3d_mode else -5
        if dist < 2.0 and not game_over:
            health -= 1
            print(f"Frame {frame_count}: Health decreased to {health} due to boss collision")
            if health <= 0:
                game_over = True
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if current_mode == 0:
        init()
        glViewport(0, 0, 1000, 800)
        setupCamera()
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glPointSize(3)
        glBegin(GL_POINTS)
        for x, y, z, offset, color_idx in stars:
            intensity = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(time + offset))
            r, g, b = star_colors[color_idx]
            glColor3f(r * intensity, g * intensity, b * intensity)
            glVertex3f(x, y, z)
        glEnd()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        light_pos = (0, 0, 1000, 1)
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glPushMatrix()
        for x, y, z, _, _, _, radius in asteroids:
            glPushMatrix()
            glTranslatef(x, y, z)
            quad = gluNewQuadric()
            glColor3f(0.5, 0.5, 0.5)
            gluSphere(quad, radius, 10, 10)
            glPopMatrix()
        glPopMatrix()
        draw_planets_and_sun()
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)
        draw_text(10, 770, "Career Mode", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 740, "Timed Run", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 710, "Boss Fight", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 680, "Endless", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 650, "Total Level - 8", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 620, f"Level Cleared - {level_cleared}", GLUT_BITMAP_HELVETICA_18)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 800)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        draw_clock(120, 740, 10)
        draw_skull(130, 710, 10)
        draw_infinity(110, 680, 10)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glutSwapBuffers()
    else:
        draw_spaceship()

def main():
    global health
    health = 5
    try:
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"Spaceship Battle")
    except Exception as e:
        print(f"Error initializing GLUT: {e}")
        sys.exit(1)
    init()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutTimerFunc(100, update_flame, 0)
    glutTimerFunc(33, update_bullets, 0)
    glutTimerFunc(33, update_boss_bullets, 0)
    glutTimerFunc(33, update_alien_bullets, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()