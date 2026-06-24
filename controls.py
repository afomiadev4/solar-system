"""
controls.py  –  Member 5: User Controls
=========================================
Responsibilities
----------------
- Speed up  : UP arrow  / W
- Slow down : DOWN arrow / S
- Reverse   : R  (toggles negative time scale)
- Pause     : SPACE
- Reset     : ENTER / BACKSPACE
- Resize all planets bigger  : +  / =
- Resize all planets smaller : -
- Resize individual planets  : 1-4 keys to select, then +/- to resize
- Cycle selected planet      : TAB
- HUD overlay showing current state (GLUT-free pixel-font approach)

Algorithm notes
---------------
time_scale is a float multiplier applied to dt in main.py.
  > 0  → forward
  < 0  → reversed
  = 0  → paused (handled via pause flag to restore direction)

Planet scale is stored as `planet.scale` (already wired in renderer.py).
Each planet starts at scale=1.0;  we clamp between [MIN_SCALE, MAX_SCALE].

HUD note
--------
We draw the HUD using simple coloured quads (pixel bars) arranged as
a tiny bitmap font, so there is NO GLUT / freeglut dependency.
If you have GLUT available, you can swap in glutBitmapCharacter instead.
"""

import glfw
from OpenGL.GL import *
import math

# ── Speed settings ──────────────────────────────────────────────────────────
DEFAULT_SPEED   = 1.0
SPEED_STEP      = 0.25       # ±step per key press
MAX_SPEED       = 8.0
MIN_SPEED       = 0.25       # minimum positive magnitude

# ── Planet scale settings ────────────────────────────────────────────────────
SCALE_STEP      = 0.10
MIN_SCALE       = 0.2
MAX_SCALE       = 3.0

