"""AI 小博士 (Doctor) — 經典科普與教學解說員角色
身穿白色實驗袍、橘色領帶、胸前口袋插著雙色筆、圓框眼鏡、天線呆毛、手持星光教鞭。
"""

import math
import cairo
from core import C, SKIN_DEFAULT, HAIR_DARK, rrect, fillstroke, star

COAT = (0.98, 0.98, 1.0)
COAT_SHADOW = (0.80, 0.84, 0.90)

def doctor(ctx, x, y, s, t, mouth=0.0, wave=False, point=False, sweat=False, happy=True, look=0.0):
    """
    AI 小博士 (Doctor)
    ctx   : Cairo Context
    x, y  : 角色錨點座標
    s     : 縮放比例 (scale)
    t     : 動畫全片時間 (秒)
    mouth : 語音音量振幅 (0.0 ~ 1.0)
    wave  : 是否做出揮手動作 (True / False)
    point : 是否做出持教鞭導引動作 (True / False)
    sweat : 是否流汗汗滴 (True / False)
    happy : 是否微笑/開心 (True) 或是嚴肅/沮喪 (False)
    look  : 視線偏移量 (-1.0 向左看 ~ 1.0 向右看)
    """
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # 1. 腳底陰影
    ctx.save()
    ctx.scale(1.0, 0.18)
    ctx.arc(0, 250 / 0.18, 100, 0, 2 * math.pi)
    ctx.set_source_rgba(0, 0, 0, 0.10)
    ctx.fill()
    ctx.restore()

    # 2. 呼吸起伏與微晃動態 (Bobbing & Tilt)
    bob = -abs(math.sin(t * 4.2)) * 12
    ctx.translate(0, bob + 200)
    ctx.rotate(math.sin(t * 2.1) * 0.05)
    ctx.translate(0, -200)

    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)

    # 3. 雙腿與皮鞋
    for sd in (-1, 1):
        ctx.move_to(sd * 26, 200)
        ctx.line_to(sd * 28, 236)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(20)
        ctx.stroke()
        rrect(ctx, sd * 28 - 22 + sd * 6, 228, 44, 20, 10)
        fillstroke(ctx, (0.95, 0.45, 0.35), stroke=C['navy'], lw=4)

    # 4. 軀幹：白大褂實驗袍 (Lab Coat)
    ctx.move_to(-60, 86)
    ctx.curve_to(-76, 150, -84, 192, -80, 212)
    ctx.line_to(80, 212)
    ctx.curve_to(84, 192, 76, 150, 60, 86)
    ctx.curve_to(30, 74, -30, 74, -60, 86)
    ctx.close_path()
    fillstroke(ctx, COAT, stroke=C['navy'], lw=5)

    # 5. 內著襯衫與領帶
    ctx.move_to(-22, 82)
    ctx.line_to(0, 140)
    ctx.line_to(22, 82)
    ctx.close_path()
    fillstroke(ctx, (0.55, 0.75, 0.95), stroke=C['navy'], lw=4)

    # 橘色領帶
    ctx.move_to(-7, 92)
    ctx.line_to(7, 92)
    ctx.line_to(10, 128)
    ctx.line_to(0, 140)
    ctx.line_to(-10, 128)
    ctx.close_path()
    fillstroke(ctx, C['orange'], stroke=C['navy'], lw=3)

    # 實驗袍領口細節
    for sd in (-1, 1):
        ctx.move_to(sd * 22, 82)
        ctx.line_to(sd * 46, 84)
        ctx.line_to(sd * 20, 150)
        ctx.close_path()
        fillstroke(ctx, COAT_SHADOW, stroke=C['navy'], lw=4)

    # 胸前口袋與筆 (Blue / Red Pens)
    rrect(ctx, 26, 156, 36, 30, 5)
    fillstroke(ctx, COAT_SHADOW, stroke=C['navy'], lw=3)
    ctx.move_to(36, 150)
    ctx.line_to(36, 170)
    ctx.set_source_rgb(*C['blue'])
    ctx.set_line_width(5)
    ctx.stroke()
    ctx.move_to(48, 150)
    ctx.line_to(48, 168)
    ctx.set_source_rgb(*C['red'])
    ctx.set_line_width(5)
    ctx.stroke()

    # 6. 橡皮管手臂與手部動作 (Rubberhose Arms)
    def arm(sx, sy, ex, ey):
        ctx.move_to(sx, sy)
        ctx.line_to(ex, ey)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(26)
        ctx.stroke()
        ctx.move_to(sx, sy)
        ctx.line_to(ex, ey)
        ctx.set_source_rgb(*COAT)
        ctx.set_line_width(17)
        ctx.stroke()
        ctx.arc(ex, ey, 13, 0, 2 * math.pi)
        fillstroke(ctx, SKIN_DEFAULT, stroke=C['navy'], lw=4)

    # 左手（畫面左側）動作分支
    if wave:
        ang = -2.3 + 0.4 * math.sin(t * 9)
        arm(-64, 108, -64 + math.cos(ang) * 72, 108 + math.sin(ang) * 72)
    else:
        arm(-64, 108, -84, 172)

    # 右手（畫面右側）動作分支：持星光教鞭
    if point:
        ex, ey = 130, 40 + math.sin(t * 3) * 6
        arm(64, 108, ex, ey)
        # 木質教鞭
        ctx.move_to(ex, ey)
        ctx.line_to(ex + 70, ey - 60)
        ctx.set_source_rgb(0.55, 0.33, 0.18)
        ctx.set_line_width(7)
        ctx.stroke()
        # 教鞭尖端星光閃爍
        star(ctx, ex + 76, ey - 66, 16, C['yellow'], 1.0, rot=t * 2, outline=True)
    else:
        arm(64, 108, 86, 172)

    # 7. 頭部輪廓與雙耳
    for sd in (-1, 1):
        ctx.arc(sd * 86, 0, 16, 0, 2 * math.pi)
        fillstroke(ctx, SKIN_DEFAULT, stroke=C['navy'], lw=4)
    ctx.arc(0, -10, 86, 0, 2 * math.pi)
    fillstroke(ctx, SKIN_DEFAULT, stroke=C['navy'], lw=5)

    # 8. 髮型：蓬鬆短髮與天線呆毛
    ctx.move_to(-90, -20)
    for k, (hx, hy) in enumerate([(-92, -70), (-60, -104), (-20, -112), (20, -112), (60, -104), (92, -70)]):
        ctx.curve_to(hx - 10, hy - 18, hx + 18, hy - 22, hx + 14, hy)
    ctx.line_to(90, -20)
    ctx.curve_to(70, -60, 40, -66, 0, -62)
    ctx.curve_to(-40, -66, -70, -60, -90, -20)
    ctx.close_path()
    fillstroke(ctx, HAIR_DARK, stroke=C['navy'], lw=5)

    # 天線呆毛 (Antenna Tuft with wobble)
    ctx.move_to(0, -112)
    ctx.curve_to(10, -150, 40, -150, 34, -128 + math.sin(t * 5) * 4)
    ctx.set_source_rgb(*HAIR_DARK)
    ctx.set_line_width(8)
    ctx.stroke()

    # 9. 眼鏡與自然眨眼 (Glasses & Blinking Eyes)
    blink = (t % 3.1) < 0.13
    for ex_ in (-34, 34):
        ctx.save()
        ctx.translate(ex_ + look * 6, -2)
        ctx.scale(1.0, 0.12 if blink else 1.0)
        ctx.arc(0, 0, 12, 0, 2 * math.pi)
        ctx.set_source_rgb(*C['navy'])
        ctx.fill()
        if not blink:
            # 眼神活力高光
            ctx.arc(4, -5, 4.5, 0, 2 * math.pi)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()
        ctx.restore()

        # 圓鏡框與半透明反光鏡片
        ctx.arc(ex_, -2, 27, 0, 2 * math.pi)
        ctx.set_source_rgba(0.8, 0.93, 1.0, 0.25)
        ctx.fill_preserve()
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(5)
        ctx.stroke()

    # 眼鏡中樑 (Bridge)
    ctx.move_to(-8, -4)
    ctx.curve_to(-4, -12, 4, -12, 8, -4)
    ctx.set_line_width(5)
    ctx.stroke()

    # 10. 雙頰可愛腮紅
    for ex_ in (-54, 54):
        ctx.arc(ex_, 32, 11, 0, 2 * math.pi)
        ctx.set_source_rgba(*C['pink'], 0.75)
        ctx.fill()

    # 11. 語音連動嘴型 (Mouth opening sync to RMS volume)
    if mouth > 0.08:
        ctx.save()
        ctx.translate(0, 44)
        ctx.scale(1.0, (4 + 18 * mouth) / 13)
        ctx.arc(0, 0, 13, 0, 2 * math.pi)
        ctx.restore()
        ctx.set_source_rgb(*C['navy'])
        ctx.fill()
    else:
        if happy:
            ctx.arc(0, 34, 15, 0.15 * math.pi, 0.85 * math.pi)
        else:
            ctx.arc(0, 56, 12, 1.2 * math.pi, 1.8 * math.pi)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(5)
        ctx.stroke()

    # 12. 汗滴特效 (Sweat Drop)
    if sweat:
        dy = (t * 40) % 30
        ctx.move_to(92, -40 + dy)
        ctx.curve_to(76, -12 + dy, 80, 0 + dy, 92, 0 + dy)
        ctx.curve_to(104, 0 + dy, 108, -12 + dy, 92, -40 + dy)
        fillstroke(ctx, (0.55, 0.80, 1.0), stroke=C['navy'], lw=3)

    ctx.restore()
