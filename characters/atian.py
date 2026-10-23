"""在地導遊・阿天 (A-Tian)
陽光開朗的戶外青年導遊，戴卡其漁夫遮陽帽、竹葉徽章、穿綠色健行背心，拿著飄揚的導遊旗！
"""

import math
import cairo
from core import C, SKIN_DEFAULT, rrect, fillstroke, star, text

# 阿天專屬色彩盤
HAT_COLOR = (0.86, 0.80, 0.68)      # 卡其遮陽帽
HAT_BAND = (0.22, 0.48, 0.32)       # 墨綠帽帶
HAIR_ATIAN = (0.24, 0.18, 0.14)     # 深棕短髮
VEST_ATIAN = (0.26, 0.56, 0.38)     # 戶外山林綠背心
VEST_DARK = (0.18, 0.42, 0.28)      # 背心滾邊深綠
TEE_INNER = (0.98, 0.96, 0.90)      # 內搭米白 T 恤
PANTS_ATIAN = (0.76, 0.66, 0.52)    # 戶外卡其褲
BOOTS_COLOR = (0.42, 0.26, 0.16)    # 登山短靴

def bamboo_leaf_badge(ctx, x, y, s=1.0):
    """帽帶上的竹葉徽章"""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rotate(-0.3)
    for ang, dx, col in [(-0.4, -4, C['green']), (0.3, 4, C['yellow'])]:
        ctx.save()
        ctx.rotate(ang)
        ctx.move_to(0, -12)
        ctx.curve_to(8, -6, 8, 6, 0, 12)
        ctx.curve_to(-8, 6, -8, -6, 0, -12)
        ctx.close_path()
        fillstroke(ctx, col, stroke=C['navy'], lw=2.2)
        ctx.restore()
    ctx.restore()

def flag_atian(ctx, hx, hy, t, ang=-1.45, L=175, d=1):
    """飄揚的導遊旗"""
    ex, ey = hx + math.cos(ang) * L, hy + math.sin(ang) * L
    # 木質旗桿
    ctx.move_to(hx, hy)
    ctx.line_to(ex, ey)
    ctx.set_source_rgb(*C['navy'])
    ctx.set_line_width(9)
    ctx.stroke()
    ctx.move_to(hx, hy)
    ctx.line_to(ex, ey)
    ctx.set_source_rgb(0.82, 0.68, 0.42)
    ctx.set_line_width(5)
    ctx.stroke()

    # 旗桿頂端小金球
    ctx.arc(ex, ey - 4, 8, 0, 2 * math.pi)
    fillstroke(ctx, C['yellow'], stroke=C['navy'], lw=3)

    # 飄動旗面
    f = math.sin(t * 7) * 8
    ctx.move_to(ex, ey)
    ctx.curve_to(ex + d * 45, ey - 8 + f, ex + d * 80, ey + 6 - f, ex + d * 118, ey + 24 + f * 0.5)
    ctx.curve_to(ex + d * 80, ey + 42 + f, ex + d * 45, ey + 56 - f, ex + d * 4, ey + 62)
    ctx.close_path()
    fillstroke(ctx, C['yellow'], stroke=C['navy'], lw=4)

    # 旗幟文字「導遊」
    text(ctx, "導遊", ex + d * 48, ey + 32 + f * 0.3, 18, C['navy'], bold=True)

