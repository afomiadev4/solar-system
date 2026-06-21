from OpenGL.GL import *

def setup_projection(width, height):

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect = width / height

    if aspect >= 1:

        glOrtho(
            -aspect,
            aspect,
            -1,
            1,
            -1,
            1
        )

    else:

        glOrtho(
            -1,
            1,
            -1/aspect,
            1/aspect,
            -1,
            1
        )

    glMatrixMode(GL_MODELVIEW)