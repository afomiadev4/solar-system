from OpenGL.GL import *
import math


class Planet:

    def __init__(self, distance, size, speed, color):

        
        self.distance = distance

        
        self.size = size

        
        self.speed = speed

        
        self.color = color

        
        self.angle = 0.0

        self.segments = 60

        self.rotation = 0.0

        self.scale = 1.0
        self.moons = []

    def update(self, dt):

        
        self.angle += self.speed * dt
        self.rotation += dt

        
        self.angle %= 2 * math.pi
        self.rotation %= 2 * math.pi

    def get_position(self):

        x = self.distance * math.cos(self.angle)
        y = self.distance * math.sin(self.angle)

        return x, y

    def draw_orbit(self):

        
        glColor3f(*(c * 0.4 for c in self.color))

        glBegin(GL_LINE_LOOP)

        
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

        
        glVertex2f(x, y)

        for i in range(self.segments + 1):

            angle = 2 * math.pi * i / self.segments

            px = x + self.size * math.cos(angle)
            py = y + self.size * math.sin(angle)

            glVertex2f(px, py)

        glEnd()

class Moon:
    def __init__(self, distance, size, speed, color=(0.7, 0.7, 0.7)):
        
        self.distance = distance
        
        
        self.size = size
        
        
        self.speed = speed
        
        
        self.color = color
        
        
        self.angle = 0.0
        self.segments = 30

    def update(self, dt):
        
        self.angle += self.speed * dt
        self.angle %= 2 * math.pi

    def draw_orbit(self):
        
        glColor3f(*(c * 0.4 for c in self.color))
        glBegin(GL_LINE_LOOP)
        for i in range(self.segments):
            angle = 2 * math.pi * i / self.segments
            glVertex2f(self.distance * math.cos(angle), self.distance * math.sin(angle))
        glEnd()

    def draw(self):
        
        glColor3f(*self.color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for i in range(self.segments + 1):
            angle = 2 * math.pi * i / self.segments
            glVertex2f(self.size * math.cos(angle), self.size * math.sin(angle))
        glEnd()
