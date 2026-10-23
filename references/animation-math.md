# 程式化動畫數學與週期函數公式 (Procedural Animation Math)

純向量角色不需要逐格關鍵影格檔案，所有動態完全由**時間參數 `t`（秒）**與**語音 RMS 音量 `mouth`** 經由三角函數、模運算與彈性緩動即時算繪。

---

## 1. 週期性呼吸起伏與點頭律動 (Breathing & Head Bobbing)

```python
# 垂直起伏 (向下蹲踏感，採用絕對值正弦波)
bob = -abs(math.sin(t * 4.2)) * 12

# 以腰部 (0, 200) 為中心旋轉微晃
ctx.translate(0, bob + 200)
ctx.rotate(math.sin(t * 2.1) * 0.05)
ctx.translate(0, -200)
```
* **頻率設計**：`4.2 rad/s` 對應每秒約 0.67 次呼吸/微彈跳週期，節奏自然親切。
* **微傾斜 (Tilt)**：使用頻率減半的 `sin(t * 2.1)`，讓角色呼吸時身體會隨之微微左右晃動，消除生硬的機器人感。

---

## 2. 自然眨眼週期 (Blinking Modulo)

```python
# 每 3.1 秒眨眼一次，閉眼持續 0.13 秒
blink = (t % 3.1) < 0.13

for ex_ in (-34, 34):
    ctx.save()
    ctx.translate(ex_ + look * 6, -2)
    # 眨眼時將 Y 軸壓扁為 0.12，形成細長閉眼縫隙
    ctx.scale(1.0, 0.12 if blink else 1.0)
    ctx.arc(0, 0, 12, 0, 2 * math.pi)
    ctx.set_source_rgb(*C['navy'])
    ctx.fill()
    if not blink:
        # 睜眼時才繪製白色高光反射
        ctx.arc(4, -5, 4.5, 0, 2 * math.pi)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
    ctx.restore()
```

---

## 3. 語音音量即時對嘴 (RMS Volume to Phoneme Lip-Sync)

```python
if mouth > 0.08:
    # 說話中：張嘴橢圓，高度隨音量連續擴大
    ctx.save()
    ctx.translate(0, 44)
    ctx.scale(1.0, (4 + 18 * mouth) / 13)
    ctx.arc(0, 0, 13, 0, 2 * math.pi)
    ctx.restore()
    ctx.set_source_rgb(*C['navy'])
    ctx.fill()
else:
    # 靜音中：根據表情繪製弧線
    if happy:
        # 微笑彎唇 (下半圓弧)
        ctx.arc(0, 34, 15, 0.15 * math.pi, 0.85 * math.pi)
    else:
        # 沮喪/嚴肅 (上半圓弧)
        ctx.arc(0, 56, 12, 1.2 * math.pi, 1.8 * math.pi)
    ctx.set_source_rgb(*C['navy'])
    ctx.set_line_width(5)
    ctx.stroke()
```

---

## 4. 揮手擺盪與星光自旋 (Wave Gesture & Star Rotation)

```python
# 快速有精神的揮手擺盪 (9 rad/s)
ang = -2.3 + 0.4 * math.sin(t * 9)
hand_x = shoulder_x + math.cos(ang) * 72
hand_y = shoulder_y + math.sin(ang) * 72

# 教鞭尖端星光慢速自旋 (2 rad/s)
star(ctx, hand_x + 76, hand_y - 66, r=16, col=C['yellow'], rot=t * 2.0, outline=True)
```

---

## 5. 冒汗與滑落粒子 (Sweat Drop Animation)

```python
if sweat:
    # 汗滴沿臉頰向下滑落並循環 (Modulo)
    dy = (t * 40) % 30
    ctx.move_to(92, -40 + dy)
    ctx.curve_to(76, -12 + dy, 80, 0 + dy, 92, 0 + dy)
    ctx.curve_to(104, 0 + dy, 108, -12 + dy, 92, -40 + dy)
    fillstroke(ctx, (0.55, 0.80, 1.0), stroke=C['navy'], lw=3)
```