# ── Tiny 5×7 bitmap font (ASCII 32-126) ─────────────────────────────────────
# Each character is represented as 5 columns of 7-bit bitmaps (bit 6 = top).
# Only the glyphs we actually need are defined; everything else falls back to '?'.
_FONT = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
    '!': [0x00, 0x00, 0x5F, 0x00, 0x00],
    '#': [0x14, 0x7F, 0x14, 0x7F, 0x14],
    '%': [0x23, 0x13, 0x08, 0x64, 0x62],
    '(': [0x00, 0x1C, 0x22, 0x41, 0x00],
    ')': [0x00, 0x41, 0x22, 0x1C, 0x00],
    '+': [0x08, 0x08, 0x3E, 0x08, 0x08],
    ',': [0x00, 0x50, 0x30, 0x00, 0x00],
    '-': [0x08, 0x08, 0x08, 0x08, 0x08],
    '.': [0x00, 0x60, 0x60, 0x00, 0x00],
    '/': [0x20, 0x10, 0x08, 0x04, 0x02],
    '0': [0x3E, 0x51, 0x49, 0x45, 0x3E],
    '1': [0x00, 0x42, 0x7F, 0x40, 0x00],
    '2': [0x42, 0x61, 0x51, 0x49, 0x46],
    '3': [0x21, 0x41, 0x45, 0x4B, 0x31],
    '4': [0x18, 0x14, 0x12, 0x7F, 0x10],
    '5': [0x27, 0x45, 0x45, 0x45, 0x39],
    '6': [0x3C, 0x4A, 0x49, 0x49, 0x30],
    '7': [0x01, 0x71, 0x09, 0x05, 0x03],
    '8': [0x36, 0x49, 0x49, 0x49, 0x36],
    '9': [0x06, 0x49, 0x49, 0x29, 0x1E],
    ':': [0x00, 0x36, 0x36, 0x00, 0x00],
    '<': [0x08, 0x14, 0x22, 0x41, 0x00],
    '=': [0x14, 0x14, 0x14, 0x14, 0x14],
    '>': [0x00, 0x41, 0x22, 0x14, 0x08],
    '?': [0x02, 0x01, 0x51, 0x09, 0x06],
    'A': [0x7E, 0x11, 0x11, 0x11, 0x7E],
    'B': [0x7F, 0x49, 0x49, 0x49, 0x36],
    'C': [0x3E, 0x41, 0x41, 0x41, 0x22],
    'D': [0x7F, 0x41, 0x41, 0x22, 0x1C],
    'E': [0x7F, 0x49, 0x49, 0x49, 0x41],
    'F': [0x7F, 0x09, 0x09, 0x09, 0x01],
    'G': [0x3E, 0x41, 0x49, 0x49, 0x7A],
    'H': [0x7F, 0x08, 0x08, 0x08, 0x7F],
    'I': [0x00, 0x41, 0x7F, 0x41, 0x00],
    'J': [0x20, 0x40, 0x41, 0x3F, 0x01],
    'K': [0x7F, 0x08, 0x14, 0x22, 0x41],
    'L': [0x7F, 0x40, 0x40, 0x40, 0x40],
    'M': [0x7F, 0x02, 0x0C, 0x02, 0x7F],
    'N': [0x7F, 0x04, 0x08, 0x10, 0x7F],
    'O': [0x3E, 0x41, 0x41, 0x41, 0x3E],
    'P': [0x7F, 0x09, 0x09, 0x09, 0x06],
    'Q': [0x3E, 0x41, 0x51, 0x21, 0x5E],
    'R': [0x7F, 0x09, 0x19, 0x29, 0x46],
    'S': [0x46, 0x49, 0x49, 0x49, 0x31],
    'T': [0x01, 0x01, 0x7F, 0x01, 0x01],
    'U': [0x3F, 0x40, 0x40, 0x40, 0x3F],
    'V': [0x1F, 0x20, 0x40, 0x20, 0x1F],
    'W': [0x3F, 0x40, 0x38, 0x40, 0x3F],
    'X': [0x63, 0x14, 0x08, 0x14, 0x63],
    'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
    'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
    'a': [0x20, 0x54, 0x54, 0x54, 0x78],
    'b': [0x7F, 0x48, 0x44, 0x44, 0x38],
    'c': [0x38, 0x44, 0x44, 0x44, 0x20],
    'd': [0x38, 0x44, 0x44, 0x48, 0x7F],
    'e': [0x38, 0x54, 0x54, 0x54, 0x18],
    'f': [0x08, 0x7E, 0x09, 0x01, 0x02],
    'g': [0x0C, 0x52, 0x52, 0x52, 0x3E],
    'h': [0x7F, 0x08, 0x04, 0x04, 0x78],
    'i': [0x00, 0x44, 0x7D, 0x40, 0x00],
    'j': [0x20, 0x40, 0x44, 0x3D, 0x00],
    'k': [0x7F, 0x10, 0x28, 0x44, 0x00],
    'l': [0x00, 0x41, 0x7F, 0x40, 0x00],
    'm': [0x7C, 0x04, 0x18, 0x04, 0x78],
    'n': [0x7C, 0x08, 0x04, 0x04, 0x78],
    'o': [0x38, 0x44, 0x44, 0x44, 0x38],
    'p': [0x7C, 0x14, 0x14, 0x14, 0x08],
    'q': [0x08, 0x14, 0x14, 0x18, 0x7C],
    'r': [0x7C, 0x08, 0x04, 0x04, 0x08],
    's': [0x48, 0x54, 0x54, 0x54, 0x20],
    't': [0x04, 0x3F, 0x44, 0x40, 0x20],
    'u': [0x3C, 0x40, 0x40, 0x20, 0x7C],
    'v': [0x1C, 0x20, 0x40, 0x20, 0x1C],
    'w': [0x3C, 0x40, 0x30, 0x40, 0x3C],
    'x': [0x44, 0x28, 0x10, 0x28, 0x44],
    'y': [0x0C, 0x50, 0x50, 0x50, 0x3C],
    'z': [0x44, 0x64, 0x54, 0x4C, 0x44],
    '[': [0x00, 0x7F, 0x41, 0x41, 0x00],
    ']': [0x00, 0x41, 0x41, 0x7F, 0x00],
    '_': [0x40, 0x40, 0x40, 0x40, 0x40],
    '|': [0x00, 0x00, 0x7F, 0x00, 0x00],
    '~': [0x08, 0x04, 0x08, 0x10, 0x08],
}


