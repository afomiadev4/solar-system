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
    """Delegate entirely to the Member-5 controls object and handle viewport updates."""
    # Keep your team's control handling intact
    controls.key_callback(window, key, scancode, action, mods)
    
    # Process camera scaling adjustments on active key press or repeat events
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_I:  # Inward perspective scaling
            import camera
            camera.zoom_factor = max(0.25, camera.zoom_factor - 0.05)
            win_w, win_h = glfw.get_framebuffer_size(window)
            camera.setup_projection(win_w, win_h)
            print(f"Zoom level adjusted: {camera.zoom_factor:.2f}")  # Verification print
            
        elif key == glfw.KEY_O:  # Outward perspective scaling
            import camera
            camera.zoom_factor = min(3.0, camera.zoom_factor + 0.05)
            win_w, win_h = glfw.get_framebuffer_size(window)
            camera.setup_projection(win_w, win_h)
            print(f"Zoom level adjusted: {camera.zoom_factor:.2f}")  # Verification print


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
    print("   Hierarchical Solar System   -   Simulation View")
    print("=" * 52)
    print("  UP / W          Speed up")
    print("  DOWN / S        Slow down")
    print("  R               Reverse time")
    print("  SPACE           Pause / Resume")
    print("  ENTER           Reset speed to 1x")
    print("  1 - 4           Select a planet")
    print("  TAB             Cycle selected planet")
    print("  + / =           Enlarge planet size")
    print("  -               Shrink planet size")
    print("  0               Reset all sizes to 1.0")
    print("  I / O           Zoom Camera In / Out")  # Added notice
    print("  ESC             Quit")
    print("=" * 52)

    while not glfw.window_should_close(window):
        # Anchor point for calculation frame performance mapping
        start_frame_time = time.time()
        
        dt = get_dt()

        # Member 5 provides the scaled dt (handles pause / reverse)
        scaled_dt = controls.effective_scale * dt

        render(scaled_dt, planets)

        # Member 5 HUD overlay – drawn on top, in screen-space, no GLUT needed
        win_w, win_h = glfw.get_framebuffer_size(window)
        controls.draw_hud(win_w, win_h)

        glfw.swap_buffers(window)
        glfw.poll_events()

        # Performance Mapping Constraints: Force simulation execution limit loop to target FPS bounds
        target_frame_duration = 1.0 / FPS
        cycle_execution_time = time.time() - start_frame_time
        if cycle_execution_time < target_frame_duration:
            time.sleep(target_frame_duration - cycle_execution_time)

    glfw.terminate()


if __name__ == "__main__":
    main()