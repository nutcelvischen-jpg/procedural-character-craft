---
name: procedural-character-craft
description: 純程式碼向量卡通角色設計與動畫製作套件。教授並自動化打造如「AI 小博士 (Doctor)」、「阿天 (Atian)」、「小綠 (Xiaolu)」等零素材依賴、100% 純程式碼、可語音對嘴與手勢互動的 2D 向量動畫角色。當使用者需要設計向量吉祥物、卡通主持人、解說員角色、動態對嘴表情、或整合至科普/教學影片時使用。
---

# 純程式化向量卡通角色設計與動畫製作 (Procedural Vector Character Craft)

本技能提供一套 **100% 純程式碼驅動、零外部圖檔素材依賴（零失真純向量）** 的 2D 卡通角色設計與動態生成管線。角色可直接在 **Python Pycairo**（影片渲染引擎）與 **HTML5 Canvas / Web**（即時互動網頁）雙端通用。

---

## 核心能力矩陣
* **標準角色簽名介面**：相容語音振幅音量口型連動（Mouth Sync）、呼吸點頭律動（Bobbing）、自然週期眨眼（Blink）、視線偏移（Look）、揮手（Wave）、手持教鞭/旗幟（Point）、緊張冒汗（Sweat）、喜怒情緒（Happy）。
* **12 層骨架圖層架構**：從腳底投影、雙腿、軀幹服飾、橡皮管手臂、頭耳基底、髮型、眼鏡五官、嘴型到配件特效，杜絕動畫位移穿幫。
* **內建經典角色庫**：
  * **AI 小博士 (`doctor.py`)**：白色實驗袍、圓框眼鏡、橘領帶、口袋紅藍筆、星光木質教鞭、天線呆毛。
  * **在地導遊・阿天 (`atian.py`)**：卡其戶外遮陽帽、竹葉徽章、山林綠背心、飄揚導遊旗、短靴。
  * **智慧大使・小綠 (`xiaolu.py`)**：湖水綠貝雷帽、制服夾克、橘色證件掛牌、雷射簡報筆。
* **一鍵驗證工具鏈**：
  * **9 格狀態矩陣圖**：一秒輸出 Idle、Talking、Wave、Point、Happy、Serious、Sweat、Look Left、Look Right 完整驗證圖。
  * **動態 GIF 生成器**：生成語音連動、呼吸與手勢兼具的平滑動畫展示。
  * **Web 即時互動測試器**：瀏覽器即時拉桿調控參數與即時預覽。

---

## 1. 角色函式標準介面 (API Contract)

所有自訂角色必須符合以下標準簽名：

```python
def my_character(ctx, x, y, s, t, mouth=0.0, wave=False, point=False, sweat=False, happy=True, look=0.0):
    """
    ctx   : Cairo Context 或 Canvas 2D Context
    x, y  : 角色錨點座標（通常為角色中心腳底地面基準點）
    s     : 縮放比例 (scale，例：1.0 全景，0.42 右下角小窗)
    t     : 動畫全片時間 (秒)，用於驅動正弦波呼吸、眨眼、擺動
    mouth : 語音音量振幅 (0.0 ~ 1.0)，連動開嘴口型大小
    wave  : 是否做出揮手或搖旗動作 (布林值)
    point : 是否做出持教鞭或手指導引動作 (布林值)
    sweat : 是否流汗滴 (布林值)
    happy : 是否微笑/開心 (True) 或是嚴肅/驚訝 (False)
    look  : 視線偏移量 (-1.0 向左看 ~ 1.0 向右看)
    """
```

---

## 2. 打造全新角色的五步驟工作流程

1. **定義角色特徵與配色表**：
   - 設定專屬顏色常數（衣服色、配件色、髮色、膚色）。
   - 決定標誌性配件（例如小博士的白袍眼鏡、阿天的遮陽帽、小綠的貝雷帽）。
2. **按照 12 層標準順序實作繪圖邏輯**（詳見 `references/anatomy-and-layers.md`）：
   - 陰影 → 雙腿鞋子 → 軀幹衣物 → 手臂動作分支 → 頭部輪廓 → 髮型呆毛 → 眼睛眼鏡 → 嘴型 → 帽子配飾 → 特效。
3. **套入動畫數學公式**（詳見 `references/animation-math.md`）：
   - 呼吸起伏：`bob = -abs(math.sin(t * 4.2)) * 12`
   - 自然眨眼：`blink = (t % 3.1) < 0.13`
   - 說話張嘴：`scale(1.0, (4 + 18 * mouth) / 13)`
4. **輸出 9 格矩陣圖驗證**：
   ```bash
   python3 tools/preview_grid.py <角色名稱> assets/matrix_<角色名稱>.png
   ```
5. **輸出動態 GIF 或於 Web 即時預覽**：
   ```bash
   python3 tools/render_demo_gif.py <角色名稱> assets/demo_<角色名稱>.gif
   ```

---

## 3. 快速常用指令

```bash
# 1. 產生 AI 小博士 9 格狀態檢驗圖
python3 tools/preview_grid.py doctor assets/matrix_doctor.png

# 2. 算繪 AI 小博士動態說話手勢 GIF (3 秒 24 FPS)
python3 tools/render_demo_gif.py doctor assets/demo_doctor.gif

# 3. 啟動 Web 互動調整器
open web/index.html
```

---

## 4. 全域角色置換 (Monkey-Patching)

當需要將影片模板預設主角全面切換為新角色時，只需在角色模組或腳本入口覆寫：

```python
import dc
import characters.doctor as doctor_mod
dc.doctor = my_new_character  # 全局場景一秒切換
```
詳細說明見 `references/monkey-patching.md`。
