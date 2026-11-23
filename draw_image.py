#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page.

One deterministic Pillow picture, 1024x1024: a navy masthead, a gold date
banner, a lead story with a drawn sea scene, four labelled panels with small
drawn scenes, and an "also today" strip. No network, no clock, no randomness:
the same script always writes the same pixels.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

PAPER = (248, 244, 233)
NAVY = (19, 40, 75)
GOLD = (201, 162, 39)
INK = (26, 26, 26)
GREY = (90, 90, 90)
RED = (179, 38, 30)
TEAL = (14, 107, 107)
GREEN = (31, 122, 60)
SEA = (28, 68, 110)
SKY = (214, 228, 238)
PANEL_LINE = (216, 210, 192)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, kicker, kicker_fill, headline, body, scene):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=WHITE, outline=PANEL_LINE, width=2)
    scene(draw, x + 12, y + 12, 132, h - 24)
    tx = x + 156
    tw = x + w - 14 - tx
    draw.text((tx, y + 12), kicker, font=SANS_B(17), fill=kicker_fill)
    head_lines = wrap(draw, headline, SERIF_B(26), tw)
    yy = draw_text_block(draw, tx, y + 36, head_lines, SERIF_B(26), INK, 30)
    body_lines = wrap(draw, body, SANS(18), tw)
    draw_text_block(draw, tx, yy + 4, body_lines[:4], SANS(18), (58, 58, 58), 22)


def scene_globe(draw, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 216, 208),
                 outline=TEAL, width=3)
    for dy in (-r // 2, 0, r // 2):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340,
                 fill=TEAL, width=2)
        draw.line([cx - r + 8, cy + dy, cx + r - 8, cy + dy], fill=TEAL, width=2)
    draw.line([cx - r + 14, cy - r + 10, cx - 6, cy - 2, cx + 4, cy + 12,
               cx - 2, cy + r - 12], fill=RED, width=4)
    draw.line([cx - r + 6, cy + r - 6, cx + r - 6, cy - r + 6],
              fill=RED, width=5)


def scene_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(253, 240, 238))
    draw.line([x + 10, y + h - 12, x + w - 8, y + h - 12], fill=GREY, width=2)
    draw.line([x + 10, y + 8, x + 10, y + h - 12], fill=GREY, width=2)
    pts = [(x + 14, y + 22), (x + 42, y + 34), (x + 66, y + 30),
           (x + 90, y + 66), (x + 112, y + 96), (x + 124, y + h - 26)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=RED)
    draw.text((x + 14, y + h - 34), "-5.1%", font=SANS_B(20), fill=RED)


def scene_flats(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 230))
    draw.rectangle([x + 16, y + 52, x + 56, y + h - 10], fill=(120, 118, 112))
    draw.rectangle([x + 66, y + 78, x + 112, y + h - 10], fill=(90, 88, 84))
    for bx in (16, 66):
        for wy in range(y + 62, y + h - 22, 18):
            draw.rectangle([x + bx + 6, wy, x + bx + 16, wy + 9],
                           fill=(220, 214, 196))
    draw.polygon([(x + 66, y + 78), (x + 80, y + 58), (x + 96, y + 70),
                  (x + 112, y + 78)], fill=(60, 58, 54))
    for cx, cy, r in ((x + 86, y + 34, 14), (x + 102, y + 20, 18),
                      (x + 74, y + 16, 10)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 148, 142))


def scene_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 244, 234))
    cx, cy = x + w // 2 - 6, y + h // 2 + 8
    for i in range(5):
        px = cx - 34 + i * 17
        draw.line([px, cy - 48, px, cy - 34], fill=GREEN, width=3)
        draw.line([px, cy + 34, px, cy + 48], fill=GREEN, width=3)
        py = cy - 34 + i * 17
        draw.line([cx - 48, py, cx - 34, py], fill=GREEN, width=3)
        draw.line([cx + 34, py, cx + 48, py], fill=GREEN, width=3)
    draw.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], fill=GREEN)
    draw.text((cx - 26, cy - 13), "NVDA", font=SANS_B(19), fill=WHITE)
    draw.line([x + w - 34, y + 34, x + w - 34, y + 12, x + w - 14, y + 12],
              fill=GREEN, width=4)
    draw.polygon([(x + w - 14, y + 12), (x + w - 26, y + 4),
                  (x + w - 26, y + 20)], fill=GREEN)


