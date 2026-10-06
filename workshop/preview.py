"""Draws workshop/preview.png (256x256, required by the PZ Workshop uploader).

Drawn at 4x and scaled down for smooth edges. Run: python workshop/preview.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 1024
OUT = pathlib.Path(__file__).with_name("preview.png")
FONT = "C:/Windows/Fonts/seguibl.ttf"


def vertical_gradient(size, top, bottom):
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / (size[1] - 1)
        d.line([(0, y), (size[0], y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    return img


def blurred(img, draw_fn, radius):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(radius)))


def soap_bar(d, x, y, w, h, depth, top, side, front):
    """A bar seen slightly from above: top face, front face, right side."""
    d.polygon([(x, y), (x + w, y), (x + w + depth, y - depth * 0.6), (x + depth, y - depth * 0.6)], fill=top)
    d.polygon([(x + w, y), (x + w + depth, y - depth * 0.6), (x + w + depth, y + h - depth * 0.6), (x + w, y + h)], fill=side)
    d.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=front)
    # Engraved oval on the front.
    d.rounded_rectangle([x + w * 0.2, y + h * 0.28, x + w * 0.8, y + h * 0.72], radius=int(h * 0.22), outline=side, width=8)


def main():
    img = vertical_gradient((S, S), (92, 52, 28), (34, 18, 12)).convert("RGBA")
    blurred(img, lambda d: d.ellipse([140, 120, 700, 700], fill=(255, 170, 80, 110)), 110)

    # Steam above the pot.
    def steam(d):
        for cx, cy, r in [(330, 250, 70), (400, 190, 60), (360, 120, 50), (470, 240, 55), (450, 150, 42)]:
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 245, 230, 120))
    blurred(img, steam, 22)

    # Fire under the pot.
    def fire(d):
        d.polygon([(250, 640), (300, 520), (330, 590), (380, 470), (420, 580), (460, 500), (500, 640)], fill=(255, 140, 40, 255))
        d.polygon([(300, 640), (340, 560), (380, 600), (420, 540), (450, 640)], fill=(255, 215, 90, 255))
    blurred(img, fire, 6)
    d = ImageDraw.Draw(img)
    for x1, x2 in ((210, 520), (240, 500)):
        d.line([(x1, 655), (x2, 625)], fill=(90, 56, 36), width=34)
        d.line([(x2, 655), (x1, 625)], fill=(110, 70, 44), width=34)

    # Iron pot: body, rim, handles, the soap mix inside.
    d.ellipse([180, 330, 560, 600], fill=(52, 52, 58))
    d.rectangle([180, 330, 560, 470], fill=(52, 52, 58))
    d.ellipse([200, 360, 300, 560], fill=(72, 72, 80))
    d.ellipse([170, 290, 570, 380], fill=(80, 80, 88))
    d.ellipse([196, 304, 544, 366], fill=(236, 214, 170))
    d.ellipse([240, 314, 340, 344], fill=(250, 236, 204))
    for hx in (150, 562):
        d.rounded_rectangle([hx, 352, hx + 28, 420], radius=12, fill=(40, 40, 46))

    # Shadow, then a stack of three soap bars in front.
    blurred(img, lambda d2: d2.ellipse([470, 780, 900, 840], fill=(0, 0, 0, 150)), 16)
    d = ImageDraw.Draw(img)
    soap_bar(d, 500, 700, 330, 110, 70, (255, 226, 200), (214, 160, 128), (244, 196, 160))
    soap_bar(d, 540, 590, 310, 104, 64, (232, 244, 220), (160, 190, 140), (206, 226, 186))
    soap_bar(d, 520, 484, 300, 100, 60, (250, 238, 214), (204, 178, 130), (238, 220, 180))

    # A few bubbles.
    for cx, cy, r in [(870, 380, 34), (800, 300, 22), (920, 270, 18), (640, 400, 16)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 245, 230), width=6)
        d.ellipse([cx - r * 0.6, cy - r * 0.6, cx - r * 0.1, cy - r * 0.25], fill=(255, 250, 240))

    # Title with a soft shadow.
    font = ImageFont.truetype(FONT, 136)
    text = "SOAPMAKER"
    w = d.textlength(text, font=font)
    x, y = (S - w) / 2, 852
    blurred(img, lambda d2: d2.text((x + 6, y + 10), text, font=font, fill=(0, 0, 0, 180)), 8)
    ImageDraw.Draw(img).text((x, y), text, font=font, fill=(255, 238, 205), stroke_width=4, stroke_fill=(70, 36, 18))

    img.convert("RGB").resize((256, 256), Image.Resampling.LANCZOS).save(OUT, optimize=True)
    print(OUT, OUT.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