def atian(ctx, x, y, s, t, mouth=0.0, wave=False, point=False, sweat=False, happy=True, look=0.0):
    """
    小半天導遊・阿天 (A-Tian)
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

    # 2. 呼吸起伏
    bob = -abs(math.sin(t * 4.2)) * 12
    ctx.translate(0, bob + 200)
    ctx.rotate(math.sin(t * 2.1) * 0.05)
    ctx.translate(0, -200)

    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)

    # 3. 雙腿與短靴
    for sd in (-1, 1):
        ctx.move_to(sd * 26, 196)
        ctx.line_to(sd * 28, 234)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(20)
        ctx.stroke()
        ctx.move_to(sd * 26, 196)
        ctx.line_to(sd * 28, 234)
        ctx.set_source_rgb(*PANTS_ATIAN)
        ctx.set_line_width(12)
        ctx.stroke()
        rrect(ctx, sd * 28 - 22 + sd * 6, 226, 44, 22, 10)
        fillstroke(ctx, BOOTS_COLOR, stroke=C['navy'], lw=4)

    # 4. 軀幹與綠背心
    rrect(ctx, -56, 84, 112, 122, 24)
    fillstroke(ctx, TEE_INNER, stroke=C['navy'], lw=5)

    # 綠背心左片與右片
    for sd in (-1, 1):
        ctx.move_to(sd * 10, 84)
        ctx.line_to(sd * 56, 84)
        ctx.line_to(sd * 56, 204)
        ctx.line_to(sd * 14, 204)
        ctx.close_path()
        fillstroke(ctx, VEST_ATIAN, stroke=C['navy'], lw=4)
        # 背心翻領口袋
        rrect(ctx, sd * 36 - 12, 150, 24, 26, 4)
        fillstroke(ctx, VEST_DARK, stroke=C['navy'], lw=2.5)

    # 5. 手臂動作分支
    def arm(sx, sy, ex, ey):
        ctx.move_to(sx, sy)
        ctx.line_to(ex, ey)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(26)
        ctx.stroke()
        ctx.move_to(sx, sy)
        ctx.line_to(ex, ey)
        ctx.set_source_rgb(*TEE_INNER)
        ctx.set_line_width(17)
        ctx.stroke()
        ctx.arc(ex, ey, 13, 0, 2 * math.pi)
        fillstroke(ctx, SKIN_DEFAULT, stroke=C['navy'], lw=4)

    # 左手拿導遊旗或揮動
    hx, hy = -64, 108
    if wave:
        ang = -2.3 + 0.4 * math.sin(t * 9)
        ex, ey = hx + math.cos(ang) * 72, hy + math.sin(ang) * 72
        arm(hx, hy, ex, ey)
        flag_atian(ctx, ex, ey, t, ang=-1.45, L=150, d=-1)
    else:
        ex, ey = -84, 172
        arm(hx, hy, ex, ey)
        flag_atian(ctx, ex, ey, t, ang=-1.8, L=160, d=-1)

    # 右手指物或垂放
    if point:
        ex, ey = 130, 40 + math.sin(t * 3) * 6
        arm(64, 108, ex, ey)
        star(ctx, ex + 28, ey - 26, 14, C['yellow'], 1.0, rot=t * 2, outline=True)
    else:
        arm(64, 108, 86, 172)

    # 6. 頭部輪廓與短髮
    for sd in (-1, 1):
        ctx.arc(sd * 84, 0, 16, 0, 2 * math.pi)
        fillstroke(ctx, SKIN_DEFAULT, stroke=C['navy'], lw=4)
    ctx.arc(0, -8, 84, 0, 2 * math.pi)
    fillstroke(ctx, SKIN_DEFAULT, stroke=C['navy'], lw=5)

    # 7. 眼睛眨眼與視線
    blink = (t % 3.4) < 0.13
    for ex_ in (-30, 30):
        ctx.save()
        ctx.translate(ex_ + look * 6, 8)
        ctx.scale(1.0, 0.12 if blink else 1.0)
        ctx.arc(0, 0, 12, 0, 2 * math.pi)
        ctx.set_source_rgb(*C['navy'])
        ctx.fill()
        if not blink:
            ctx.arc(4, -4, 4.5, 0, 2 * math.pi)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()
            ctx.arc(-3, 4, 2.0, 0, 2 * math.pi)
            ctx.fill()
        ctx.restore()

    # 8. 腮紅
    for ex_ in (-48, 48):
        ctx.arc(ex_, 36, 10, 0, 2 * math.pi)
        ctx.set_source_rgba(*C['pink'], 0.75)
        ctx.fill()

    # 9. 嘴型
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
            ctx.arc(0, 36, 15, 0.15 * math.pi, 0.85 * math.pi)
        else:
            ctx.arc(0, 56, 12, 1.2 * math.pi, 1.8 * math.pi)
        ctx.set_source_rgb(*C['navy'])
        ctx.set_line_width(5)
        ctx.stroke()

    # 10. 卡其戶外遮陽帽 (Bucket Hat)
    ctx.save()
    ctx.translate(0, -68)
    # 帽簷下緣 (圓弧邊緣)
    ctx.move_to(-105, 10)
    ctx.curve_to(-50, 28, 50, 28, 105, 10)
    ctx.curve_to(95, -12, -95, -12, -105, 10)
    ctx.close_path()
    fillstroke(ctx, HAT_COLOR, stroke=C['navy'], lw=4.5)

    # 帽身主體
    ctx.move_to(-72, 6)
    ctx.line_to(-58, -50)
    ctx.curve_to(-25, -60, 25, -60, 58, -50)
    ctx.line_to(72, 6)
    ctx.close_path()
    fillstroke(ctx, HAT_COLOR, stroke=C['navy'], lw=4.5)

    # 墨綠帽帶
    ctx.move_to(-68, 6)
    ctx.line_to(-64, -8)
    ctx.curve_to(-25, -16, 25, -16, 64, -8)
    ctx.line_to(68, 6)
    ctx.close_path()
    fillstroke(ctx, HAT_BAND, stroke=C['navy'], lw=3.5)

    # 竹葉徽章
    bamboo_leaf_badge(ctx, 36, -2, s=0.95)
    ctx.restore()

    # 11. 汗滴
    if sweat:
        dy = (t * 40) % 30
        ctx.move_to(90, -20 + dy)
        ctx.curve_to(76, 8 + dy, 80, 20 + dy, 90, 20 + dy)
        ctx.curve_to(102, 20 + dy, 106, 8 + dy, 90, -20 + dy)
        fillstroke(ctx, (0.55, 0.80, 1.0), stroke=C['navy'], lw=3)

    ctx.restore()
