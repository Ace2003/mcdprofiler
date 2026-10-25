# -*- coding: utf-8 -*-
"""麦门侧写师参赛封面合成：底图 → 4:3 裁切 1600x1200 → 叠加标题文字层"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = r"E:\allthings\mcd\mcd-profiler\cover-src\Dark_hacker_terminal_aesthetic_2026-10-25T04-03-56.png"
OUT = r"E:\allthings\mcd\mcd-profiler\cover\cover-1600x1200.png"
OUT_JPG = r"E:\allthings\mcd\mcd-profiler\cover\cover-1600x1200.jpg"

W, H = 1600, 1200

# ---------- 1. 居中裁切为 4:3 并放大 ----------
img = Image.open(SRC).convert("RGB")
sw, sh = img.size
target_ratio = 4 / 3
crop_w = int(sh * target_ratio)
if crop_w <= sw:
    left = (sw - crop_w) // 2
    img = img.crop((left, 0, left + crop_w, sh))
else:
    crop_h = int(sw / target_ratio)
    top = (sh - crop_h) // 2
    img = img.crop((0, top, sw, top + crop_h))
img = img.resize((W, H), Image.LANCZOS)

# ---------- 2. 可读性渐变遮罩（上/下压暗） ----------
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for y in range(420):
    a = int(160 * (1 - y / 420) ** 1.5)
    od.line([(0, y), (W, y)], fill=(5, 8, 12, a))
for y in range(260):
    a = int(170 * (y / 260) ** 1.5)
    od.line([(0, H - 260 + y), (W, H - 260 + y)], fill=(5, 8, 12, a))
img = Image.alpha_composite(img.convert("RGBA"), overlay)

draw = ImageDraw.Draw(img)

GREEN = (63, 185, 80, 255)
DIM = (139, 148, 158, 255)
WHITE = (235, 240, 245, 255)
ORANGE = (240, 136, 62, 255)

f_big = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 118)
f_en = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 44)
f_term = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 30)
f_small = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 34)
f_tag = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 52)

M = 80  # 安全边距

# ---------- 3. 顶部终端栏 ----------
draw.rectangle([M, M, M + 460, M + 54], outline=(63, 185, 80, 200), width=2)
draw.text((M + 22, M + 8), "MCD-PROFILER v2.0", font=f_term, fill=GREEN)
draw.rectangle([M + 478, M + 16, M + 508, M + 46], fill=GREEN)  # 光标块

# ---------- 4. 主标题 ----------
ty = 170
draw.text((M, ty), "麦门侧写师", font=f_big, fill=WHITE)
# 标题下的绿色高亮条
draw.rectangle([M + 2, ty + 148, M + 560, ty + 158], fill=(63, 185, 80, 220))

# 英文副标题
draw.text((M, ty + 190), "McProfiling", font=f_en, fill=GREEN)
draw.text((M + 330, ty + 190), "·  点单即人格", font=f_en, fill=ORANGE)

# ---------- 5. 底部信息带 ----------
by = H - 190
# 标语
draw.text((M, by), "先读懂你，再喂饱你。", font=f_tag, fill=WHITE)

# 徽章行
def badge(x, text):
    w = draw.textlength(text, font=f_small)
    draw.rounded_rectangle([x, by + 84, x + w + 44, by + 140], radius=10,
                           outline=GREEN, width=2)
    draw.text((x + 22, by + 92), text, font=f_small, fill=GREEN)
    return x + w + 44 + 24

x = badge(M, "麦当劳 MCP 真实下单")
x = badge(x, "行为侧写引擎")
x = badge(x, "1024 用餐赛道参赛作品")

# ---------- 6. 盖掉右下角工具水印残影 ----------
wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
wd = ImageDraw.Draw(wm)
for i in range(220):
    a = int(255 * (1 - i / 220))
    wd.line([(W - i, H), (W - i, H - 90)], fill=(6, 10, 14, a))
wd.rectangle([W - 220, H - 90, W, H], fill=(6, 10, 14, 255))
img = Image.alpha_composite(img, wm)

# ---------- 7. 输出 ----------
img.convert("RGB").save(OUT_JPG, quality=92)
img.convert("RGB").save(OUT.replace(".png", ".png"))
print("done", OUT_JPG)
