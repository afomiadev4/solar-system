from OpenGL.GL import *
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

    # 🌞 draw sun
    sun.draw()

    # 🪐 draw planets
    for planet in planets:
        planet.update(dt)
        planet.draw()