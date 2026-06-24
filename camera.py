from OpenGL.GL import *
from settings import WORLD_HALF_HEIGHT

# Camera zoom: <1 zooms in (smaller world view), >1 zooms out (larger view).
zoom_factor = 1.0

def setup_projection(width, height):

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect = width / height



    half_h = WORLD_HALF_HEIGHT * zoom_factor

    if aspect >= 1:

        half_w = half_h * aspect

    else:

        half_w = half_h
        half_h = half_h / aspect

    glOrtho(
        -half_w,
        half_w,
        -half_h,
        half_h,
        -1,
        1
    )

    glMatrixMode(GL_MODELVIEW)