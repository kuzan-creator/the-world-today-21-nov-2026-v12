#!/usr/bin/env python3
"""The World in One Day — Saturday 21 November 2026, v12.
Poster-style one-page newspaper: cream paper, serif masthead, UTC timeline,
number strip, region bar, 13 illustrated cards, dotted map, DATE CHECK.
43 stories, 7 regions, 15 fields. Rendered 2048 supersample, LANCZOS to 1024.
Deterministic: no random module, sine-hash grain only."""
import math
from PIL import Image, ImageDraw, ImageFont

SS = 2
W = H = 2048
MX = 16
CREAM = (246, 240, 224)
PAPER = (250, 246, 233)
INK = (26, 24, 20)
RED = (178, 34, 34)
NAVY = (16, 24, 52)
GREY = (110, 104, 92)
MUT = (90, 86, 76)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
BB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def SERIF_B(n):
    return ImageFont.truetype(FB, n * SS)


def SERIF(n):
    return ImageFont.truetype(FS, n * SS)


def SANS_B(n):
    return ImageFont.truetype(BB, n * SS)


def SANS(n):
    return ImageFont.truetype(BS, n * SS)


def vgrad(d, box, top, bot):
    x0, y0, x1, y1 = box
    for yy in range(y0, y1, 2 * SS):
        t = (yy - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.rectangle([x0, yy, x1, yy + 2 * SS], fill=c)


def grain(img, amp=4):
    px = img.load()
    w, h = img.size
    for yy in range(0, h, 3):
        for xx in range(0, w, 3):
            n = int(amp * math.sin(xx * 12.9898 + yy * 78.233) * 43758.5453) % (2 * amp + 1) - amp
            r, g, b = px[xx, yy]
            px[xx, yy] = (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, min(255, b + n)))


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def banner(d, x, y, w, text):
    d.rectangle([x, y, x + w, y + 15 * SS], fill=RED)
    d.text((x + 6 * SS, y + 2 * SS), text, font=SANS_B(9), fill=(255, 255, 255))


def srcstrip(d, x, y, w, h, text):
    d.rectangle([x, y + h - 12 * SS, x + w, y + h], fill=(12, 12, 12))
    d.text((x + 6 * SS, y + h - 11 * SS), text, font=SANS(8), fill=(255, 255, 255))


TIMELINE = [
    ("00:09", "Peru quake M6.7"),
    ("05:30", "Riyadh: 3 missiles downed"),
    ("09:00", "COP31 draft due, still not out"),
    ("15:00", "COP31: no deal, no new text"),
]

NUMBERS = [
    ("400+", "drones over Ukraine"),
    ("110", "missiles in one night"),
    ("6.7", "Peru quake magnitude"),
    ("3", "missiles downed over Riyadh"),
    ("146", "walk away after jet fire"),
    ("$58,983", "Bitcoin price"),
]

REGIONS = [
    ("EUROPE", 11, (20, 40, 90)),
    ("ASIA", 10, (178, 34, 34)),
    ("AMERICAS", 8, (20, 110, 60)),
    ("MIDDLE EAST", 5, (120, 70, 20)),
    ("AFRICA", 4, (150, 110, 30)),
    ("OCEANIA", 3, (40, 90, 120)),
    ("WORLD", 2, (90, 90, 90)),
]

