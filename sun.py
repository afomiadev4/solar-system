from OpenGL.GL import *
import math


class Sun:

    def __init__(self):

        self.radius = 25
        self.segments = 100

    def draw(self):

        glColor3f(
            1.0,
            0.85,
            0.0
        )

        glBegin(GL_TRIANGLE_FAN)

        glVertex2f(0, 0)

        for i in range(self.segments + 1):

            angle = 2 * math.pi * i / self.segments

            x = self.radius * math.cos(angle)
            y = self.radius * math.sin(angle)

            glVertex2f(x, y)

        glEnd()