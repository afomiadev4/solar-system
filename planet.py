from OpenGL.GL import *
import math


class Planet:

    def __init__(self, distance, size, speed, color):

        # orbit radius from the sun at (0, 0)
        self.distance = distance

        # radius of the planet's circle
        self.size = size

        # angular speed (radians per second)
        self.speed = speed

        # RGB tuple, each component in 0.0 - 1.0
        self.color = color

        # internal orbital angle (radians)
        self.angle = 0.0

        self.segments = 60

    def update(self, dt):

        # advance around the orbit using delta time
        self.angle += self.speed * dt

        # keep the angle bounded to avoid float growth
        self.angle %= 2 * math.pi

    def get_position(self):

        x = self.distance * math.cos(self.angle)
        y = self.distance * math.sin(self.angle)

        return x, y

    def draw_orbit(self):

        # dim version of the planet's color for the orbit ring
        glColor3f(*(c * 0.4 for c in self.color))

        glBegin(GL_LINE_LOOP)

        # ring centered on the sun at (0, 0) at this planet's distance
        for i in range(self.segments):

            angle = 2 * math.pi * i / self.segments

            px = self.distance * math.cos(angle)
            py = self.distance * math.sin(angle)

            glVertex2f(px, py)

        glEnd()

    def draw(self):

        x, y = self.get_position()

        glColor3f(*self.color)

        glBegin(GL_TRIANGLE_FAN)

        # center of the planet at its orbit position
        glVertex2f(x, y)

        for i in range(self.segments + 1):

            angle = 2 * math.pi * i / self.segments

            px = x + self.size * math.cos(angle)
            py = y + self.size * math.sin(angle)

            glVertex2f(px, py)

        glEnd()
