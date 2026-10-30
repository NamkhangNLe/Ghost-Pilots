import math, random, sys
from PIL import Image, ImageDraw, ImageFilter

A = "/Users/dhruvchowdhary/Ghost-Pilots2/APBOv2/Assets.xcassets/"
OUT = sys.argv[1]
BG = (21, 32, 68)
SHIP = {c: A + f"Ships/apbo{c}.imageset/apbo{c}.png" for c in
        ["Black", "Blue", "Green", "Orange", "Purple", "White", "Yellow"]}
SHIP["Red"] = A + "Ships/player.imageset/apboRed.png"


def starfield(W, H, n, seed):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (W, H), BG + (255,))
    # soft center glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    r = int(min(W, H) * 0.55)
    gd.ellipse((W // 2 - r * 1.4, H // 2 - r, W // 2 + r * 1.4, H // 2 + r), fill=(60, 80, 160, 70))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(r * 0.45)))
    d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        s = rnd.choice([5, 7, 9, 11, 14, 18])
        a = rnd.randint(150, 255)
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 255, 255, a))
    return im


def ship(color, scale, angle):
    s = Image.open(SHIP[color]).convert("RGBA")
    s = s.resize((int(s.width * scale), int(s.height * scale)), Image.LANCZOS)
    return s.rotate(angle, resample=Image.BICUBIC, expand=True)


def place(canvas, color, cx, cy, scale, angle, trail=True, shots=0):
    rad = math.radians(angle)
    fx, fy = math.cos(rad), -math.sin(rad)  # facing direction (screen coords)
    over = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    if trail:
        for i in range(1, 9):
            dist = 95 * scale + i * 34 * scale
            r = (26 - i * 2.2) * scale
            a = int(170 - i * 18)
            x, y = cx - fx * dist, cy - fy * dist
            d.ellipse((x - r, y - r, x + r, y + r), fill=(230, 220, 225, a))
    for k in range(shots):
        dist = 190 * scale + k * 120 * scale
        x, y = cx + fx * dist, cy + fy * dist
        L, w = 34 * scale, 9 * scale
        d.line((x - fx * L, y - fy * L, x + fx * L, y + fy * L), fill=(255, 255, 255, 255), width=int(w * 2))
        d.ellipse((x + fx * L - w, y + fy * L - w, x + fx * L + w, y + fy * L + w), fill=(255, 255, 255, 255))
        d.ellipse((x - fx * L - w, y - fy * L - w, x - fx * L + w, y - fy * L + w), fill=(255, 255, 255, 255))
    canvas.alpha_composite(over)
    s = ship(color, scale, angle)
    canvas.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))


def ghost(canvas, cx, cy, size):
    src = Image.open(A + "AppIcon.appiconset/1024.png").convert("RGB")
    # cut the ghost out: everything not near the bg color, then keep only the
    # component connected to the ghost's body (drops the icon's own stars)
    binm = Image.new("L", src.size, 0)
    px, bp = src.load(), binm.load()
    for y in range(src.height):
        for x in range(src.width):
            r, g_, b = px[x, y]
            if abs(r - BG[0]) + abs(g_ - BG[1]) + abs(b - BG[2]) > 30:
                bp[x, y] = 255
    ImageDraw.floodfill(binm, (512, 640), 128)
    mask = binm.point(lambda v: 255 if v == 128 else 0).filter(ImageFilter.MaxFilter(3))
    g = src.convert("RGBA")
    g.putalpha(mask)
    g = g.resize((size, size), Image.LANCZOS)
    # soft shadow/glow behind the ghost
    sh = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sh.putalpha(g.getchannel("A").point(lambda v: int(v * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(size * 0.03))
    canvas.alpha_composite(sh, (cx - size // 2, cy - size // 2 + int(size * 0.02)))
    canvas.alpha_composite(g, (cx - size // 2, cy - size // 2))


def header():
    W, H = 3840, 1646
    c = starfield(W, H, 170, 7)
    ghost(c, W // 2, int(H * 0.47), 1250)
    # dogfight: left squad heads right/up, right squad heads left
    place(c, "Red",    560,  430, 2.3, -12, shots=2)
    place(c, "Blue",   300, 1120, 2.0, 18, shots=1)
    place(c, "Yellow", 1060, 1330, 1.7, 35)
    place(c, "Green",  1100, 250, 1.6, -25)
    place(c, "Orange", 3280, 470, 2.3, 192, shots=2)
    place(c, "Purple", 3560, 1140, 2.0, 160, shots=1)
    place(c, "White",  2780, 1340, 1.7, 145)
    place(c, "Black",  2760, 240, 1.6, 205)
    return c


def search():
    W, H = 3840, 2560
    c = starfield(W, H, 240, 11)
    ghost(c, W // 2, int(H * 0.48), 1700)
    place(c, "Red",    620,  560, 2.6, -15, shots=2)
    place(c, "Blue",   420, 1500, 2.3, 15, shots=1)
    place(c, "Yellow", 1040, 2170, 2.0, 40)
    place(c, "Green",  1150, 260, 1.8, -30)
    place(c, "Orange", 3220, 600, 2.6, 195, shots=2)
    place(c, "Purple", 3440, 1560, 2.3, 165, shots=1)
    place(c, "White",  2800, 2200, 2.0, 140)
    place(c, "Black",  2700, 250, 1.8, 210)
    return c


for name, fn in [("header_3840x1646.png", header), ("search_3840x2560.png", search)]:
    fn().convert("RGB").save(f"{OUT}/{name}", optimize=True)
    print(name)
