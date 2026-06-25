#!/usr/bin/env python3
"""
render_menu.py  —  重新生成开始界面菜单图片

当菜单文字需要修改时，编辑下方 MENU_ITEMS 列表，然后运行本脚本即可。

依赖:  pip install brotli fonttools Pillow
"""

import os, tempfile
from io import BytesIO
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

# ── 配置 ──────────────────────────────────────────────
FONT_WOFF2 = os.path.join(os.path.dirname(__file__),
                          "..", "source", "fonts", "Cubic_11.woff2")
OUT_DIR    = os.path.join(os.path.dirname(__file__),
                          "..", "game", "images")
FONT_SIZE  = 48
TEXT_COLOR = (200, 210, 230)
PAD        = 12

MENU_ITEMS = [
    ("start",    "开始游戏"),
    ("settings", "设置"),
    ("help",     "帮助"),
]


def woff2_to_ttf(woff2_path: str) -> str:
    """用 fonttools 将 WOFF2 解为 TTF，返回临时文件路径。"""
    with open(woff2_path, "rb") as f:
        font = TTFont(BytesIO(f.read()))
    tmp = os.path.join(tempfile.gettempdir(), "Cubic_11.ttf")
    font.save(tmp)
    font.close()
    return tmp


def render_all():
    os.makedirs(OUT_DIR, exist_ok=True)
    ttf = woff2_to_ttf(FONT_WOFF2)
    font = ImageFont.truetype(ttf, FONT_SIZE)

    for key, text in MENU_ITEMS:
        bbox = font.getbbox(text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        w, h = tw + PAD * 2, th + PAD * 2
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((PAD, PAD - bbox[1]), text, fill=TEXT_COLOR, font=font)
        out = os.path.join(OUT_DIR, f"menu_{key}.png")
        img.save(out)
        print(f"  {out}  ({w}x{h})")

    os.remove(ttf)
    print("done")


if __name__ == "__main__":
    render_all()