CARDS = [
    dict(place="ANTALYA, TURKIYE", tag="CLIMATE", badge="DAY 13 OF 12",
         head="COP31 talks run into overtime with no deal",
         body="Draft text lost its fossil-fuel language as talks ran past deadline. (AP)",
         src="Summit president · Reuters", scene="cop"),
    dict(place="RIYADH", tag="MISSILES", badge="3 INTERCEPTED",
         head="Coalition downs three missiles over Riyadh",
         body="A 1:53 a.m. alert woke Riyadh; defences downed three Houthi missiles. (Reuters)",
         src="Coalition statement · Reuters", scene="riyadh"),
    dict(place="JUNIN, PERU", tag="QUAKE", badge="M6.7",
         head="M6.7 quake shakes central Peru",
         body="Deep quake struck at 00:09 GMT near Junin, felt in Lima. No deaths. (USGS)",
         src="USGS · Local reports", scene="quake"),
    dict(place="KYIV", tag="WAR", badge="42 HURT",
         head="Russia hits Kyiv again, 42 hurt",
         body="Homes ablaze in Kyiv; 42 hurt in Kryvyi Rih. (Kyiv Post)",
         src="Kyiv Post", scene="kyiv"),
    dict(place="DAVAO", tag="AVIATION", badge="146 SAFE",
         head="146 walk away after jet fire",
         body="Jet shut an engine down and landed safely. (Philstar)",
         src="Philstar", scene="jet"),
    dict(place="MERCURY", tag="SPACE", badge="FLYBY 6",
         head="BepiColombo's Mercury flyby",
         body="Final flyby sets up orbit insertion in 2027. (ESA)",
         src="ESA", scene="mercury"),
    dict(place="WARSAW", tag="NATO", badge="NATO ALERT",
         head="Poland calls NATO talks over drone",
         body="NATO calls the debris fall a grave violation. (Reuters)",
         src="Reuters", scene="poland"),
    dict(place="LAS VEGAS", tag="F1", badge="RACE NIGHT",
         head="Vegas: Verstappen fastest",
         body="Norris on pole as title rivals split practice. (F1)",
         src="F1", scene="vegas"),
    dict(place="WELLINGTON", tag="CRICKET", badge="136 RUNS",
         head="Rahul's 136 puts India in charge",
         body="Rahul's century gave India the lead. (ESPNcricinfo)",
         src="ESPNcricinfo", scene="cricket"),
    dict(place="BAYELSA", tag="NIGERIA", badge="BOAT LOST",
         head="Boat capsizes in Bayelsa",
         body="A boat of mourners capsized in Bayelsa. (Punch)",
         src="Punch", scene="boat"),
    dict(place="BITCOIN", tag="MARKETS", badge="$58,983",
         head="Bitcoin slides below $59,000",
         body="Bitcoin fell 3.9% as the Nasdaq sank 5.28%. (CoinDesk)",
         src="CoinDesk", scene="bitcoin"),
    dict(place="HORMUZ", tag="DRONES", badge="US DENIES",
         head="US denies Iran downed a drone",
         body="Iran claimed an MQ-9 kill; US denies it. (Reuters)",
         src="Reuters", scene="hormuz"),
    dict(place="CANBERRA", tag="AI SAFETY", badge="AI TALKS",
         head="Australia, China talk AI safety",
         body="Canberra and Beijing keep talking on AI risks. (Reuters)",
         src="Reuters", scene="aitalks"),
]

MORE = [
    (14, "Kyiv: Zelensky warns Crimea bridge 'will not stay' (NBC)"),
    (15, "France arrests terror suspect linked to ex-spy plot (AFP)"),
    (16, "Measles: US loses elimination status as cases spread (CDC)"),
    (17, "Sydney police hunt car after Bondi shooting (ABC)"),
    (18, "Riyadh: Houthi warhead parts recovered from debris (SPA)"),
    (19, "UK judge okays Bayer's $7.25bn Roundup settlement (Reuters)"),
    (20, "Trump: Zelensky has until Thursday to back the plan (Reuters)"),
    (21, "Trump says $2,000 tariff dividend checks are coming (NBC)"),
    (22, "Germany: 1 dead in stabbing at a Berlin train station (Bild)"),
    (23, "Rubio: the peace plan was authored by the US, he says (AP)"),
    (24, "COP31: EU, Panama fight to save fossil-fuel line (HPW)"),
    (25, "FBI: cyberattack exposed US police database NCIC (Reuters)"),
    (26, "Australia: 5 die in house fire; murder charges laid (ABC)"),
    (27, "Ukraine: drone hits Zaporizhzhia plant district (Kyiv Post)"),
    (28, "India: 15 die in fire at a Hyderabad chemical plant (NDTV)"),
    (29, "Markets: S&P 500 falls 3.7% in the AI rout (Reuters)"),
    (30, "Nvidia: shares slide ~14% after record run (Bloomberg)"),
    (31, "Gold: falls 4.62% to $3,515.4 an ounce (Bloomberg)"),
    (32, "Anthropic: shares dip 8.5% after its $2tn IPO debut (CNBC)"),
    (33, "COP31: small-island states demand a fossil phase-out (AP)"),
    (34, "Poland: PM Tusk calls it a deliberate provocation (BBC)"),
    (35, "Turin: Sinner beats Alcaraz to reach the ATP final (AP)"),
    (36, "Argentina: country risk tops 1,000 (Reuters)"),
    (37, "Haiti: Salvadoran troops hit by explosives, 3 hurt (AP)"),
    (38, "Gen Z protests spread across 25 European countries (Euronews)"),
    (39, "CERN: first ultra-rare particle decay observed (CERN)"),
    (40, "US: Agriculture Dept hit in a cyberattack (Reuters)"),
    (41, "Australia: police search for a missing hiker (ABC)"),
    (42, "Space: Blue Origin launches its 6th crewed flight (Space.com)"),
    (43, "Gaza: aid trucks enter as ceasefire holds (Reuters)"),
]

