"""All glyphs, drawn on an 11 x 11 BLOCK grid (measured from the reference).

Measured from "Pixel Icons #001" (see tools/reference_bitmaps.txt):
  - icons are 24 px with a 2 px stroke  ->  1 block = 2 px, stroke = 1 block
  - biggest icon = 22 px = 11 blocks; most are 9-11 blocks wide
  - an icon uses only ~30-40 blocks (avg 134 lit px of 576)
  - corners: the corner block is left out (1 block chamfer)
  - gaps: 1 block between an outline and anything inside / overlapping
  - dots: 1 block
  - one colour per icon: orange #EE5A2D or grey #5E5E5E, checkerboard; no white
Every glyph is centred automatically (odd sizes in the exact centre, even sizes
shifted by half a block = 1 px), so coordinates below are only relative.
"""
from geo import rect, disk, ellipse, outline, line, path, hl, vl, ring, over, grow

ICONS = {}


def icon(fn):
    ICONS[fn.__name__] = fn
    return fn


def art(s):
    """ASCII at block scale: '#' = one block."""
    return {(x, y) for y, row in enumerate(s.strip("\n").split("\n"))
            for x, c in enumerate(row) if c == "#"}


# ------------------------------------------------------------------ system apps

@icon
def phone():
    return art("""
.##........
#..#.......
#..#.......
#.#........
#.#........
#..#.......
.#..#......
..#..#..##.
...#..##..#
....#.....#
.....#####.
""")


@icon
def message():
    g = ring(0, 0, 11, 7)
    g -= {(7, 6), (9, 6)}          # speech tail: gap + one block below
    g |= {(7, 7)}
    g |= {(3, 3), (5, 3), (7, 3)}
    return g


@icon
def contacts():
    head = ring(3, 0, 5, 5)
    body = outline({(x, 6) for x in range(3, 8)} | {(x, 7) for x in range(2, 9)}
                   | {(x, y) for y in range(8, 11) for x in range(1, 10)})
    return head | body


@icon
def camera():
    g = ring(0, 2, 11, 9) | hl(2, 4, 1)          # viewfinder bump on the left
    return g | ring(3, 4, 5, 5)


@icon
def gallery():
    g = ring(0, 0, 11, 9) | {(7, 2)}
    g |= path((1, 7), (4, 4), (7, 7)) | path((6, 6), (7, 5), (9, 7))
    return g


def sliders():
    """Reference-style sliders (kept as an alternate glyph)."""
    g = set()
    for y, k in ((1, 3), (5, 7), (9, 5)):
        g |= hl(0, k - 2, y) | hl(k + 2, 10, y) | vl(k, y - 1, y + 1)
    return g


@icon
def clock():
    """Alarm clock: 9-block face, two bells 1 block off the face, two feet."""
    g = outline(disk(1, 1, 9)) | vl(5, 3, 5) | hl(6, 7, 5)
    bells = {(0, 2), (0, 1), (1, 0), (2, 0), (10, 2), (10, 1), (9, 0), (8, 0)}
    return g | bells | {(2, 10), (8, 10)}


@icon
def calendar():
    g = ring(0, 1, 11, 10) | hl(1, 9, 3) | {(3, 0), (7, 0)}
    return g | {(2, 5), (4, 5), (6, 5), (8, 5), (2, 7), (4, 7), (6, 7)}


@icon
def calculator():
    g = ring(1, 0, 9, 11) | ring(3, 2, 5, 3, 0)
    return g | {(x, y) for y in (6, 8) for x in (3, 5, 7)}


@icon
def folder():
    return outline(rect(0, 0, 5, 3) | rect(0, 1, 11, 8)) | hl(1, 9, 3)


@icon
def globe():
    g = outline(disk(0, 0, 11)) | hl(1, 9, 5)
    return g | {(5, 1), (5, 9)} | vl(4, 2, 8) | vl(6, 2, 8)




@icon
def mail():
    return ring(0, 0, 11, 9) | path((1, 1), (5, 5), (9, 1))


@icon
def pin():
    return art("""
...#####...
..#.....#..
.#.......#.
#....#....#
#...#.#...#
#....#....#
.#.......#.
..#.....#..
...#...#...
....#.#....
.....#.....
""")