def scene_sea(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + 26], fill=SKY)
    draw.rectangle([x, y + 26, x + w, y + h], fill=SEA)
    for i, wy in enumerate((y + 38, y + 52, y + 66)):
        draw.line([x + 20 + i * 30, wy, x + w - 40 - i * 20, wy],
                  fill=(90, 140, 180), width=2)
    # coastline strip on the right, labelled Benghazi
    draw.rectangle([x + w - 190, y + 26, x + w, y + h], fill=(222, 198, 150))
    draw.text((x + w - 178, y + 30), "BENGHAZI,", font=SANS_B(15), fill=(90, 70, 40))
    draw.text((x + w - 178, y + 48), "LIBYA", font=SANS_B(15), fill=(90, 70, 40))
    # warship silhouette
    sx, sy = x + 120, y + 44
    draw.polygon([(sx, sy), (sx + 210, sy), (sx + 190, sy + 16),
                  (sx + 20, sy + 16)], fill=(30, 32, 38))
    draw.rectangle([sx + 70, sy - 16, sx + 130, sy], fill=(30, 32, 38))
    draw.line([sx + 96, sy - 30, sx + 96, sy - 16], fill=(30, 32, 38), width=4)
    # explosion burst over the ship
    ex, ey = sx + 150, sy - 14
    for ang in range(0, 360, 30):
        import math
        dx = int(26 * math.cos(math.radians(ang)))
        dy = int(26 * math.sin(math.radians(ang)))
        draw.line([ex, ey, ex + dx, ey + dy], fill=(240, 150, 40), width=5)
    draw.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=(250, 200, 60))
    draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 240, 180))
    # small sea drone with a wake, bottom left
    dx, dy = x + 60, y + h - 22
    draw.ellipse([dx - 12, dy - 6, dx + 12, dy + 6], fill=(220, 220, 220))
    draw.line([dx - 34, dy + 2, dx - 14, dy + 2], fill=WHITE, width=3)
    draw.line([dx - 44, dy + 6, dx - 18, dy + 6], fill=WHITE, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.rectangle([0, 0, W, 92], fill=NAVY)
    title = "THE WORLD IN ONE PAGE"
    tw = draw.textlength(title, font=SERIF_B(52))
    draw.text(((W - tw) / 2, 18), title, font=SERIF_B(52), fill=WHITE)
    draw.rectangle([0, 92, W, 98], fill=GOLD)

    # Date banner
    date = "MONDAY  \u2022  23 NOVEMBER 2026"
    tw = draw.textlength(date, font=SANS_B(36))
    draw.text(((W - tw) / 2, 102), date, font=SANS_B(36), fill=NAVY)
    sub = "THE DAY'S WORLD NEWS \u2014 IN ONE IMAGE"
    tw = draw.textlength(sub, font=SANS_B(15))
    draw.text(((W - tw) / 2, 146), sub, font=SANS_B(15), fill=GREY)

    # Lead panel
    lx, ly, lw, lh = 28, 168, 968, 236
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=6,
                           fill=WHITE, outline=NAVY, width=3)
    draw.text((lx + 20, ly + 12), "LEAD  \u2022  UKRAINE  \u2022  LIBYA",
              font=SANS_B(19), fill=RED)
    head = "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA"
    head_lines = wrap(draw, head, SERIF_B(38), lw - 40)
    yy = draw_text_block(draw, lx + 20, ly + 38, head_lines, SERIF_B(38),
                         INK, 44)
    subline = ("Kyiv says its sea drones sank the corvette Merkury at Benghazi, "
               "about 1,500 miles from the front line \u2014 and hit a second "
               "Russian ship.")
    sub_lines = wrap(draw, subline, SANS(21), lw - 40)
    draw_text_block(draw, lx + 20, yy + 2, sub_lines[:2], SANS(21),
                    (58, 58, 58), 26)
    scene_sea(draw, lx + 8, ly + lh - 84, lw - 16, 76)

    # Four panels in two rows
    pw, ph = 474, 188
    panel(draw, 28, 420, pw, ph, "CLIMATE \u2022 ANTALYA", TEAL,
          "CLIMATE TALKS END WITH NO DEAL",
          "COP31 closes without an agreement \u2014 the longest climate "
          "summit ever \u2014 after the EU rejects a draft that leaves out "
          "fossil fuels.",
          scene_globe)
    panel(draw, 522, 420, pw, ph, "MARKETS \u2022 ASIA & WALL ST", RED,
          "TECH ROUT HITS WORLD MARKETS",
          "Kospi falls 3.3%, Nikkei 5.1% and the S&P 500 3.7% as doubts "
          "over AI spending hammer chip stocks.",
          scene_chart)
    panel(draw, 28, 624, pw, ph, "UKRAINE \u2022 KYIV REGION", RED,
          "STRIKE ON FLATS KILLS AT LEAST 11",
          "A Russian strike partly destroys an apartment block in Dymer; "
          "14 people are reported missing under the rubble.",
          scene_flats)
    panel(draw, 522, 624, pw, ph, "TECH \u2022 CHIPS", GREEN,
          "HUANG IS BACK AT NVIDIA",
          "The board reinstates Jensen Huang as chief executive; President "
          "Trump calls the move \u201ccorrect and proper\u201d.",
          scene_chip)

    # Also-today strip
    sx, sy, sw, sh = 28, 828, 968, 140
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=6,
                           fill=(233, 228, 212), outline=PANEL_LINE, width=2)
    draw.text((sx + 18, sy + 10), "ALSO TODAY", font=SANS_B(20), fill=NAVY)
    items = [
        "Indonesia: factory fire kills 24; dozens missing.",
        "Peru: magnitude 6.7 quake shakes the Andes.",
        "Iran strikes a site in Bahrain; Trump warns of fresh strikes.",
        "Mexico: cartel chief \u201cEl Chapo Isidro\u201d captured; 11 die in the firefight.",
        "Manchester: 12,000 evacuated from a concert after a substance is released.",
        "BepiColombo spacecraft enters orbit around Mercury.",
        "US: Democrats win at least 258 House seats, their most since 1992.",
    ]
    joined = "  \u2022  ".join(items)
    lines = wrap(draw, joined, SANS(19), sw - 36)
    draw_text_block(draw, sx + 18, sy + 38, lines[:4], SANS(19), INK, 24)

    # Footer: where the facts come from
    foot = ("As reported on 23 Nov 2026 \u2014 Reuters  \u2022  AP  \u2022  Al Jazeera  "
            "\u2022  Just Security  \u2022  Economic Times  \u2022  Tribune Online")
    tw = draw.textlength(foot, font=SANS(15))
    draw.text(((W - tw) / 2, 984), foot, font=SANS(15), fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
