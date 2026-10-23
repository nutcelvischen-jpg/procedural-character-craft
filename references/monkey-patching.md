# 全域角色無縫熱插拔與猴子補丁指南 (Monkey-Patching Guide)

在完整的教學/科普卡通影片生成管線中，場景模板庫（如 `intro_scene`, `roadmap_scene`, `quiz_q`, `corner` 右下角解說窗等）通常預設綁定某一通用角色（如 `dc.doctor`）。

為了讓使用者能在不改動數十個場景代碼的情況下，一秒切換整部影片的主角，必須遵循本規範。

---

## 1. 規範化的函式介面 (The Contract)

任何自訂新角色函式，必須相容以下介面簽名：

```python
def my_custom_character(ctx, x, y, s, t, mouth=0.0, wave=False, point=False, sweat=False, happy=True, look=0.0):
    ...
```

只要參數名與預設值一致，外部模板即可完全透明地傳遞時間戳與動態旗標。

---

## 2. 模組底部自動覆寫 (Module-level Monkey Patching)

以自訂角色「阿天 (`atian.py`)」為例：

```python
# atian.py 檔案結尾
import dc

# 將模板庫中的 doctor 覆寫為 atian
dc.doctor = atian
```

在專案主腳本 `ep1.py` 或 `render_video.py` 中，只需：

```python
# main.py
import dc
from characters.atian import *  # 自動將所有模板預設主持人置換為阿天！

# 後續所有調用 dc.intro_scene(), dc.corner() 等場景將自動渲染出阿天
```

---

## 3. 右下角常駐解說小窗 (Corner Presenter)

影片常駐解說員只需使用簡單的 Wrapper 函式：

```python
def corner(ctx, t, mouth, **kw):
    """將角色縮放為 0.42 放置於 1280x720 畫面右下角"""
    current_presenter = getattr(dc, 'doctor', doctor)
    current_presenter(ctx, 1150, 545, 0.42, t, mouth=mouth, **kw)
```

如此無論當前角色換成小博士、阿天還是小綠，右下角解說小窗都能維持統一的錨點與縮放標準。