@icon
def music():
    g = ring(0, 7, 4, 4) | ring(7, 6, 4, 4)
    return g | vl(3, 0, 7) | vl(10, 0, 6) | hl(3, 10, 0) | hl(3, 10, 2)




@icon
def play():
    return art("""
##.......
#.##.....
#...##...
#.....##.
#.......#
#.....##.
#...##...
#.##.....
##.......
""")




@icon
def youtube():
    return ring(0, 0, 11, 9) | vl(4, 2, 6) | path((4, 2), (6, 4), (4, 6))


@icon
def chat_round():
    g = outline(disk(0, 0, 11) | {(0, 9), (0, 10), (1, 9), (1, 10)})
    return g | {(3, 3), (4, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 7), (7, 6)}


@icon
def insta():
    return ring(0, 0, 11, 11, 2) | ring(3, 3, 5, 5) | {(8, 2)}


@icon
def plane():
    return path((0, 0), (10, 5), (0, 10)) | path((0, 0), (2, 5), (0, 10)) | hl(3, 6, 5)


@icon
def notes():
    g = vl(1, 1, 9) | hl(2, 6, 0) | path((7, 1), (9, 3)) | vl(9, 4, 9) | hl(2, 8, 10)
    g |= vl(6, 1, 3) | hl(7, 8, 3)
    return g | hl(3, 7, 5) | hl(3, 5, 7)


@icon
def weather():
    sun = ring(2, 2, 5, 5) | {(4, 0), (0, 4), (1, 1), (7, 1), (1, 7)}   # dot rays, like the timer
    cloud = rect(5, 5, 4, 3) | rect(3, 7, 8, 4)
    return over(sun, outline(cloud), cloud)




@icon
def download():
    g = vl(5, 0, 6) | path((2, 3), (5, 6)) | path((8, 3), (5, 6))
    return g | path((0, 7), (0, 9), (10, 9), (10, 7))


@icon
def tv():
    return ring(0, 3, 11, 8) | ring(2, 5, 7, 4, 0) | path((3, 0), (5, 2), (7, 0))


@icon
def cart():
    g = path((0, 0), (2, 0), (3, 2)) | path((3, 2), (10, 2), (9, 5), (4, 5), (3, 2))
    return g | {(4, 7), (9, 7)}


@icon
def card():
    return ring(0, 0, 11, 9) | hl(1, 9, 2) | hl(2, 4, 6) | hl(7, 8, 6)


@icon
def x():
    return line(0, 0, 10, 10) | line(10, 0, 0, 10)


@icon
def fb():
    return ring(0, 0, 11, 11, 2) | vl(5, 3, 10) | {(6, 2), (7, 2)} | hl(3, 7, 5)


@icon
def gamepad():
    g = outline(rect(0, 0, 11, 6) | rect(0, 4, 4, 3) | rect(7, 4, 4, 3))
    g |= {(2, 2), (3, 2), (4, 2), (3, 1), (3, 3)}
    return g | {(7, 1), (7, 3), (6, 2), (8, 2)}


@icon
def mic():
    g = ring(3, 0, 5, 7)
    g |= {(1, 4), (1, 5), (1, 6), (2, 7), (3, 8), (9, 4), (9, 5), (9, 6), (8, 7), (7, 8)}
    return g | hl(4, 6, 8) | {(5, 9)} | hl(3, 7, 10)


@icon
def linkedin():
    g = ring(0, 0, 11, 11, 2) | {(3, 3)} | vl(3, 5, 8)
    return g | vl(5, 5, 8) | hl(6, 7, 5) | vl(8, 6, 8)


@icon
def ghost():
    return art("""
...#####...
..#.....#..
.#.......#.
.#.......#.
##.......##
#.........#
.#.......#.
.#.......#.
#.........#
.##.###.##.
...#...#...
""")


@icon
def drive():
    return art("""
.....#.....
....#.#....
....#.#....
...#...#...
...#...#...
..#..#..#..
..#.#.#.#..
.#.#####.#.
.#.......#.
###########
""")




@icon
def lock():
    return (ring(3, 0, 5, 5) - {(4, 4), (5, 4), (6, 4)}) | ring(1, 4, 9, 7) | {(5, 6), (5, 7)}


