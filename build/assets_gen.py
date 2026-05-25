# -*- coding: utf-8 -*-
"""파비콘 5종 세트 + OG 이미지 생성. `python build/assets_gen.py` → dist/ 에 출력."""

import os
from PIL import Image, ImageDraw, ImageFont
import pages  # for OUT path

OUT = pages.OUT
GOLD = (244, 210, 156)
COPPER = (201, 138, 107)
BG = (11, 11, 14)


def radial_icon(size):
    """브랜드 라디얼 그라데이션 + specular 하이라이트 + 다크 림 아이콘."""
    s = size * 4  # supersample
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    px = img.load()
    cx, cy, r = s / 2, s / 2, s / 2
    for y in range(s):
        for x in range(s):
            dx, dy = x - cx, y - cy
            d = (dx * dx + dy * dy) ** 0.5
            if d > r:
                continue
            t = d / r
            # specular: 상단-좌측 밝게
            hl = max(0, 1 - (((x - s * 0.36) ** 2 + (y - s * 0.34) ** 2) ** 0.5) / (r * 1.15))
            cr = int(GOLD[0] * (1 - t) + COPPER[0] * t + hl * 40)
            cg = int(GOLD[1] * (1 - t) + COPPER[1] * t + hl * 30)
            cb = int(GOLD[2] * (1 - t) + COPPER[2] * t + hl * 20)
            # dark rim
            if t > 0.92:
                k = (t - 0.92) / 0.08
                cr = int(cr * (1 - k) + 30 * k)
                cg = int(cg * (1 - k) + 22 * k)
                cb = int(cb * (1 - k) + 16 * k)
            px[x, y] = (min(cr, 255), min(cg, 255), min(cb, 255), 255)
    img = img.resize((size, size), Image.LANCZOS)
    return img


def add_monogram(img, text="M"):
    s = img.size[0]
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", int(s * 0.5))
    except Exception:
        font = ImageFont.load_default()
    bb = d.textbbox((0, 0), text, font=font)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((s - w) / 2 - bb[0], (s - h) / 2 - bb[1]), text, font=font, fill=(26, 18, 6, 230))
    return img


def main():
    os.makedirs(OUT, exist_ok=True)

    # favicon.svg (vector, 의존성 0)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs><radialGradient id="g" cx="36%" cy="34%" r="70%">
<stop offset="0%" stop-color="#f8e0b4"/><stop offset="55%" stop-color="#f4d29c"/>
<stop offset="100%" stop-color="#c98a6b"/></radialGradient></defs>
<circle cx="32" cy="32" r="31" fill="url(#g)" stroke="#1a1206" stroke-width="2"/>
<text x="32" y="44" font-family="Georgia,serif" font-size="34" font-weight="bold" fill="#1a1206" text-anchor="middle">M</text>
</svg>"""
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(svg)

    base = add_monogram(radial_icon(512), "M")
    base.save(os.path.join(OUT, "icon-512.png"))
    base.resize((192, 192), Image.LANCZOS).save(os.path.join(OUT, "icon-192.png"))
    base.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"))

    # maskable: 80% safe zone (패딩)
    mask = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    inner = base.resize((410, 410), Image.LANCZOS)
    mask.paste(inner, (51, 51), inner)
    mask.save(os.path.join(OUT, "icon-maskable-512.png"))

    # favicon.ico (멀티사이즈)
    ico = radial_icon(64)
    ico.save(os.path.join(OUT, "favicon.ico"),
             sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    # OG 이미지 1200x630
    og = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(og)
    # 우상단 글로우
    glow = Image.new("RGBA", (1200, 630), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([700, -200, 1400, 400], fill=(244, 210, 156, 38))
    og.paste(Image.alpha_composite(og.convert("RGBA"), glow).convert("RGB"), (0, 0))
    try:
        f_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 84)
        f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
    except Exception:
        f_big = f_sub = ImageFont.load_default()
    d.text((80, 220), "Massage KOREA", font=f_big, fill=GOLD)
    d.text((84, 340), "Seoul · Gyeonggi · Incheon · Busan", font=f_sub, fill=(243, 243, 245))
    d.text((84, 392), "24h Visiting Massage  ·  0508-202-4743", font=f_sub, fill=(154, 154, 163))
    icon = base.resize((150, 150), Image.LANCZOS)
    og.paste(icon, (990, 80), icon)
    og.save(os.path.join(OUT, "assets", "og-cover.jpg") if os.path.isdir(os.path.join(OUT, "assets"))
            else os.path.join(OUT, "og-cover.jpg"), quality=86)
    # ensure /assets/og-cover.jpg path (head references /assets/og-cover.jpg)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    og.save(os.path.join(OUT, "assets", "og-cover.jpg"), quality=86)

    print("자산 생성 완료: favicon.svg/.ico, icon-192/512, maskable, apple-touch, assets/og-cover.jpg")


if __name__ == "__main__":
    main()