LAND = [
    (2, 2, 14, 7), (4, 7, 13, 9), (6, 9, 9, 11),
    (15, 2, 17, 4),
    (12, 12, 17, 14), (13, 14, 16, 18), (14, 18, 15, 21),
    (24, 3, 30, 5), (25, 5, 28, 7), (24, 6, 25, 7),
    (25, 9, 32, 12), (26, 12, 31, 16), (27, 16, 30, 19),
    (31, 2, 44, 5), (31, 5, 40, 8), (36, 8, 39, 11),
    (40, 8, 44, 11), (40, 11, 44, 12),
    (43, 6, 44, 8),
    (40, 16, 44, 19),
]

PINS = {1: (27, 7), 2: (30, 10), 3: (13, 12), 4: (27, 4), 5: (37, 10), 6: (20, 7),
        7: (23, 4), 8: (8, 7), 9: (43, 16), 10: (23, 10), 11: (13, 6),
        12: (32, 7), 13: (40, 15)}


def scene_cop(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (70, 130, 200), (30, 80, 160))
    cx, cy, r = x + w * 0.42, y + h * 0.56, h * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 140, 90), outline=(255, 255, 255), width=3 * SS)
    for bx, by, br in ((0.38, 0.48, 0.16), (0.52, 0.62, 0.12), (0.30, 0.66, 0.10)):
        d.ellipse([x + w * bx - br * h, y + h * by - br * h, x + w * bx + br * h, y + h * by + br * h],
                  fill=(40, 110, 70))
    kx, ky, kr = x + w * 0.78, y + h * 0.30, h * 0.22
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=(30, 30, 30), width=3 * SS)
    d.line([kx, ky, kx, ky - kr * 0.6], fill=(20, 20, 20), width=4 * SS)
    d.line([kx, ky, kx + kr * 0.5, ky], fill=(20, 20, 20), width=4 * SS)


def scene_riyadh(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (14, 18, 48), (30, 34, 70))
    for bx, bw, bh in ((0.02, 0.12, 0.30), (0.16, 0.09, 0.20), (0.28, 0.14, 0.36),
                       (0.46, 0.10, 0.24), (0.60, 0.13, 0.34), (0.76, 0.11, 0.22),
                       (0.89, 0.09, 0.30)):
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(58, 62, 96))
        for k in range(3):
            wx = x + w * (bx + 0.02 + k * 0.035)
            wy = y + h - h * bh * (0.65 if k % 2 else 0.4)
            d.rectangle([wx, wy, wx + 6 * SS, wy + 6 * SS], fill=(255, 220, 120))
    for fx in (0.24, 0.52, 0.80):
        bx, by = x + w * fx, y + h * 0.30
        d.line([bx + w * 0.10, y + h * 0.88, bx, by], fill=(255, 210, 90), width=5 * SS)
        d.ellipse([bx - 16 * SS, by - 16 * SS, bx + 16 * SS, by + 16 * SS], fill=(255, 150, 40))
        d.ellipse([bx - 8 * SS, by - 8 * SS, bx + 8 * SS, by + 8 * SS], fill=(255, 220, 120))