def _draw_char(ch, x, y, scale=2):
    """Draw a single bitmap character at pixel position (x, y)."""
    cols = _FONT.get(ch, _FONT['?'])
    for ci, col_bits in enumerate(cols):
        for ri in range(7):
            if col_bits & (1 << ri):        # bit 0 = top row in this font
                px = x + ci * scale
                py = y - ri * scale
                glBegin(GL_QUADS)
                glVertex2f(px,          py)
                glVertex2f(px + scale,  py)
                glVertex2f(px + scale,  py - scale)
                glVertex2f(px,          py - scale)
                glEnd()
    return x + (len(cols) + 1) * scale   # advance width


def _draw_string(text, x, y, scale=2):
    """Draw a string left-to-right; returns final x position."""
    cx = x
    for ch in text:
        cx = _draw_char(ch, cx, y, scale)
    return cx


class UserControls:
    """Encapsulates all user-control state for Member 5."""

    def __init__(self, planets):
        self.planets    = planets           # list of Planet objects
        self._speed_mag = DEFAULT_SPEED     # positive magnitude of speed
        self._reversed  = False             # is time going backwards?
        self._paused    = False             # pause flag
        self.selected   = None             # None = affect ALL planets

    # ── Properties ──────────────────────────────────────────────────────────

    @property
    def effective_scale(self):
        """Returns the actual dt multiplier used by main.py each frame."""
        if self._paused:
            return 0.0
        sign = -1 if self._reversed else 1
        return sign * self._speed_mag

    # ── Keyboard handler ────────────────────────────────────────────────────

    def key_callback(self, window, key, scancode, action, mods):
        """Pass this directly to glfw.set_key_callback()."""

        if action not in (glfw.PRESS, glfw.REPEAT):
            return

        # ── Exit ─────────────────────────────────────────────────────────────
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        # ── Speed up ─────────────────────────────────────────────────────────
        elif key in (glfw.KEY_UP, glfw.KEY_W):
            self._speed_mag = min(round(self._speed_mag + SPEED_STEP, 2),
                                  MAX_SPEED)
            self._paused = False
            self._print_status()

        # ── Slow down ────────────────────────────────────────────────────────
        elif key in (glfw.KEY_DOWN, glfw.KEY_S):
            new_mag = round(self._speed_mag - SPEED_STEP, 2)
            self._speed_mag = max(new_mag, MIN_SPEED)
            self._paused = False
            self._print_status()

        # ── Reverse time ─────────────────────────────────────────────────────
        elif key == glfw.KEY_R and action == glfw.PRESS:
            self._reversed = not self._reversed
            self._paused   = False
            self._print_status()

        # ── Pause / Resume ───────────────────────────────────────────────────
        elif key == glfw.KEY_SPACE and action == glfw.PRESS:
            self._paused = not self._paused
            self._print_status()

        # ── Reset speed ──────────────────────────────────────────────────────
        elif key in (glfw.KEY_ENTER, glfw.KEY_KP_ENTER,
                     glfw.KEY_BACKSPACE) and action == glfw.PRESS:
            self._speed_mag = DEFAULT_SPEED
            self._reversed  = False
            self._paused    = False
            self._print_status()

        # ── Select individual planet (keys 1-4) ──────────────────────────────
        elif glfw.KEY_1 <= key <= glfw.KEY_4 and action == glfw.PRESS:
            idx = key - glfw.KEY_1
            if idx < len(self.planets):
                if self.selected == idx:
                    self.selected = None
                    print("[Controls] Deselected - all planets targeted")
                else:
                    self.selected = idx
                    print(f"[Controls] Selected planet {idx + 1}")

        # ── Cycle selected planet with TAB ────────────────────────────────────
        elif key == glfw.KEY_TAB and action == glfw.PRESS:
            if self.selected is None:
                self.selected = 0
            else:
                self.selected = (self.selected + 1) % len(self.planets)
            print(f"[Controls] Selected planet {self.selected + 1}")

        # ── Resize bigger (+  or  =) ─────────────────────────────────────────
        elif key in (glfw.KEY_EQUAL, glfw.KEY_KP_ADD):
            self._resize(+SCALE_STEP)

        # ── Resize smaller (-) ───────────────────────────────────────────────
        elif key in (glfw.KEY_MINUS, glfw.KEY_KP_SUBTRACT):
            self._resize(-SCALE_STEP)

        # ── Reset planet sizes ────────────────────────────────────────────────
        elif key == glfw.KEY_0 and action == glfw.PRESS:
            for p in self.planets:
                p.scale = 1.0
            self.selected = None
            print("[Controls] All planet sizes reset to 1.0")

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _resize(self, delta):
        """Apply a scale delta to the selected planet or all planets."""
        targets = ([self.planets[self.selected]]
                   if self.selected is not None
                   else self.planets)
        for p in targets:
            p.scale = round(max(MIN_SCALE, min(MAX_SCALE, p.scale + delta)), 2)
        if self.selected is not None:
            print(f"[Controls] Planet {self.selected + 1} scale -> "
                  f"{self.planets[self.selected].scale:.2f}")
        else:
            sizes = ", ".join(f"{p.scale:.2f}" for p in self.planets)
            print(f"[Controls] All scales -> [{sizes}]")

    def _print_status(self):
        direction = "REVERSED" if self._reversed else "forward"
        state     = "PAUSED"   if self._paused   else f"{self._speed_mag:.2f}x"
        print(f"[Controls] Speed={state}  Direction={direction}")

    # ── HUD Rendering (GLUT-free) ─────────────────────────────────────────────

    def draw_hud(self, win_w, win_h):
        """
        Renders an on-screen HUD using raw OpenGL quads (no GLUT needed).
        Call this AFTER rendering the scene each frame, before swap_buffers().
        """
        # Switch to pixel-space 2-D overlay
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, win_w, 0, win_h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # ── Build content ────────────────────────────────────────────────────
        speed_str = "PAUSED"    if self._paused   else f"{self._speed_mag:.2f}x"
        dir_str   = "[REVERSE]" if self._reversed else "[forward]"

        # Colour-coded lines: (text, r, g, b)
        # Uppercase letters only ( font covers A-Z, a-z, digits, basic punct )
        lines = []
        lines.append(("USER CONTROLS", 1.0, 0.85, 0.2))
        lines.append(("-" * 18,         0.4, 0.4,  0.55))
        lines.append((f"Speed   : {speed_str}",
                      1.0 if self._paused else 0.85,
                      0.35 if self._paused else 0.85,
                      0.25 if self._paused else 0.95))
        lines.append((f"Dir     : {dir_str}",
                      1.0 if self._reversed else 0.85,
                      0.35 if self._reversed else 0.85,
                      0.25 if self._reversed else 0.95))
        lines.append(("", 0.0, 0.0, 0.0))
        lines.append(("Planets:", 1.0, 0.85, 0.2))
        for i, planet in enumerate(self.planets):
            marker = ">" if i == self.selected else " "
            r, g, b = (1.0, 0.85, 0.2) if i == self.selected else (0.75, 0.75, 0.9)
            lines.append((f" {marker} P{i+1} scale: {planet.scale:.2f}x", r, g, b))
        lines.append(("", 0.0, 0.0, 0.0))
        lines.append(("[/] speed  R rev  SPC pause", 0.5, 0.5, 0.65))
        lines.append(("[+/-] resize  1-4 sel  0 rst", 0.5, 0.5, 0.65))

        # ── Panel dimensions ─────────────────────────────────────────────────
        char_scale = 2
        char_w     = 6 * char_scale    # 5 cols + 1 gap
        char_h     = 8 * char_scale    # 7 rows + 1 gap
        pad        = 10
        max_chars  = max(len(t) for t, *_ in lines)
        panel_w    = pad * 2 + max_chars * char_w + 6
        panel_h    = pad * 2 + len(lines) * char_h + 4
        x0         = 12
        y0         = win_h - 12 - panel_h

        # ── Background panel ─────────────────────────────────────────────────
        glColor4f(0.02, 0.02, 0.12, 0.72)
        glBegin(GL_QUADS)
        glVertex2f(x0,           y0)
        glVertex2f(x0 + panel_w, y0)
        glVertex2f(x0 + panel_w, y0 + panel_h)
        glVertex2f(x0,           y0 + panel_h)
        glEnd()

        # Panel border
        glColor4f(0.3, 0.3, 0.6, 0.8)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x0,           y0)
        glVertex2f(x0 + panel_w, y0)
        glVertex2f(x0 + panel_w, y0 + panel_h)
        glVertex2f(x0,           y0 + panel_h)
        glEnd()

        # ── Draw each text line ──────────────────────────────────────────────
        text_x  = x0 + pad
        text_y  = y0 + panel_h - pad - char_h + 2   # top line baseline
        for text, r, g, b in lines:
            if text:
                glColor3f(r, g, b)
                _draw_string(text, text_x, text_y, scale=char_scale)
            text_y -= char_h

        # ── Restore matrices ────────────────────────────────────────────────
        glDisable(GL_BLEND)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    # ── Help / manual overlay (bottom-right) ─────────────────────────────────

    def draw_help(self, win_w, win_h):
        """
        Renders a static key-guide ("manual") panel in the bottom-right corner.
        Call this AFTER rendering the scene each frame, before swap_buffers().
        """
        # The on-screen manual mirrors the console key list.
        help_lines = [
            ("USER GUIDE",          1.0, 0.85, 0.2),
            ("-" * 22,              0.4, 0.4,  0.55),
            ("UP / W      Speed up",   0.8, 0.8, 0.95),
            ("DOWN / S    Slow down",  0.8, 0.8, 0.95),
            ("R           Reverse",    0.8, 0.8, 0.95),
            ("SPACE       Pause",      0.8, 0.8, 0.95),
            ("ENTER       Reset speed", 0.8, 0.8, 0.95),
            ("1 - 4       Select",     0.8, 0.8, 0.95),
            ("TAB         Cycle",      0.8, 0.8, 0.95),
            ("+ / -       Resize",     0.8, 0.8, 0.95),
            ("0           Reset size", 0.8, 0.8, 0.95),
            ("I / O       Zoom",       0.8, 0.8, 0.95),
            ("ESC         Quit",       0.9, 0.5, 0.5),
        ]

        # Switch to pixel-space 2-D overlay
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, win_w, 0, win_h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # ── Panel dimensions ─────────────────────────────────────────────────
        char_scale = 2
        char_w     = 6 * char_scale    # 5 cols + 1 gap
        char_h     = 8 * char_scale    # 7 rows + 1 gap
        pad        = 10
        max_chars  = max(len(t) for t, *_ in help_lines)
        panel_w    = pad * 2 + max_chars * char_w + 6
        panel_h    = pad * 2 + len(help_lines) * char_h + 4
        x0         = win_w - 12 - panel_w   # anchored to the right edge
        y0         = 12                      # anchored to the bottom edge

        # ── Background panel ─────────────────────────────────────────────────
        glColor4f(0.02, 0.02, 0.12, 0.72)
        glBegin(GL_QUADS)
        glVertex2f(x0,           y0)
        glVertex2f(x0 + panel_w, y0)
        glVertex2f(x0 + panel_w, y0 + panel_h)
        glVertex2f(x0,           y0 + panel_h)
        glEnd()

        # Panel border
        glColor4f(0.3, 0.3, 0.6, 0.8)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x0,           y0)
        glVertex2f(x0 + panel_w, y0)
        glVertex2f(x0 + panel_w, y0 + panel_h)
        glVertex2f(x0,           y0 + panel_h)
        glEnd()

        # ── Draw each text line ──────────────────────────────────────────────
        text_x  = x0 + pad
        text_y  = y0 + panel_h - pad - char_h + 2   # top line baseline
        for text, r, g, b in help_lines:
            if text:
                glColor3f(r, g, b)
                _draw_string(text, text_x, text_y, scale=char_scale)
            text_y -= char_h

        # ── Restore matrices ────────────────────────────────────────────────
        glDisable(GL_BLEND)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
