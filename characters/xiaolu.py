"""智慧導覽員・小綠 (Xiaolu)
親和力滿滿的專業導覽大使，身穿湖水綠/青色西裝夾克、佩戴導覽證件、頭戴經典導覽貝雷帽、手持簡報器或揮手歡迎！
"""

import math
import cairo
from core import C, SKIN_WARM, rrect, fillstroke, star, text

# 小綠色彩盤
CAP_TEAL = (0.20, 0.65, 0.60)
CAP_DARK = (0.15, 0.48, 0.44)
JACKET_TEAL = (0.24, 0.68, 0.62)
SHIRT_WHITE = (0.98, 0.98, 1.0)
SKIRT_DARK = (0.16, 0.25, 0.35)
LANYARD_ORANGE = (1.0, 0.55, 0.35)
HAIR_XIAOLU = (0.25, 0.18, 0.22)

def xiaolu(ctx, x, y, s, t, mouth=0.0, wave=False, point=False, sweat=False, happy=True, look=0.0):
    """
    智慧導覽員・小綠 (Xiaolu)
    """
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # 1. 腳底陰影
    ctx.save()
    ctx.scale(1.0, 0.18)
    ctx.arc(0, 250 / 0.18, 95, 0, 2 * math.pi)
    ctx.set_source_rgba(0, 0, 0, 0.10)
    ctx.fill()
    ctx.restore()

    # 2. 呼吸起伏
    bob = -abs(math.sin(t * 4.2)) * 11
    ctx.translate(0, bob + 200)
    ctx.rotate(math.sin(t * 2.1) * 0.04)
    ctx.translate(0, -200)

    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)

    # 3. 雙腿與制服便鞋
    for sd in (-1, 1):
        ctx.move_to(sd * 24, 198)
        ctx.line_to(sd * 26, 234)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(18)
        ctx.stroke()
        rrect(ctx, sd * 26 - 18 + sd * 4, 226, 38, 20, 9)
        fillstroke(ctx, C['dark'], stroke=C['navy'], lw=3.5)

    # 4. 軀幹：內著襯衫 + 導覽夾克
    rrect(ctx, -52, 86, 104, 116, 22)
    fillstroke(ctx, SHIRT_WHITE, stroke=C['navy'], lw=5)

    # 夾克左右前襟
    for sd in (-1, 1):
        ctx.move_to(sd * 12, 86)
        ctx.line_to(sd * 52, 86)
        ctx.line_to(sd * 50, 198)
        ctx.line_to(sd * 16, 198)
        ctx.close_path()
        fillstroke(ctx, JACKET_TEAL, stroke=C['navy'], lw=4)

    # 橘色識別掛繩與胸前證件牌
    ctx.move_to(-16, 86)
    ctx.line_to(0, 142)
    ctx.line_to(16, 86)
    ctx.set_source_rgb(*LANYARD_ORANGE)
    ctx.set_line_width(5)
    ctx.stroke()
    rrect(ctx, -14, 142, 28, 36, 4)
    fillstroke(ctx, C['white'], stroke=C['navy'], lw=2.5)
    rrect(ctx, -10, 146, 20, 10, 2)
    fillstroke(ctx, C['teal'], stroke=C['navy'], lw=1.5)

    # 5. 手臂動作分支
    def arm(sx, sy, ex, ey):
        ctx.move_to(sx, sy)
        ctx.line_to(ex, ey)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(24)
        ctx.stroke()
        ctx.move_to(sx, sy)
        ctx.line_to(ex, ey)
        ctx.set_source_rgb(*JACKET_TEAL)
        ctx.set_line_width(16)
        ctx.stroke()
        ctx.arc(ex, ey, 12, 0, 2 * math.pi)
        fillstroke(ctx, SKIN_WARM, stroke=C['navy'], lw=4)

    # 左手揮手歡迎或垂放
    if wave:
        ang = -2.3 + 0.4 * math.sin(t * 9)
        arm(-60, 106, -60 + math.cos(ang) * 72, 106 + math.sin(ang) * 72)
    else:
        arm(-60, 106, -78, 170)

    # 右手指物導引
    if point:
        ex, ey = 126, 42 + math.sin(t * 3) * 6
        arm(60, 106, ex, ey)
        # 智慧簡報筆與雷射亮點
        ctx.move_to(ex, ey)
        ctx.line_to(ex + 24, ey - 14)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(7)
        ctx.stroke()
        star(ctx, ex + 34, ey - 22, 14, C['teal'], 1.0, rot=t * 2, outline=True)
    else:
        arm(60, 106, 78, 170)

    # 6. 頭部與雙耳
    for sd in (-1, 1):
        ctx.arc(sd * 82, 2, 15, 0, 2 * math.pi)
        fillstroke(ctx, SKIN_WARM, stroke=C['navy'], lw=4)
    ctx.arc(0, -6, 82, 0, 2 * math.pi)
    fillstroke(ctx, SKIN_WARM, stroke=C['navy'], lw=5)

    # 7. 齊瀏海柔和短髮
    ctx.move_to(-86, -10)
    ctx.curve_to(-80, -65, -45, -96, 0, -96)
    ctx.curve_to(45, -96, 80, -65, 86, -10)
    ctx.curve_to(65, -35, 30, -42, 0, -40)
    ctx.curve_to(-30, -42, -65, -35, -86, -10)
    ctx.close_path()
    fillstroke(ctx, HAIR_XIAOLU, stroke=C['navy'], lw=5)

    # 8. 眼睛眨眼與視線
    blink = (t % 3.6) < 0.13
    for ex_ in (-28, 28):
        ctx.save()
        ctx.translate(ex_ + look * 6, 4)
        ctx.scale(1.0, 0.12 if blink else 1.0)
        ctx.arc(0, 0, 11, 0, 2 * math.pi)
        ctx.set_source_rgb(*C['navy'])
        ctx.fill()
        if not blink:
            ctx.arc(4, -4, 4.0, 0, 2 * math.pi)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()
            ctx.arc(-3, 3, 2.0, 0, 2 * math.pi)
            ctx.fill()
        ctx.restore()

    # 9. 腮紅
    for ex_ in (-46, 46):
        ctx.arc(ex_, 32, 11, 0, 2 * math.pi)
        ctx.set_source_rgba(*C['pink'], 0.75)
        ctx.fill()

    # 10. 嘴型
    if mouth > 0.08:
        ctx.save()
        ctx.translate(0, 42)
        ctx.scale(1.0, (4 + 18 * mouth) / 13)
        ctx.arc(0, 0, 12, 0, 2 * math.pi)
        ctx.restore()
        ctx.set_source_rgb(*C['navy'])
        ctx.fill()
    else:
        if happy:
            ctx.arc(0, 32, 14, 0.15 * math.pi, 0.85 * math.pi)
        else:
            ctx.arc(0, 52, 11, 1.2 * math.pi, 1.8 * math.pi)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(4.5)
        ctx.stroke()

    # 11. 經典湖水綠導覽帽 (Beret / Guide Cap)
    ctx.save()
    ctx.translate(0, -78)
    ctx.rotate(0.08)
    # 貝雷帽圓弧帽身
    ctx.move_to(-88, 12)
    ctx.curve_to(-94, -30, -45, -52, 10, -52)
    ctx.curve_to(75, -52, 98, -25, 92, 12)
    ctx.curve_to(40, 22, -40, 22, -88, 12)
    ctx.close_path()
    fillstroke(ctx, CAP_TEAL, stroke=C['navy'], lw=4.5)

    # 帽子金質導覽徽章
    ctx.arc(-26, -14, 8, 0, 2 * math.pi)
    fillstroke(ctx, C['yellow'], stroke=C['navy'], lw=2.5)
    ctx.restore()

    # 12. 汗滴
    if sweat:
        dy = (t * 40) % 30
        ctx.move_to(88, -20 + dy)
        ctx.curve_to(74, 8 + dy, 78, 20 + dy, 88, 20 + dy)
        ctx.curve_to(100, 20 + dy, 104, 8 + dy, 88, -20 + dy)
        fillstroke(ctx, (0.55, 0.80, 1.0), stroke=C['navy'], lw=3)

    ctx.restore()