def scene_quake(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (90, 70, 50), (50, 38, 28))
    d.polygon([(x, y + h), (x + w * 0.25, y + h * 0.45), (x + w * 0.45, y + h),
               (x + w * 0.65, y + h * 0.55), (x + w * 0.85, y + h), (x + w, y + h)],
              fill=(40, 30, 22))
    pts = [(x + w * a, y + h * b) for a, b in
           ((0.03, 0.42), (0.14, 0.42), (0.20, 0.28), (0.26, 0.58), (0.33, 0.34),
            (0.40, 0.50), (0.48, 0.26), (0.56, 0.60), (0.64, 0.36), (0.72, 0.48),
            (0.80, 0.30), (0.88, 0.46), (0.97, 0.42))]
    d.line(pts, fill=(255, 60, 40), width=5 * SS, joint="curve")


def scene_kyiv(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (20, 22, 44), (48, 30, 26))
    for bx, bw, bh in ((0.04, 0.14, 0.42), (0.22, 0.11, 0.30), (0.38, 0.15, 0.48),
                       (0.58, 0.12, 0.34), (0.74, 0.14, 0.44)):
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(16, 16, 28))
    for fx, fy, fr in ((0.30, 0.62, 0.10), (0.66, 0.58, 0.13), (0.86, 0.66, 0.09)):
        cx, cy, r = x + w * fx, y + h * fy, h * fr
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 30))
        d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=(255, 210, 90))


def scene_jet(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (140, 190, 235), (200, 225, 245))
    sx, sy, sr = x + w * 0.82, y + h * 0.22, h * 0.14
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 220, 90))
    cx, cy = x + w * 0.50, y + h * 0.55
    d.ellipse([cx - w * 0.34, cy - h * 0.16, cx + w * 0.34, cy + h * 0.16], fill=(255, 255, 255))
    d.polygon([(cx + w * 0.10, cy), (cx + w * 0.30, cy - h * 0.30), (cx + w * 0.36, cy - h * 0.28),
               (cx + w * 0.22, cy + h * 0.02)], fill=(220, 230, 240))
    d.polygon([(cx - w * 0.05, cy + h * 0.10), (cx - w * 0.20, cy + h * 0.34),
               (cx - w * 0.14, cy + h * 0.36), (cx + w * 0.05, cy + h * 0.12)], fill=(220, 230, 240))
    d.rectangle([cx - w * 0.34, cy - h * 0.05, cx - w * 0.20, cy + h * 0.05], fill=(200, 60, 60))


def scene_mercury(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (8, 8, 18), (20, 16, 34))
    for sx, sy in ((0.12, 0.18), (0.28, 0.10), (0.72, 0.14), (0.88, 0.30), (0.18, 0.78), (0.85, 0.80)):
        d.ellipse([x + w * sx - 2 * SS, y + h * sy - 2 * SS, x + w * sx + 2 * SS, y + h * sy + 2 * SS],
                  fill=(255, 255, 255))
    cx, cy, r = x + w * 0.48, y + h * 0.52, h * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(170, 120, 80), outline=(120, 80, 50), width=3 * SS)
    for bx, by, br in ((0.40, 0.44, 0.07), (0.56, 0.60, 0.09), (0.48, 0.66, 0.06)):
        d.ellipse([x + w * bx - br * h, y + h * by - br * h, x + w * bx + br * h, y + h * by + br * h],
                  fill=(130, 85, 55))


def scene_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.5], fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.5, x + w, y + h], fill=(220, 40, 50))
    for tx in (0.18, 0.50, 0.82):
        d.polygon([(x + w * tx, y + h * 0.12), (x + w * (tx - 0.09), y + h * 0.52),
                   (x + w * (tx + 0.09), y + h * 0.52)], fill=(20, 110, 60))
        d.rectangle([x + w * (tx - 0.015), y + h * 0.52, x + w * (tx + 0.015), y + h * 0.66],
                    fill=(90, 60, 30))


