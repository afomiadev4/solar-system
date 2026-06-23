from OpenGL.GL import *
import math
from settings import BACKGROUND_COLOR
from sun import Sun

# 🌞 Sun (Member 1)
sun = Sun()

def initialize():
    glClearColor(*BACKGROUND_COLOR)
    glEnable(GL_POINT_SMOOTH)


def render(dt, planets):   # 🪐 receives planets from main
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # 1. 🌞 DRAW THE SUN AT GLOBAL ORIGIN
    sun.draw()

    # 2. 🪐 MATRIX STACK WORK FOR PLANETS & MOONS
    for planet in planets:
        # Update animations
        planet.update(dt)
        for moon in planet.moons:
            moon.update(dt)

        # Draw the planet's background orbit ring
        planet.draw_orbit()

        # ─── ENTER PLANET MATRIX SPACE ───
        glPushMatrix()  # Save Sun's origin (0,0) onto the stack
            
            # Convert radians to degrees for OpenGL matrix rotation
            orbit_degrees = math.degrees(planet.angle)
            
            # 1. Rotate the transformation matrix to handle the orbit direction
            glRotatef(orbit_degrees, 0.0, 0.0, 1.0)
            
            # 2. Translate out along the rotated X-axis to the orbit radius
            glTranslatef(planet.distance, 0.0, 0.0)

            # Draw the planet primitive directly at its new local matrix center
            glPushMatrix()  # Save position before applying size scaling
                glScalef(planet.scale, planet.scale, 1.0) # Interactive scaling (Member 5 feature)
                
                # Draw the planet circle at local (0,0)
                glColor3f(*planet.color)
                glBegin(GL_TRIANGLE_FAN)
                glVertex2f(0, 0)
                for i in range(planet.segments + 1):
                    angle = 2 * math.pi * i / planet.segments
                    glVertex2f(planet.size * math.cos(angle), planet.size * math.sin(angle))
                glEnd()
            glPopMatrix()   # Remove scaling so it doesn't distort the child moons!

            # ─── ENTER MOON SPACE (Hierarchical Children of Planet) ───
            for moon in planet.moons:
                moon.draw_orbit() # Draw moon's orbit ring around its parent planet
                
                glPushMatrix()  # Save Planet's local position state
                    moon_degrees = math.degrees(moon.angle)
                    glRotatef(moon_degrees, 0.0, 0.0, 1.0)  # Rotate local moon space
                    glTranslatef(moon.distance, 0.0, 0.0)   # Move out to moon orbit distance
                    moon.draw()                             # Draw moon body primitive
                glPopMatrix()   # Leave individual Moon space, return to current Planet center

        glPopMatrix()  # Leave Planet space, return to Sun Space origin (0,0)