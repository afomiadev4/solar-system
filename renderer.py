from OpenGL.GL import *
import math
from settings import BACKGROUND_COLOR
from sun import Sun

sun = Sun()

def initialize():
    glClearColor(*BACKGROUND_COLOR)
    glEnable(GL_POINT_SMOOTH)


def render(dt, planets):  
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    sun.draw()

    
    for planet in planets:
        
        planet.update(dt)
        for moon in planet.moons:
            moon.update(dt)

        
        planet.draw_orbit()

        
        glPushMatrix()  
        
        
        orbit_degrees = math.degrees(planet.angle)
        
        
        glRotatef(orbit_degrees, 0.0, 0.0, 1.0)
        
        
        glTranslatef(planet.distance, 0.0, 0.0)

        
        glPushMatrix()  
        glScalef(planet.scale, planet.scale, 1.0) 
        
        
        glColor3f(*planet.color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for i in range(planet.segments + 1):
            angle = 2 * math.pi * i / planet.segments
            glVertex2f(planet.size * math.cos(angle), planet.size * math.sin(angle))
        glEnd()
        glPopMatrix()   

        
        for moon in planet.moons:
            moon.draw_orbit() 
            
            glPushMatrix()  
            moon_degrees = math.degrees(moon.angle)
            glRotatef(moon_degrees, 0.0, 0.0, 1.0)  
            glTranslatef(moon.distance, 0.0, 0.0)   
            moon.draw()                             
            glPopMatrix()   

        glPopMatrix()  