@icon
def code():
    return path((3, 2), (0, 5), (3, 8)) | path((7, 2), (10, 5), (7, 8)) | line(6, 1, 4, 9)


@icon
def sparkle():
    q = {(5, 0), (5, 1), (4, 2), (4, 3), (3, 4), (2, 4), (1, 5), (0, 5)}
    return {p for (x, y) in q for p in ((x, y), (10 - x, y), (x, 10 - y), (10 - x, 10 - y))}


@icon
def waves():
    g = outline(disk(0, 0, 11))
    return g | hl(3, 7, 3) | hl(3, 7, 5) | hl(4, 6, 7)


@icon
def n():
    return vl(2, 0, 10) | vl(8, 0, 10) | line(3, 1, 7, 9)


@icon
def videocam():
    return ring(0, 2, 7, 7) | path((8, 4), (10, 2), (10, 8), (8, 6), (8, 4))


@icon
def heart():
    return art("""
.###...###.
#...#.#...#
#....#....#
#.........#
.#.......#.
..#.....#..
...#...#...
....#.#....
.....#.....
""")


@icon
def news():
    g = ring(0, 0, 11, 10) | ring(2, 2, 3, 3, 0)
    return g | hl(6, 8, 2) | hl(6, 8, 4) | hl(2, 8, 6) | hl(2, 6, 8)


@icon
def book():
    g = ring(0, 0, 6, 9) | ring(5, 0, 6, 9)
    for y in (2, 4, 6):
        g |= hl(2, 3, y) | hl(7, 8, y)
    return g


@icon
def car():
    g = hl(3, 7, 0) | {(2, 1), (8, 1), (2, 2), (8, 2)}
    g |= ring(0, 3, 11, 5) | {(2, 5), (8, 5)}
    return g | {(1, 8), (2, 8), (8, 8), (9, 8)}


@icon
def pack():
    return ring(0, 0, 5, 5) | ring(6, 0, 5, 5) | ring(0, 6, 5, 5) | ring(6, 6, 5, 5)

# ------------------------------------------------------------------ unique / new

@icon
def settings():
    """Gear: 8 teeth (3 wide on the axes, 2-block hooks on the diagonals), diamond hub."""
    return art("""
....###....
.##.#.#.##.
.#.#...#.#.
..#.....#..
##...#...##
#...#.#...#
##...#...##
..#.....#..
.#.#...#.#.
.##.#.#.##.
....###....
""")


ICONS["sliders"] = sliders

@icon
def maps():
    """Tri-fold paper map with a location drop on the middle panel."""
    fold = rect(0, 1, 3, 10, 0) | rect(2, 0, 7, 10, 0) | rect(8, 1, 3, 10, 0)
    g = outline(fold) | vl(2, 1, 9) | vl(8, 1, 9)
    return g | {(5, 2), (4, 3), (6, 3), (5, 4), (5, 5), (4, 7), (6, 7)}


@icon
def wallet():
    g = ring(0, 2, 11, 9) | hl(2, 7, 0) | {(1, 1), (8, 1)}
    clasp = ring(6, 5, 5, 3, 0)
    return (g - {(10, 6)}) | clasp | {(8, 6)}


@icon
def upi():
    """Rupee sign."""
    return art("""
#######
.....#.
......#
#######
......#
.....#.
#####..
.#.....
..#....
...#...
....#..
""")


@icon
def star_play():
    return art("""
.....#.....
....#.#....
....#.#....
####...####
.#.......#.
..#.....#..
..#.....#..
.#...#...#.
.#..#.#..#.
#..#...#..#
###.....###
""")


@icon
def food():
    return art("""
...#...#...
....#...#..
...#...#...
...........
###########
#.........#
.#.......#.
..#.....#..
...#####...
...........
..#######..
""")


@icon
def bag():
    g = ring(0, 3, 11, 8) | hl(4, 6, 0) | {(3, 1), (3, 2), (7, 1), (7, 2)}
    return g | {(3, 7), (7, 7)} | hl(4, 6, 8)


@icon
def signal():
    return ring(0, 8, 3, 3, 0) | ring(4, 4, 3, 7, 0) | ring(8, 0, 3, 11, 0)
