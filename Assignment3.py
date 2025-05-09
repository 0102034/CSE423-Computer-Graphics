from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Camera-related variables
camera_pos = (0, 500, 500)
cam_angle = 0
person_mode = False

#grid
fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
#rand_var = 423
grid_size = 4

#game
game_over = False
score = 0
lives = 10
missed_bul = 0


#player
p_pos = [0, 0, 0]
p_speed = 5
gun = 50
gun_angle = 0
gun_rotation_speed = 0.5
#enemy
enemies = []
e_speed = 0.01
e_radius = 20
e_pulse_speed = 0.5
e_dir = 1
#bul
bullets = []
bul_speed = 15
bul_size = 10
#cheats
cheat_active = False
auto_follow = False

def init():
    global enemies, bullets, game_over, score, lives, missed_bul, p_pos, gun_angle, bullets, enemies, cheat_active, auto_follow
    game_over = False
    score = 0
    lives = 5
    missed_bul = 0
    p_pos = [0, 0, 0]
    gun_angle = 0
    bullets = []
    cheat_active = False
    auto_follow = False
    enemies = []

    for i in range(5):
        spawn_enemy()

def spawn_enemy():
    while True:
        x = random.randint(-GRID_LENGTH + 100, GRID_LENGTH-100)
        y = random.randint(-GRID_LENGTH+100, GRID_LENGTH-100)
        if math.sqrt((x-p_pos[0])**2 + (y-p_pos[1])**2)>200:
            break

    enemy = {
        "pos": [x, y, e_radius],
        "size": e_radius,
        "pulse_factor": random.uniform(0.8, 1.2),
        "direction": 1
    }
    enemies.append(enemy)

def fire_bullets():
    if game_over:
        return
    angle_rad = math.radians(gun_angle)
    direction_x = math.cos(angle_rad)
    direction_y = math.sin(angle_rad)

    bullet = {
        "pos": [p_pos[0] +direction_x*70, p_pos[1]+direction_y*70, 30],
        "direction": [direction_x, direction_y],
        "hits_enemy": False,
        "out_of_bounds": False
    }
    bullets.append(bullet)

def game_state():
    global missed_bul, score, lives, game_over, bullets

    if game_over:
        return
    for bullet in bullets[:]:
        bullet["pos"][0] += bullet["direction"][0] * bul_speed
        bullet["pos"][1] += bullet["direction"][1] * bul_speed

        if (abs(bullet["pos"][0]) > GRID_LENGTH or abs(bullet["pos"][1]) > GRID_LENGTH):
            bullet["out_of_bounds"] = True
            if not bullet["hits_enemy"]:
                missed_bul += 1

        for enemy in enemies[:]:
            dx = bullet["pos"][0] - enemy["pos"][0]
            dy = bullet["pos"][1] - enemy["pos"][1]
            distance = math.sqrt(dx**2 + dy**2)

            if distance < enemy["size"] + bul_size/2:
                bullet["hits_enemy"] = True
                enemies.remove(enemy)
                score+=1
                spawn_enemy()
                break
    bullets[:] = [b for b in bullets if not (b["hits_enemy"] or b["out_of_bounds"])]

    for enemy in enemies:
        dx = p_pos[0] - enemy["pos"][0]
        dy = p_pos[1] - enemy["pos"][1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            enemy["pos"][0] += (dx/distance) * e_speed
            enemy["pos"][1] += (dy/distance) * e_speed

        pulse_amount = e_pulse_speed * enemy["pulse_factor"]
        enemy["size"] += enemy["direction"]*pulse_amount

        if enemy["size"] > e_radius*1.3:
            enemy["direction"] = -1
        elif enemy["size"] < e_radius*0.7:
            enemy["direction"] = 1

        if distance<enemy["size"]+50:
            lives -= 1
            enemies.remove(enemy)
            spawn_enemy()

    if lives <= 0 or missed_bul >50:
        game_over = True

    if cheat_active:
        global gun_angle
        gun_angle = (gun_angle+2) % 360

        for enemy in enemies:
            dx = p_pos[0] - enemy["pos"][0]
            dy = p_pos[1] - enemy["pos"][1]
            enemy_angle = math.degrees(math.atan2(dy, dx)) % 360

            if abs(gun_angle - enemy_angle) < 5 or abs(gun_angle - enemy_angle > 355):
                fire_bullets()
                break

def draw_player():
    glPushMatrix()
    glTranslatef(p_pos[0], p_pos[1], p_pos[2])
    glRotatef(gun_angle, 0, 0, 1)

    if game_over:
        glRotatef(90, 0, 1, 0)

    glColor3f(0.8, 0.6, 0.2) #player
    gluSphere(gluNewQuadric(), 40, 20, 20)

    glPushMatrix() #barrel
    glTranslatef(0, 0, 20)
    glRotatef(90, 0, 1, 0)
    glColor3f(0.3, 0.3, 0.3)
    gluCylinder(gluNewQuadric(), 10, 10, gun, 10, 10)

    glTranslatef(0, 0, gun)
    gluCylinder(gluNewQuadric(), 15, 5, 20, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -10, 10)
    glColor3f(0.5, 0.5, 0.5)
    glutSolidCube(40)
    glPopMatrix()

    glPopMatrix()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy["pos"][0], enemy["pos"][1], enemy["pos"][2])
        glColor3f(1.0, 0.2, 0.2)
        gluSphere(gluNewQuadric(), enemy["size"], 20, 20)

        glColor3f(0.8, 0.2, 0.0)
        glTranslatef(0,0,enemy["size"]*0.8)
        gluSphere(gluNewQuadric(), enemy["size"], 20, 20)
        glPopMatrix()

