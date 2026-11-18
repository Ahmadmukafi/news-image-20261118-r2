#!/usr/bin/env python3
"""Draw a magazine-cover front page summing up world news of 18 Nov 2026.

Concept: magazine cover, not a broadsheet. White masthead, a big
photo-led hero (a drawn map of the Gulf at night: the U.S. strike on
Qeshm Island and Iran's drone attacks on Bahrain and Kuwait), then a
three-column grid of the day's other big stories, and a dark markets
ticker at the foot. All text is drawn with DejaVu fonts; the output is
deterministic (no timestamps, no randomness).
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

NAVY = (10, 26, 44)
NAVY2 = (18, 42, 66)
LAND = (29, 58, 78)
LAND2 = (33, 66, 88)
RED = (200, 16, 46)
RED_L = (255, 90, 78)
AMBER = (242, 165, 65)
WHITE = (255, 255, 255)
INK = (12, 12, 12)
GREY = (90, 96, 104)
BLUE = (31, 95, 168)
TEAL = (14, 124, 107)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def starburst(d, cx, cy, r_out, r_in, n, fill, outline=None):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill, outline=outline)


def dashed_line(d, p0, p1, fill, width=3, dash=10, gap=7):
    x0, y0 = p0
    x1, y1 = p1
    total = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / total, (y1 - y0) / total
    s = 0.0
    while s < total:
        e = min(s + dash, total)
        d.line([(x0 + ux * s, y0 + uy * s), (x0 + ux * e, y0 + uy * e)],
               fill=fill, width=width)
        s = e + gap


def draw(out_path):
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.line([(32, 10), (992, 10)], fill=INK, width=3)
    d.text((W // 2, 52), "THE WORLD", font=SERIF_B(84), fill=INK,
           anchor="mm")
    d.line([(32, 100), (992, 100)], fill=INK, width=2)
    d.text((40, 120), "WEDNESDAY, 18 NOVEMBER 2026",
           font=SANS_B(20), fill=INK, anchor="lm")
    d.text((984, 120), "WORLD IN ONE DAY", font=SANS_B(20), fill=RED,
           anchor="rm")
    d.line([(32, 140), (992, 140)], fill=INK, width=1)

    # ---- Hero: the Gulf at night ---------------------------------------
    hy0, hy1 = 140, 600
    for y in range(hy0, hy1):
        t = (y - hy0) / (hy1 - hy0)
        r = int(NAVY[0] + (NAVY2[0] - NAVY[0]) * t)
        g = int(NAVY[1] + (NAVY2[1] - NAVY[1]) * t)
        b = int(NAVY[2] + (NAVY2[2] - NAVY[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # Landmasses (stylised): Iran top-right, Arabia bottom-left.
    d.polygon([(560, 140), (1024, 140), (1024, 300), (920, 330),
               (780, 300), (660, 262), (560, 222)], fill=LAND)
    d.polygon([(0, 600), (0, 430), (170, 405), (300, 440), (390, 505),
               (430, 600)], fill=LAND)
    # Qeshm Island in the strait.
    d.polygon([(470, 330), (540, 312), (585, 330), (545, 352),
               (490, 352)], fill=LAND2, outline=(120, 160, 190))
    # Strait label.
    d.text((430, 392), "STRAIT OF HORMUZ", font=SANS_B(15),
           fill=(150, 175, 195), anchor="mm")
    d.text((180, 250), "THE GULF", font=SANS_B(30),
           fill=(70, 100, 130), anchor="mm")

    # Explosion bursts: Qeshm (the strike) and a smaller one offshore.
    d.ellipse([505, 285, 575, 355], fill=(242, 120, 40))
    starburst(d, 540, 320, 52, 22, 10, fill=(255, 190, 60))
    starburst(d, 540, 320, 30, 13, 10, fill=(255, 240, 180))
    starburst(d, 700, 415, 24, 10, 8, fill=(255, 150, 50))
    starburst(d, 700, 415, 13, 6, 8, fill=(255, 220, 150))

    # Drone arcs from the Iranian coast toward Bahrain and Kuwait.
    dashed_line(d, (640, 300), (700, 398), AMBER, width=3)
    dashed_line(d, (700, 290), (800, 400), AMBER, width=3)
    d.polygon([(700, 398), (690, 382), (712, 386)], fill=AMBER)
    d.polygon([(800, 400), (786, 394), (800, 416)], fill=AMBER)

    # Place markers and labels.
    d.ellipse([535, 315, 545, 325], fill=WHITE, outline=NAVY)
    d.text((540, 252), "QESHM ISLAND", font=SANS_B(16), fill=WHITE,
           anchor="mm")
    for (x, y, label) in [(800, 400, "KUWAIT")]:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=WHITE,
                  outline=NAVY)
        d.text((x + 12, y - 8), label, font=SANS_B(16), fill=WHITE,
               anchor="lm")
    d.ellipse([695, 410, 705, 420], fill=WHITE, outline=NAVY)
    d.text((984, 168), "IRAN", font=SANS_B(18), fill=(150, 175, 195),
           anchor="rm")

    # Headline block over the hero's foot (solid navy, no scrim needed).
    d.rectangle([0, 440, W, hy1], fill=NAVY)
    d.text((40, 458), "THE GULF IGNITES", font=SANS_B(26), fill=RED_L,
           anchor="lm")
    d.text((40, 492), "U.S. STRIKES IRAN;", font=SERIF_B(42), fill=WHITE,
           anchor="lm")
    d.text((40, 540), "TEHRAN HITS BAHRAIN AND KUWAIT",
           font=SERIF_B(42), fill=WHITE, anchor="lm")
    # Bahrain's label sits below its burst, in the empty navy strip
    # above the kicker, so it never collides with the burst or arcs.
    d.text((700, 452), "BAHRAIN", font=SANS_B(16), fill=WHITE,
           anchor="mm")

    # ---- Deck -----------------------------------------------------------
    d.rectangle([40, 616, 48, 668], fill=RED)
    deck = ("American jets hit a missile site on Qeshm Island; Iran's "
            "drones struck U.S. radar sites in Bahrain and Kuwait \u2014 "
            "the third attack there in a week.")
    dy = 618
    for line in wrap(d, deck, SERIF(21), 900):
        d.text((64, dy), line, font=SERIF(21), fill=INK, anchor="lm")
        dy += 28

    # ---- Three-column grid ----------------------------------------------
    gy = 700
    d.line([(32, gy - 16), (992, gy - 16)], fill=INK, width=2)
    cols = [
        ("UKRAINE", RED, "CRIMEA BRIDGE FALLS",
         "Ukraine hits the Kerch bridge a second day; part of its road "
         "span falls into the strait."),
        ("AMERICA", BLUE, "DEMOCRATS TAKE 56",
         "Peltola wins Alaska's Senate seat, giving Democrats 56 seats "
         "(50.12% in the unofficial tally)."),
        ("HEALTH", TEAL, "EBOLA DOUBLES",
         "The DR Congo outbreak passes 11,000 cases and 5,400 deaths \u2014 "
         "more than double in three months, the UN says."),
    ]
    for i, (chip, colour, head, body) in enumerate(cols):
        x0 = 40 + i * 320
        d.rectangle([x0, gy, x0 + 10, gy + 10], fill=colour)
        d.text((x0 + 18, gy + 5), chip, font=SANS_B(18), fill=colour,
               anchor="lm")
        hy = gy + 34
        for line in wrap(d, head, SERIF_B(29), 304):
            d.text((x0, hy), line, font=SERIF_B(29), fill=INK,
                   anchor="lm")
            hy += 36
        by = hy + 10
        for line in wrap(d, body, SANS(18), 304):
            d.text((x0, by), line, font=SANS(18), fill=(40, 40, 40),
                   anchor="lm")
            by += 25

    # ---- Foot: markets + also -------------------------------------------
    fy0 = 884
    d.rectangle([0, fy0, W, H], fill=NAVY)
    d.text((40, 906), "MARKETS", font=SANS_B(20), fill=RED_L, anchor="lm")
    markets = ("S&P 500  7,340.53  \u22121.03%      Nasdaq  24,328.38  "
               "\u22120.74%      Nikkei  59,024.28  +0.28%")
    d.text((170, 906), markets, font=SANS(17), fill=WHITE, anchor="lm")
    d.text((40, 940), "Brent  $91.55  \u22121.71%      Gold  $3,775  "
           "\u22122.31%      VIX  25.46  +11.13%",
           font=SANS(17), fill=WHITE, anchor="lm")
    d.line([(40, 968), (984, 968)], fill=(70, 100, 130), width=1)
    d.text((40, 990), "ALSO", font=SANS_B(18), fill=RED_L, anchor="lm")
    also = ("Cyclone Xavier hits Cook Islands  \u00b7  Russian plane crash "
            "kills 19  \u00b7  6.0 quake in Papua New Guinea")
    d.text((110, 990), also, font=SANS(16), fill=(200, 210, 220),
           anchor="lm")

    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "/output"
    os.makedirs(out_dir, exist_ok=True)
    draw(os.path.join(out_dir, "entry.png"))