def scene_vegas(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (30, 20, 60), (70, 40, 90))
    for i in range(8):
        c = (255, 255, 255) if i % 2 == 0 else (20, 20, 20)
        d.rectangle([x + w * i / 8, y, x + w * (i + 1) / 8, y + h * 0.10], fill=c)
    cx, cy = x + w * 0.50, y + h * 0.58
    d.rectangle([cx - w * 0.34, cy - h * 0.16, cx + w * 0.34, cy + h * 0.12], fill=(220, 30, 30))
    d.rectangle([cx - w * 0.10, cy - h * 0.30, cx + w * 0.16, cy - h * 0.14], fill=(180, 20, 20))
    for wx in (-0.22, 0.22):
        d.ellipse([cx + w * wx - 9 * SS, cy + h * 0.10 - 9 * SS, cx + w * wx + 9 * SS, cy + h * 0.10 + 9 * SS],
                  fill=(15, 15, 15))


def scene_cricket(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (40, 140, 70), (20, 100, 50))
    d.ellipse([x + w * 0.50 - w * 0.30, y + h * 0.55, x + w * 0.50 + w * 0.30, y + h * 0.95],
              fill=(210, 190, 150))
    d.rectangle([x + w * 0.42, y + h * 0.18, x + w * 0.50, y + h * 0.62], fill=(150, 110, 60))
    d.rectangle([x + w * 0.44, y + h * 0.08, x + w * 0.48, y + h * 0.20], fill=(120, 85, 45))
    bx, by, br = x + w * 0.74, y + h * 0.30, h * 0.09
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255), outline=(180, 40, 40), width=2 * SS)


def scene_boat(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (120, 180, 220), (40, 110, 180))
    for wy in (0.62, 0.74, 0.86):
        pts = [(x + w * a, y + h * wy + h * 0.03 * math.sin(a * 12)) for a in
               [i / 10 for i in range(11)]]
        d.line(pts, fill=(255, 255, 255), width=4 * SS, joint="curve")
    cx, cy = x + w * 0.50, y + h * 0.50
    d.polygon([(cx - w * 0.30, cy), (cx + w * 0.30, cy), (cx + w * 0.20, cy + h * 0.16),
               (cx - w * 0.20, cy + h * 0.16)], fill=(120, 75, 40))
    d.polygon([(cx, cy - h * 0.28), (cx, cy), (cx + w * 0.18, cy)], fill=(255, 255, 255))


def scene_bitcoin(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (255, 200, 60), (245, 160, 20))
    pts = [(x + w * a, y + h * b) for a, b in
           ((0.04, 0.62), (0.20, 0.40), (0.34, 0.55), (0.50, 0.28), (0.66, 0.50), (0.82, 0.30), (0.96, 0.42))]
    d.line(pts, fill=(178, 34, 34), width=5 * SS, joint="curve")
    cx, cy, r = x + w * 0.50, y + h * 0.52, h * 0.40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 150, 30), outline=(200, 110, 10), width=3 * SS)
    d.text((cx - 12 * SS, cy - 24 * SS), "B", font=SERIF_B(44), fill=(255, 255, 255))


def scene_hormuz(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (90, 140, 200), (30, 80, 140))
    sx, sy, sr = x + w * 0.80, y + h * 0.20, h * 0.12
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 220, 120))
    cx, cy = x + w * 0.48, y + h * 0.46
    d.ellipse([cx - w * 0.16, cy - h * 0.10, cx + w * 0.16, cy + h * 0.10], fill=(120, 120, 130))
    d.rectangle([cx - w * 0.34, cy - h * 0.03, cx - w * 0.14, cy + h * 0.03], fill=(90, 90, 100))
    d.rectangle([cx + w * 0.14, cy - h * 0.03, cx + w * 0.34, cy + h * 0.03], fill=(90, 90, 100))
    d.rectangle([cx - w * 0.02, cy - h * 0.22, cx + w * 0.02, cy + h * 0.22], fill=(100, 100, 110))


def scene_aitalks(d, x, y, w, h):
    vgrad(d, (x, y, x + w, y + h), (16, 20, 44), (40, 40, 80))
    for cx, cy, col, lab in ((0.30, 0.62, (140, 90, 210), "AI"), (0.70, 0.62, (40, 180, 120), "AU")):
        px, py, r = x + w * cx, y + h * cy, h * 0.30
        d.ellipse([px - r, py - r, px + r, py + r], fill=col, outline=(255, 255, 255), width=3 * SS)
        d.text((px - 14 * SS, py - 14 * SS), lab, font=SANS_B(16), fill=(255, 255, 255))


