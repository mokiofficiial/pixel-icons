"""Math-made icons for apps that have no hand-drawn icon yet.

Same design rules as every other icon (11 x 11 blocks, 1 block stroke,
1 block chamfer, 2 block gap around the inner mark). Nothing is random:
the same app always gets the same icon.

  1. h = FNV-1a 32-bit hash of the package name
  2. CATEGORY  - words in the app name / package (bank, music, food, ride...)
                 pick a matching glyph from the pack, if one fits
  3. otherwise a MONOGRAM:
       frame   = FRAMES[h % 5]           circle / rounded / square / octagon / bubble
       letter  = first letter or digit of the app name, 5 x 5 block font
       cuts    = two 1-block gaps in the frame at angle (h >> 8) % 8 * 45 deg
                 and the opposite side (rotational symmetry, like the reference)
       cuts on = ((h >> 4) % 3) != 0     (2 of 3 apps get cuts)
"""
import math
import re

from geo import disk, outline, ring

# ---------------------------------------------------------------- 5x5 block font
_F = """
A .###. #...# ##### #...# #...#
B ####. #...# ####. #...# ####.
C .#### #.... #.... #.... .####
D ####. #...# #...# #...# ####.
E ##### #.... ####. #.... #####
F ##### #.... ####. #.... #....
G .#### #.... #..## #...# .###.
H #...# #...# ##### #...# #...#
I ##### ..#.. ..#.. ..#.. #####
J ..### ...#. ...#. #..#. .##..
K #...# #..#. ###.. #..#. #...#
L #.... #.... #.... #.... #####
M #...# ##.## #.#.# #...# #...#
N #...# ##..# #.#.# #..## #...#
O .###. #...# #...# #...# .###.
P ####. #...# ####. #.... #....
Q .###. #...# #.#.# #..#. .##.#
R ####. #...# ####. #..#. #...#
S .#### #.... .###. ....# ####.
T ##### ..#.. ..#.. ..#.. ..#..
U #...# #...# #...# #...# .###.
V #...# #...# #...# .#.#. ..#..
W #...# #...# #.#.# ##.## #...#
X #...# .#.#. ..#.. .#.#. #...#
Y #...# .#.#. ..#.. ..#.. ..#..
Z ##### ...#. ..#.. .#... #####
0 .###. #..## #.#.# ##..# .###.
1 ..#.. .##.. ..#.. ..#.. .###.
2 ####. ....# .###. #.... #####
3 ####. ....# .###. ....# ####.
4 #...# #...# ##### ....# ....#
5 ##### #.... ####. ....# ####.
6 .###. #.... ####. #...# .###.
7 ##### ....# ...#. ..#.. ..#..
8 .###. #...# .###. #...# .###.
9 .###. #...# .#### ....# .###.
"""
FONT = {}
for _line in _F.strip().split("\n"):
    _k, *_rows = _line.split()
    FONT[_k] = {(x, y) for y, r in enumerate(_rows) for x, c in enumerate(r) if c == "#"}

# ---------------------------------------------------------------- frames (11 x 11)
FRAMES = [
    ("circle",  lambda: outline(disk(0, 0, 11)), 3),
    ("rounded", lambda: ring(0, 0, 11, 11, 2), 3),
    ("square",  lambda: ring(0, 0, 11, 11, 1), 3),
    ("octagon", lambda: ring(0, 0, 11, 11, 3), 3),
    ("bubble",  lambda: (ring(0, 0, 11, 9, 1) - {(1, 8), (3, 8)}) | {(3, 9)}, 2),
]

# ---------------------------------------------------------------- categories
CATEGORIES = [
    ("upi",        "bank pay upi money wallet cash loan finance invest stock trade credit"),
    ("music",      "music song songs radio fm podcast audio beats"),
    ("tv",         "video movie movies tv stream ott cinema series anime"),
    ("gamepad",    "game games gaming ludo chess pubg arcade puzzle"),
    ("gallery",    "photo photos gallery pic pics album"),
    ("camera",     "camera cam selfie scanner scan"),
    ("mail",       "mail email inbox"),
    ("message",    "chat messenger message messages sms talk"),
    ("news",       "news times daily headlines"),
    ("bag",        "shop shopping store mart buy sale fashion"),
    ("food",       "food eat restaurant grocery kitchen recipe delivery"),
    ("maps",       "map maps navigation gps"),
    ("weather",    "weather forecast rain"),
    ("book",       "book books read reader kindle library study learn edu education class school"),
    ("car",        "cab ride rides taxi car bike metro train rail railway bus travel"),
    ("heart",      "fit fitness health gym steps yoga med medical doctor dating"),
    ("notes",      "note notes doc docs office pdf word sheet"),
    ("folder",     "file files drive cloud storage manager"),
    ("clock",      "clock alarm timer stopwatch"),
    ("calculator", "calc calculator"),
    ("calendar",   "calendar planner agenda"),
    ("lock",       "lock vault password secure security vpn authenticator antivirus"),
    ("globe",      "browser web internet"),
    ("phone",      "phone dialer call caller"),
    ("mic",        "mic recorder record voice"),
    ("code",       "code dev developer terminal git ide"),
    ("sparkle",    "ai gpt assistant bot copilot"),
    ("download",   "download downloader torrent"),
    ("settings",   "settings setting tools cleaner booster"),
]


def fnv1a(s):
    h = 0x811C9DC5
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 0x01000193) & 0xFFFFFFFF
    return h


def tokens(*texts):
    out = set()
    for t in texts:
        # split words, package dots and camelCase
        t = re.sub(r"([a-z])([A-Z])", r"\1 \2", t)
        out |= {w for w in re.split(r"[^a-z0-9]+", t.lower()) if w}
    return out


def category(name, package):
    words = tokens(name, package)
    for glyph, keys in CATEGORIES:
        if words & set(keys.split()):
            return glyph
    return None


def monogram(name, package):
    h = fnv1a(package)
    fname, frame_fn, pad = FRAMES[h % len(FRAMES)]
    frame = frame_fn()
    if (h >> 4) % 3 != 0:
        a0 = ((h >> 8) % 8) * 45
        c = 5.0
        cut = set()
        for (x, y) in frame:
            a = math.degrees(math.atan2(y - c, x - c)) % 360
            for t in (a0, a0 + 180):
                if abs((a - t + 180) % 360 - 180) < 9:
                    cut.add((x, y))
        frame -= cut
    ch = next((c for c in name.upper() if c in FONT), "A")
    oy = pad if fname != "bubble" else 2
    letter = {(x + 3, y + oy) for (x, y) in FONT[ch]}
    return frame | letter, f"{fname} + '{ch}'"


def make(name, package):
    """Returns (glyph_name_or_None, blocks_or_None, how)."""
    cat = category(name, package)
    if cat:
        return cat, None, f"category -> {cat}"
    blocks, how = monogram(name, package)
    return None, blocks, f"monogram: {how}"
