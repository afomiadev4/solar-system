from OpenGL.GL import *
from settings import WORLD_HALF_HEIGHT

def setup_projection(width, height):

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect = width / height

    # span the world in world units so planets (placed at
    # distances of hundreds) fall inside the visible region.
    half_h = WORLD_HALF_HEIGHT

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