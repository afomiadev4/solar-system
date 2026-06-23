import glfw
import time

from renderer import initialize, render
from camera import setup_projection
from settings import *

from planet import Planet, Moon


planets = [
    Planet(80, 6, 2.0, (0.6, 0.6, 1.0)),
    Planet(120, 10, 1.5, (0.2, 0.8, 0.2)),
    Planet(170, 8, 1.2, (1.0, 0.4, 0.2)),
    Planet(230, 14, 0.6, (1.0, 0.8, 0.3)),
]

planets[0].moons.append(Moon(distance=15, size=2, speed=4.0, color=(0.8, 0.8, 0.8)))

planets[1].moons.append(Moon(distance=18, size=2.5, speed=3.0, color=(0.9, 0.5, 0.9)))
planets[1].moons.append(Moon(distance=28, size=1.5, speed=-2.0, color=(0.5, 0.9, 0.9)))

last_time = time.time()

def get_dt():
    global last_time
    current = time.time()
    dt = current - last_time
    last_time = current
    return dt


def framebuffer_callback(window, width, height):
    setup_projection(width, height)


def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def create_window():
    if not glfw.init():
        raise Exception("GLFW Initialization Failed")

    window = glfw.create_window(WIDTH, HEIGHT, TITLE, None, None)

    if not window:
        glfw.terminate()
        raise Exception("Window Creation Failed")

    glfw.make_context_current(window)

    glfw.set_framebuffer_size_callback(window, framebuffer_callback)
    glfw.set_key_callback(window, key_callback)

    setup_projection(WIDTH, HEIGHT)

    return window


def main():
    window = create_window()

    initialize()

    while not glfw.window_should_close(window):

        dt = get_dt()

        
        render(dt, planets)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()