"""Animated GIF Preview Generator
Renders a 3-second animated loop of a procedural character speaking and gesturing.
"""

import os
import sys
import math
import numpy as np
from PIL import Image
import cairo

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import C, rrect, fillstroke, text
from characters import CHARACTERS

def render_gif(char_name, out_path, duration=3.0, fps=24):
    if char_name not in CHARACTERS:
        raise ValueError(f"Unknown character '{char_name}'")
    
    char_func = CHARACTERS[char_name]
    total_frames = int(duration * fps)
    w, h = 480, 560
    frames = []

    print(f"Rendering {total_frames} frames for {char_name} animated GIF...")

    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)

    for frame_idx in range(total_frames):
        t = frame_idx / fps

        # Background
        ctx.set_source_rgb(*C['bg'])
        ctx.paint()

        # Decorative card
        rrect(ctx, 16, 16, w - 32, h - 32, 20)
        fillstroke(ctx, C['white'], stroke=C['lightgrey'], lw=3.0)

        # Name badge
        text(ctx, f"• {char_name.upper()} •", w / 2.0, 48, 20, C['navy'], bold=True)

        # Dynamic state schedule
        # Wave in first half, Point in second half
        wave = (t < 1.4)
        point = (t >= 1.6)
        
        # Talking mouth simulation (rhythmic opening and closing)
        mouth = max(0.0, math.sin(t * 11) * 0.9) if (0.3 < t < 2.7) else 0.0
        
        # Look drift
        look = math.sin(t * 2.5) * 0.8

        # Render Character
        char_func(ctx, w / 2.0, h / 2.0 + 35, 0.65, t,
                  mouth=mouth, wave=wave, point=point, sweat=False, happy=True, look=look)

        # Convert Cairo surface to Pillow Image
        data = surf.get_data()
        img_np = np.ndarray(shape=(h, w, 4), dtype=np.uint8, buffer=data)
        # Cairo ARGB32 on little-endian macOS is BGRA
        img_rgba = img_np[:, :, [2, 1, 0, 3]]
        pil_img = Image.fromarray(img_rgba, mode='RGBA')
        frames.append(pil_img.convert('P', palette=Image.Palette.ADAPTIVE))

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True
    )
    print(f"✓ Saved animated GIF to: {out_path}")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'doctor'
    out = sys.argv[2] if len(sys.argv) > 2 else f"assets/demo_{target}.gif"
    render_gif(target, out)
