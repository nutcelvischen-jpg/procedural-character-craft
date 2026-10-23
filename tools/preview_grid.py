"""Action & Expression 9-State Matrix Preview Generator
Renders a 3x3 high-resolution contact sheet testing all states of a procedural character.
"""

import os
import sys
import math
import cairo

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import C, fillstroke, rrect, text
from characters import CHARACTERS

STATES = [
    {"label": "1. 正常待機 (Idle)", "kw": {"t": 0.0, "mouth": 0.0, "happy": True}},
    {"label": "2. 語音連動 (Talking)", "kw": {"t": 0.5, "mouth": 0.75, "happy": True}},
    {"label": "3. 揮手打招呼 (Wave)", "kw": {"t": 1.25, "wave": True, "happy": True}},
    {"label": "4. 指物/持教鞭 (Point)", "kw": {"t": 0.8, "point": True, "happy": True}},
    {"label": "5. 開心微笑 (Happy)", "kw": {"t": 0.0, "mouth": 0.0, "happy": True}},
    {"label": "6. 嚴肅/驚訝 (Serious)", "kw": {"t": 0.0, "mouth": 0.0, "happy": False}},
    {"label": "7. 緊張流汗 (Sweat)", "kw": {"t": 0.35, "sweat": True, "happy": False}},
    {"label": "8. 視線向左 (Look Left)", "kw": {"t": 0.0, "look": -1.0, "happy": True}},
    {"label": "9. 視線向右 (Look Right)", "kw": {"t": 0.0, "look": 1.0, "happy": True}},
]

def render_grid(char_name, out_path):
    if char_name not in CHARACTERS:
        raise ValueError(f"Unknown character '{char_name}'. Available: {list(CHARACTERS.keys())}")
    
    char_func = CHARACTERS[char_name]
    
    cell_w, cell_h = 420, 480
    cols, rows = 3, 3
    padding_top = 100
    total_w = cell_w * cols + 40
    total_h = cell_h * rows + padding_top + 40

    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, total_w, total_h)
    ctx = cairo.Context(surf)

    # Background
    ctx.set_source_rgb(*C['bg'])
    ctx.paint()

    # Title Banner
    text(ctx, f"Procedural Character Matrix — {char_name.capitalize()}",
         total_w / 2.0, 45, 34, C['navy'], bold=True)
    text(ctx, "9-State Procedural Vector Animation Verification Sheet",
         total_w / 2.0, 78, 16, (0.45, 0.52, 0.62), bold=False)

    for i, state in enumerate(STATES):
        col = i % cols
        row = i // cols
        x0 = 20 + col * cell_w
        y0 = padding_top + row * cell_h

        # Cell card background
        rrect(ctx, x0 + 10, y0 + 10, cell_w - 20, cell_h - 20, 16)
        fillstroke(ctx, C['white'], stroke=C['lightgrey'], lw=2.5)

        # Label tag
        rrect(ctx, x0 + 24, y0 + 24, cell_w - 48, 36, 8)
        fillstroke(ctx, (0.94, 0.96, 0.99), stroke=(0.82, 0.88, 0.94), lw=1.5)
        text(ctx, state["label"], x0 + cell_w / 2.0, y0 + 42, 16, C['navy'], bold=True)

        # Draw Character in cell
        char_cx = x0 + cell_w / 2.0
        char_cy = y0 + 240
        char_func(ctx, char_cx, char_cy, 0.52, **state["kw"])

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    surf.write_to_png(out_path)
    print(f"✓ Saved 9-state matrix to: {out_path}")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'doctor'
    out = sys.argv[2] if len(sys.argv) > 2 else f"assets/matrix_{target}.png"
    render_grid(target, out)