SCENES = {"cop": scene_cop, "riyadh": scene_riyadh, "quake": scene_quake, "kyiv": scene_kyiv,
          "jet": scene_jet, "mercury": scene_mercury, "poland": scene_poland, "vegas": scene_vegas,
          "cricket": scene_cricket, "boat": scene_boat, "bitcoin": scene_bitcoin,
          "hormuz": scene_hormuz, "aitalks": scene_aitalks}


def card_frame(d, x, y, cw, ch, pic_h, card, num, hero):
    d.rectangle([x, y, x + cw, y + ch], fill=PAPER, outline=(200, 192, 172), width=2 * SS)
    SCENES[card["scene"]](d, x, y, cw, pic_h)
    banner(d, x, y, cw, card["badge"])
    srcstrip(d, x, y, cw, pic_h, card["src"])
    ty = y + pic_h + 8 * SS
    d.text((x + 10 * SS, ty), str(num), font=SERIF_B(13), fill=RED)
    d.text((x + 34 * SS, ty + 2 * SS), card["place"] + " · " + card["tag"],
           font=SANS_B(10), fill=RED)
    tw = cw - 20 * SS
    hl = wrap(d, card["head"], SERIF_B(14 if hero else 12), tw)
    by = ty + 30 * SS
    for i, ln in enumerate(hl[:2]):
        d.text((x + 10 * SS, by + i * 26 * SS), ln, font=SERIF_B(14 if hero else 12), fill=INK)
    bl = wrap(d, card["body"], SANS(11 if hero else 10), tw)
    by2 = by + 2 * 26 * SS + 4 * SS
    for i, ln in enumerate(bl[:2]):
        d.text((x + 10 * SS, by2 + i * 20 * SS), ln, font=SANS(11 if hero else 10), fill=(50, 48, 44))
    return len(hl), len(bl)


