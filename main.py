import glfw
import time

from renderer import initialize, render
from camera import setup_projection
from settings import *
from planet import Planet, Moon
from controls import UserControls         # Member 5

# ── Scene setup ─────────────────────────────────────────────────────────────
planets = [
    Planet(80,  6,  2.0, (0.6, 0.6, 1.0)),   # 1 – blue (Earth-like)
    Planet(120, 10, 1.5, (0.2, 0.8, 0.2)),   # 2 – green
    Planet(170, 8,  1.2, (1.0, 0.4, 0.2)),   # 3 – red-orange (Mars-like)
    Planet(230, 14, 0.6, (1.0, 0.8, 0.3)),   # 4 – yellow (Jupiter-like)
]

planets[0].moons.append(Moon(distance=15, size=2,   speed=4.0,  color=(0.8, 0.8, 0.8)))
planets[1].moons.append(Moon(distance=18, size=2.5, speed=3.0,  color=(0.9, 0.5, 0.9)))
planets[1].moons.append(Moon(distance=28, size=1.5, speed=-2.0, color=(0.5, 0.9, 0.9)))

controls = UserControls(planets)

# ── Delta-time tracker ──────────────────────────────────────────────────────
last_time = time.time()

def get_dt():
    global last_time
    current   = time.time()
    dt        = current - last_time
    last_time = current
    return dt

# ── GLFW callbacks ──────────────────────────────────────────────────────────

def framebuffer_callback(window, width, height):
    setup_projection(width, height)


def key_callback(window, key, scancode, action, mods):
    """Delegate entirely to the Member-5 controls object."""
    controls.key_callback(window, key, scancode, action, mods)


# ── Window creation ─────────────────────────────────────────────────────────

def create_window():
    if not glfw.init():
        raise Exception("GLFW Initialisation Failed")

    window = glfw.create_window(WIDTH, HEIGHT, TITLE, None, None)

    if not window:
        glfw.terminate()
        raise Exception("Window Creation Failed")

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_callback)
    glfw.set_key_callback(window, key_callback)

    setup_projection(WIDTH, HEIGHT)
    return window


# ── Main loop ───────────────────────────────────────────────────────────────

def main():
    window = create_window()
    initialize()

    print("=" * 52)
    print("  Hierarchical Solar System  -  Member 5 Controls")
    print("=" * 52)
    print("  UP / W          Speed up")
    print("  DOWN / S        Slow down")
    print("  R               Reverse time")
    print("  SPACE           Pause / Resume")
    print("  ENTER           Reset speed to 1x")
    print("  1 - 4           Select a planet (again to deselect)")
    print("  TAB             Cycle selected planet")
    print("  + / =           Enlarge selected / all planet(s)")
    print("  -               Shrink  selected / all planet(s)")
    print("  0               Reset all planet sizes to 1.0")
    print("  ESC             Quit")
    print("=" * 52)

    while not glfw.window_should_close(window):
        dt = get_dt()

        # Member 5 provides the scaled dt (handles pause / reverse)
        scaled_dt = controls.effective_scale * dt

        render(scaled_dt, planets)

        # Member 5 HUD overlay – drawn on top, in screen-space, no GLUT needed
        win_w, win_h = glfw.get_framebuffer_size(window)
        controls.draw_hud(win_w, win_h)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()