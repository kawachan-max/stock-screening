"""
PWA用アイコン（オレンジ背景＋「株」）を public/ に生成する。
依存: pip install pillow

使い方（screening-ui ディレクトリで）:
  python scripts/generate_pwa_icons.py

日本語フォントが見つからない環境では環境変数 PWA_ICON_FONT に .ttf/.ttc のパスを指定してください。
"""
from __future__ import annotations

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow が必要です: pip install pillow", file=sys.stderr)
    sys.exit(1)

ORANGE = "#d97706"
TEXT = "\u682a"  # 株
SIZES = (192, 512)


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        os.environ.get("PWA_ICON_FONT"),
        r"C:\Windows\Fonts\meiryo.ttc",
        r"C:\Windows\Fonts\YuGothM.ttc",
        r"C:\Windows\Fonts\msgothic.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for path in candidates:
        if not path or not os.path.isfile(path):
            continue
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_icon(size: int, out_path: str) -> None:
    img = Image.new("RGB", (size, size), ORANGE)
    draw = ImageDraw.Draw(img)
    font_size = max(24, int(size * 0.45))
    font = load_font(font_size)
    bbox = draw.textbbox((0, 0), TEXT, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    draw.text((x, y), TEXT, fill="white", font=font)
    img.save(out_path, format="PNG")
    print(f"Wrote {out_path}")


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public = os.path.join(root, "public")
    os.makedirs(public, exist_ok=True)
    for s in SIZES:
        make_icon(s, os.path.join(public, f"icon-{s}.png"))


if __name__ == "__main__":
    main()
