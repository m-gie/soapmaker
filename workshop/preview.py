"""Draws workshop/preview.png (256x256, required by the PZ Workshop uploader).

Uses the game's own item icons, read from your Project Zomboid install and scaled
by whole numbers so the pixel art stays crisp. Run: python workshop/preview.py [game dir]
"""
import pathlib
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pzpack import read_pack  # noqa: E402

GAME = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "E:/SteamLibrary/steamapps/common/ProjectZomboid")
OUT = pathlib.Path(__file__).with_name("preview.png")
FONT = "C:/Windows/Fonts/seguibl.ttf"
S = 256


def icons(*names):
    wanted, found = set(names), {}
    for pack in ("UI2.pack", "UI.pack"):
        for _, page, entries in read_pack(GAME / "media/texturepacks" / pack):
            for name, x, y, w, h, ox, oy, fw, fh in entries:
                if name in wanted and name not in found:
                    full = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
                    full.paste(page.crop((x, y, x + w, y + h)), (ox, oy))
                    found[name] = full
    missing = wanted - found.keys()
    assert not missing, f"icons not found: {missing}"
    return found


def scaled(img, k):
    return img.resize((img.width * k, img.height * k), Image.Resampling.NEAREST)


def place(canvas, img, x, y, shadow=True):
    """Pastes img with its bottom-centre at (x, y), with a soft ground shadow."""
    left, top = x - img.width // 2, y - img.height
    if shadow:
        sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([x - img.width * 0.42, y - 7, x + img.width * 0.42, y + 5], fill=(0, 0, 0, 120))
        canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    canvas.alpha_composite(img, (left, top))


def creamy(img):
    """Turns the stew in vanilla's pot icon into a creamy soap mix: every coloured
    (saturated) pixel becomes cream of the same brightness; the grey metal stays."""
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a and max(r, g, b) - min(r, g, b) > 30:
                lum = (r * 299 + g * 587 + b * 114) / 1000 / 255
                t = min(1.0, 0.35 + lum * 1.1)
                px[x, y] = (int(150 + 105 * t), int(130 + 110 * t), int(95 + 115 * t), a)
    return out


def main():
    ic = icons("Item_Pot_Forged_Soup", "Item_Soap", "Item_Lard", "Item_Charcoal", "Item_Book", "Item_MagazineFood")
    random.seed(5)
    img = Image.new("RGBA", (S, S))
    d = ImageDraw.Draw(img)
    # Warm cabin wall, then wooden floor planks from y=150.
    for y in range(S):
        t = y / S
        d.line([(0, y), (S, y)], fill=(int(70 - 30 * t), int(42 - 18 * t), int(28 - 12 * t), 255))
    for i, ty in enumerate(range(150, S, 12)):
        shade = (112, 76, 48, 255) if i % 2 == 0 else (98, 66, 42, 255)
        d.rectangle([0, ty, S, ty + 11], fill=shade)
        d.line([(0, ty), (S, ty)], fill=(64, 42, 28, 255))
        for x in range((i * 37) % 64, S, 64):
            d.line([(x, ty), (x, ty + 11)], fill=(70, 46, 30, 255))
    d.line([(0, 149), (S, 149)], fill=(40, 26, 18, 255), width=3)

    # Glow of the fire under the pot.
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([60, 150, 196, 240], fill=(255, 150, 50, 110))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))

    # Back row: the book and the magazine that teach the recipe.
    place(img, scaled(ic["Item_Book"], 2), 34, 156)
    place(img, scaled(ic["Item_MagazineFood"], 2), 222, 156)

    # Pixel flames, then the pot of soap mix on them.
    f = ImageDraw.Draw(img)
    for _ in range(140):
        x = int(random.gauss(128, 20))
        y = int(random.gauss(214, 5))
        f.rectangle([x, y, x + 2, y + 2], fill=random.choice([(255, 196, 64, 255), (255, 132, 32, 255), (230, 70, 20, 255)]))
    place(img, scaled(creamy(ic["Item_Pot_Forged_Soup"]), 4), 128, 204, shadow=False)

    # Steam: soft pixel puffs above the pot.
    for cx, cy, r in [(112, 74, 6), (126, 62, 7), (140, 70, 5), (120, 48, 5), (134, 40, 4)]:
        f.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 225, 210, 150))

    # Front row: ingredients on the left, the finished soap on the right.
    place(img, scaled(ic["Item_Lard"], 2), 36, 246)
    place(img, scaled(ic["Item_Charcoal"], 2), 82, 252)
    place(img, scaled(ic["Item_Soap"], 2), 186, 244)
    place(img, scaled(ic["Item_Soap"], 2), 222, 252)

    # Title with a dark outline, like the game's UI text.
    font = ImageFont.truetype(FONT, 32)
    text = "SOAPMAKER"
    w = f.textlength(text, font=font)
    f.text(((S - w) / 2, 6), text, font=font, fill=(255, 238, 205, 255), stroke_width=3, stroke_fill=(40, 22, 12, 255))

    img.convert("RGB").save(OUT, optimize=True)
    print(OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