def draw_map(d, x, y, w, h):
    gx, gy = 44, 22
    dx, dy = w / gx, h / gy
    for r in range(gy):
        for c in range(gx):
            if any(x0 <= c < x1 and y0 <= r < y1 for x0, y0, x1, y1 in LAND):
                cx, cy = x + (c + 0.5) * dx, y + (r + 0.5) * dy
                d.ellipse([cx - 4 * SS, cy - 4 * SS, cx + 4 * SS, cy + 4 * SS],
                          fill=(178, 158, 118))
    for n, (c, r) in PINS.items():
        cx, cy = x + (c + 0.5) * dx, y + (r + 0.5) * dy
        d.ellipse([cx - 8 * SS, cy - 8 * SS, cx + 8 * SS, cy + 8 * SS], fill=RED,
                  outline=(255, 255, 255), width=2 * SS)
        d.text((cx - 4 * SS, cy - 6 * SS), str(n), font=SANS_B(7), fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # header band
    d.rectangle([0, 0, W, 60 * SS], fill=NAVY)
    d.text((MX, 16 * SS), "THE WORLD IN ONE DAY", font=SANS_B(11), fill=(255, 255, 255))
    band_r = "43 STORIES · 7 REGIONS · 15 FIELDS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - MX - d.textlength(band_r, font=SANS_B(10)), 18 * SS), band_r,
           font=SANS_B(10), fill=(255, 220, 120))
    # masthead
    title = "Saturday 21 November 2026"
    d.text(((W - d.textlength(title, font=SERIF_B(52))) / 2, 72), title,
           font=SERIF_B(52), fill=INK)
    # timeline (single line, under the masthead)
    d.rectangle([MX, 184, MX + 200, 212], fill=RED)
    d.text((MX + 10, 190), "THE DAY IN UTC", font=SANS_B(9), fill=(255, 255, 255))
    for i, (t, cap) in enumerate(TIMELINE):
        sx = 236 + i * 444
        d.text((sx, 188), t, font=SANS_B(10), fill=RED)
        tw = d.textlength(t, font=SANS_B(10))
        d.text((sx + tw + 8, 188), cap, font=SANS(10), fill=INK)
    d.line([MX, 228, W - MX, 228], fill=(200, 192, 172), width=2 * SS)
    d.line([MX, 228, W - MX, 228], fill=(200, 192, 172), width=2 * SS)
    # numbers strip
    seg = (W - 2 * MX) / 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = MX + seg * i + seg / 2
        d.text((cx - d.textlength(num, font=SERIF_B(26)) / 2, 236), num,
               font=SERIF_B(26), fill=RED)
        d.text((cx - d.textlength(cap, font=SANS(9)) / 2, 288), cap,
               font=SANS(9), fill=MUT)
        if i:
            d.line([MX + seg * i, 240, MX + seg * i, 312], fill=(210, 202, 182), width=2 * SS)
    d.line([MX, 328, W - MX, 328], fill=(200, 192, 172), width=2 * SS)
    # region bar
    tot = sum(n for _, n, _ in REGIONS)
    x = MX
    for name, n, col in REGIONS:
        segw = (W - 2 * MX) * n / tot
        d.rectangle([x, 336, x + segw, 372], fill=col)
        label = f"{name} {n}"
        d.text((x + (segw - d.textlength(label, font=SANS_B(9))) / 2, 344),
               label, font=SANS_B(9), fill=(255, 255, 255))
        x += segw
    # heroes
    gap = 16
    hw = (W - 2 * MX - 2 * gap) // 3
    pic_h = 72 * SS
    frame_h = pic_h + 134 * SS
    counts = []
    for i in range(3):
        counts.append(card_frame(d, MX + i * (hw + gap), 384, hw, frame_h, pic_h,
                                 CARDS[i], i + 1, True))
    # mediums
    mw = (W - 2 * MX - 4 * gap) // 5
    mpic = 54 * SS
    mframe = mpic + 122 * SS
    for row in range(2):
        for col in range(5):
            idx = 3 + row * 5 + col
            counts.append(card_frame(d, MX + col * (mw + gap), 812 + row * 368,
                                     mw, mframe, mpic, CARDS[idx], idx + 1, False))
    # bottom header
    d.text((MX, 1548), "WHERE IT HAPPENED", font=SANS_B(11), fill=INK)
    d.text((296, 1548), "ALSO ON SATURDAY 21 NOVEMBER — 30 MORE STORIES",
           font=SANS_B(11), fill=INK)
    # map
    draw_map(d, MX, 1584, 500, 270)
    d.text((MX, 1860), "PACIFIC", font=SANS(9), fill=MUT)
    d.text((MX + 500 - d.textlength("ATLANTIC", font=SANS(9)), 1860), "ATLANTIC",
           font=SANS(9), fill=MUT)
    # list
    lx, colw = 296, 700
    for i, (n, t) in enumerate(MORE):
        col = i // 15
        row = i % 15
        tx = lx + col * (colw + 20 * SS)
        ty = 1584 + row * 24
        d.text((tx, ty), str(n), font=SANS_B(11), fill=RED)
        d.text((tx + 26 * SS, ty), t, font=SANS(11), fill=(50, 48, 44))
    # date check box
    d.rectangle([MX, 1952, W - MX, 2010], outline=RED, width=2 * SS)
    d.text((MX + 10 * SS, 1958),
           "DATE CHECK — Left out on purpose: UK–EU deal (Fri), Geneva talks (Sun 23), ICJ ruling (Thu 19), Anthropic debut + GTA VI (19 Nov).",
           font=SANS(11), fill=INK)
    d.text((MX + 10 * SS, 1984),
           "Not yet: COP31 final draft, ATP final (Sun 22). Tags: CONFIRMED = 2+ outlets · OFFICIAL = on the record · REPORTED = one outlet.",
           font=SANS(11), fill=INK)
    # footer
    d.text((MX, 2018), "Every story here happened or was first reported on Sat 21 Nov 2026.",
           font=SANS(10), fill=GREY)
    ft = "SATURDAY 21 NOVEMBER 2026 · ONE PAGE"
    d.text((W - MX - d.textlength(ft, font=SANS_B(11)), 2018), ft,
           font=SANS_B(11), fill=GREY)
    out = img.resize((1024, 1024), Image.LANCZOS)
    grain(out, amp=4)
    out.save("entry.png", format="PNG")
    print("wrap counts (head, body) per card:", counts)
    print("saved entry.png")


if __name__ == "__main__":
    build()