def draw_bullets():
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet["pos"][0], bullet["pos"][1], bullet['pos'][2])
        glColor3f(1.0, 1.0, 0.0)
        glutSolidCube(bul_size)
        glPopMatrix()

def draw_shapes():
    glPushMatrix()  # Save the current matrix state
    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 0)
    glutSolidCube(60)  # Take cube size as the parameter
    glTranslatef(0, 0, 100)
    glColor3f(0, 1, 0)
    glutSolidCube(60)

    glColor3f(1, 1, 0)
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10,
                10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glTranslatef(100, 0, 100)
    glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    glColor3f(0, 1, 1)
    glTranslatef(300, 0, 100)
    gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()  # Restore the previous matrix state

def game():
    draw_text(10, 770, f"Life: {lives}")
    draw_text(10, 740, f"Score: {score}")
    draw_text(10, 710, f"Bullets Missed: {missed_bul}")

    if cheat_active:
        draw_text(800, 770, "Cheat Mode: ON")
    else:
        draw_text(800, 770, "Cheat Mode: Off")
    if person_mode:
        draw_text(800, 740, "View: First Person")
    else:
        draw_text(800, 740, "View: Third Person")

    if auto_follow and cheat_active and person_mode:
        draw_text(800, 710, "Auto Follow: On")

    if game_over:
        draw_text(400, 400, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(400, 370, "Press 'R' to restart", GLUT_BITMAP_HELVETICA_18)


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global p_pos, gun_angle, cheat_active, auto_follow, game_over
    if game_over and key == b"r":
        init()
        return
    if game_over:
        return
    # # Move forward (W key)
    if key == b'w':
        angle_rad = math.radians(gun_angle)
        p_pos[0] += math.cos(angle_rad)*p_speed
        p_pos[1] += math.sin(angle_rad) * p_speed
        p_pos[0] = max(min(p_pos[0], GRID_LENGTH-50), -GRID_LENGTH+50)
        p_pos[1] = max(min(p_pos[1], GRID_LENGTH - 50), -GRID_LENGTH + 50)

    # # Move backward (S key)
    if key == b'b':
        angle_rad = math.radians(gun_angle)
        p_pos[0] -= math.cos(angle_rad) * p_speed
        p_pos[1] -= math.sin(angle_rad) * p_speed
        p_pos[0] = max(min(p_pos[0], GRID_LENGTH - 50), -GRID_LENGTH + 50)
        p_pos[1] = max(min(p_pos[1], GRID_LENGTH - 50), -GRID_LENGTH + 50)

    # # Rotate gun left (A key)
    if key == b'l':
        gun_angle = (gun_angle-gun_rotation_speed)%360

    # # Rotate gun right (D key)
    if key == b'r':
        gun_angle = (gun_angle + gun_rotation_speed) % 360

    # # Toggle cheat mode (C key)
    if key == b'c':
        cheat_active = not cheat_active
        if not cheat_active:
            auto_follow = False

    # # Toggle cheat vision (V key)
    if key == b'v':
        if cheat_active and person_mode:
            auto_follow = not auto_follow


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, cam_angle
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        y+=20
        y = min(y, 1000)

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        y-=20
        y=max(y, 100)

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement
        cam_angle = (cam_angle+2)%360

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement
        cam_angle = (cam_angle - 2) % 360

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # # Left mouse button fires a bullet
    global person_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not game_over:
            fire_bullets()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        person_mode = not person_mode


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500)  # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if person_mode:
        eye_x = p_pos[0] -100*math.cos(math.radians(gun_angle))
        eye_y = p_pos[1] - 100 * math.sin(math.radians(gun_angle))
        eye_z = 50
        if auto_follow and cheat_active:
            look_x = p_pos[0] + 200 * math.cos(math.radians(gun_angle))
            look_y = p_pos[1] + 200 * math.sin(math.radians(gun_angle))
            look_z = 30
        else:
            look_x = p_pos[0]
            look_y = p_pos[1]
            look_z = 30
        gluLookAt(eye_x, eye_y, eye_z, look_x, look_y, look_z, 0, 0, 1)
    else:
        # Extract camera position and look-at target
        x, y, z = camera_pos
        # Position the camera and set its orientation
        orbit_radius = math.sqrt(x**2 + y**2)
        cam_x = orbit_radius*math.cos(math.radians(cam_angle))
        cam_y = orbit_radius*math.sin(math.radians(cam_angle))

        gluLookAt(x, y, z,  # Camera position
               0, 0, 0,  # Look-at target
               0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    game_state()
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    draw_player()
    draw_enemies()
    draw_bullets()
    game()

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    glBegin(GL_QUADS)
#use LOOPS to tackle this, not by hand
    for i in range(-grid_size, grid_size):
        for j in range(-grid_size, grid_size):
            x_start = i*(GRID_LENGTH/grid_size)
            x_end = (i+1) * (GRID_LENGTH/grid_size)
            y_start = j * (GRID_LENGTH/grid_size)
            y_end = (j+1)*(GRID_LENGTH/grid_size)

        glVertex3f(x_start, y_start, 0)
        glVertex3f(x_end, y_start, 0)
        glVertex3f(x_end, y_end, 0)
        glVertex3f(x_start, y_end, 0)
    glEnd()

    #grid_fix
    glBegin(GL_LINES)
    for i in range(-grid_size, grid_size+1):
        y = i*(GRID_LENGTH/grid_size)
        glVertex3f(-GRID_LENGTH, y, 0)
        glVertex3f(GRID_LENGTH, y, 0)
    for j in range(-grid_size, grid_size+1):
        x = j * (GRID_LENGTH / grid_size)
        glVertex3f(x, -GRID_LENGTH, 0)
        glVertex3f(x, GRID_LENGTH, 0)
    glEnd()

    # Display game info text at a fixed screen position
    #draw_text(10, 770, f"A Random Fixed Position Text")
    #draw_text(10, 740, f"See how the position and variable change?: {rand_var}")

    draw_shapes()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()

# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"LabAssignment3")  # Create the window
    init()
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop


if __name__ == "__main__":
    main()



#if (i + j) % 2 == 0:
    # glColor3f(1.0, 1.0, 1.0)
#else:
# glColor3f(0.7, 0.5, 0.95)