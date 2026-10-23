"""Procedural Vector Cartoon Character Engine Core
Provides color definitions, canvas geometry helpers, math curves, and utilities.
"""

import math
import cairo

# ---------- Color Palette ----------
C = {
    'bg': (1.0, 0.97, 0.925),
    'navy': (0.15, 0.23, 0.35),
    'dark': (0.12, 0.14, 0.18),
    'teal': (0.30, 0.71, 0.67),
    'teal2': (0.22, 0.56, 0.53),
    'orange': (1.0, 0.54, 0.40),
    'yellow': (1.0, 0.84, 0.31),
    'red': (0.90, 0.35, 0.35),
    'pink': (1.0, 0.66, 0.70),
    'screen': (0.88, 0.97, 0.98),
    'blue': (0.35, 0.60, 0.92),
    'green': (0.36, 0.74, 0.42),
    'forest': (0.18, 0.45, 0.28),
    'grey': (0.75, 0.78, 0.82),
    'lightgrey': (0.92, 0.93, 0.95),
    'white': (1.0, 1.0, 1.0),
    'black': (0.05, 0.05, 0.08),
}

# Standard Skin & Hair Palettes
SKIN_DEFAULT = (1.0, 0.86, 0.72)
SKIN_WARM = (0.96, 0.80, 0.66)
SKIN_SHADOW = (0.88, 0.72, 0.60)
HAIR_DARK = (0.20, 0.16, 0.22)
HAIR_BROWN = (0.30, 0.20, 0.15)

FONT_DEFAULT = "Noto Sans CJK TC"

# ---------- Math & Animation Easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def ease_out(x):
    x = clamp(x)
    return 1.0 - (1.0 - x) ** 3

def back_out(x, c1=1.9):
    c3 = c1 + 1.0
    x = clamp(x)
    return 1.0 + c3 * (x - 1.0) ** 3 + c1 * (x - 1.0) ** 2

# ---------- Vector Drawing Primitives ----------
def rrect(ctx, x, y, w, h, r):
    """Draws a rounded rectangle path."""
    r = min(r, w / 2.0, h / 2.0)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2.0, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2.0)
    ctx.arc(x + r, y + h - r, r, math.pi / 2.0, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()

def fillstroke(ctx, fill, stroke=C['navy'], lw=5.0, a=1.0):
    """Fills and strokes current path with consistent line weight."""
    ctx.set_source_rgba(*fill, a)
    ctx.fill_preserve()
    ctx.set_source_rgba(*stroke, a)
    ctx.set_line_width(lw)
    ctx.stroke()

def star(ctx, x, y, r, col=C['yellow'], a=1.0, rot=0.0, outline=False, lw=3.0):
    """Draws a 5-pointed sparkling star."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        ang = -math.pi / 2.0 + k * math.pi / 5.0
        if k == 0:
            ctx.move_to(math.cos(ang) * rr, math.sin(ang) * rr)
        else:
            ctx.line_to(math.cos(ang) * rr, math.sin(ang) * rr)
    ctx.close_path()
    ctx.set_source_rgba(*col, a)
    if outline:
        ctx.fill_preserve()
        ctx.set_source_rgba(*C['navy'], a)
        ctx.set_line_width(lw)
        ctx.stroke()
    else:
        ctx.fill()
    ctx.restore()

def text(ctx, s, x, y, size, col=C['navy'], bold=True, align='c', font=FONT_DEFAULT, a=1.0):
    """Renders aligned vector text."""
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    e = ctx.text_extents(s)
    dx = {'c': -e.x_advance / 2.0, 'l': 0.0, 'r': -e.x_advance}.get(align, 0.0)
    ctx.move_to(x + dx, y + size * 0.36)
    ctx.set_source_rgba(*col, a)
    ctx.show_text(s)
    ctx.new_path()
    return e.x_advance
