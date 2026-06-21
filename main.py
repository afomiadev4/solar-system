import glfw

from renderer import initialize
from renderer import render

from camera import setup_projection

from settings import *


def framebuffer_callback(window, width, height):

    setup_projection(width, height)


def key_callback(window, key, scancode, action, mods):

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:

        glfw.set_window_should_close(window, True)


def create_window():

    if not glfw.init():

        raise Exception("GLFW Initialization Failed")

    window = glfw.create_window(

        WIDTH,

        HEIGHT,

        TITLE,

        None,

        None

    )

    if not window:

        glfw.terminate()

        raise Exception("Window Creation Failed")

    glfw.make_context_current(window)

    glfw.set_framebuffer_size_callback(

        window,

        framebuffer_callback

    )

    glfw.set_key_callback(

        window,

        key_callback

    )

    setup_projection(WIDTH, HEIGHT)

    return window


def main():

    window = create_window()

    initialize()

    while not glfw.window_should_close(window):

        render()

        glfw.swap_buffers(window)

        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":

    main()