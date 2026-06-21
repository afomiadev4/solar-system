from OpenGL.GL import *

from settings import BACKGROUND_COLOR

from sun import Sun

sun = Sun()


def initialize():

    glClearColor(*BACKGROUND_COLOR)

    glEnable(GL_POINT_SMOOTH)


def render():

    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    sun.draw()