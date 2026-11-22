"""Tiny pixel-geometry kit. Every icon is built from these, on one 24x24 grid.

DESIGN SYSTEM (same for every icon)
  grid ......... 24 x 24 px
  live area .... 20 x 20 px  (2 px padding on every side, x/y 2..21)
  stroke ....... 1 px, outlines only
  corners ...... 1 px chamfer (rounded look); 3 px for "app-tile" squares
  inner gap .... 2 px empty between an outline and anything inside it
  overlaps ..... 1 px knock-out gap where two shapes cross
  dots ......... 2 x 2 px
  keylines ..... circle 20, square 18, landscape 20x14, portrait 14x20
  centre ....... 11.5 (between pixel 11 and 12) - shapes use even sizes
"""
import math

N = 24


# ---------- filled masks (sets of (x, y)) ----------

def rect(x, y, w, h, ch=1):
    """Filled rectangle with chamfered corners (ch = corner cut in px)."""
    m = set()
    for j in range(y, y + h):
        for i in range(x, x + w):
            dx = min(i - x, x + w - 1 - i)
            dy = min(j - y, y + h - 1 - j)
            if dx + dy >= ch:
                m.add((i, j))
    return m


def ellipse(x, y, w, h):
    """Filled ellipse fitted in the box (x, y, w, h)."""
    cx, cy = x + (w - 1) / 2, y + (h - 1) / 2
    rx, ry = w / 2 - 0.2, h / 2 - 0.2
    return {(i, j) for j in range(y, y + h) for i in range(x, x + w)
            if ((i - cx) / rx) ** 2 + ((j - cy) / ry) ** 2 <= 1}


def disk(x, y, d):
    return ellipse(x, y, d, d)


def poly(*pts):
    """Filled polygon, pixel centres tested (points in pixel coords)."""
    m = set()
    for j in range(N):
        for i in range(N):
            if _inside(i, j, pts):
                m.add((i, j))
    return m


def _inside(x, y, pts):
    c = False
    n = len(pts)
    for k in range(n):
        (x1, y1), (x2, y2) = pts[k], pts[(k + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def where(m, fn):
    return {p for p in m if fn(*p)}


def grow(m, r=1):
    out = set(m)
    for (x, y) in m:
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                out.add((x + dx, y + dy))
    return out


def outline(m):
    """1 px, 8-connected border of a filled mask."""
    return {(x, y) for (x, y) in m
            if any(n not in m for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))}


# ---------- strokes ----------

def line(x0, y0, x1, y1):
    pts = set()
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.add((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def path(*pts):
    out = set()
    for a, b in zip(pts, pts[1:]):
        out |= line(*a, *b)
    return out


def hl(x0, x1, y):
    return {(x, y) for x in range(x0, x1 + 1)}


def vl(x, y0, y1):
    return {(x, y) for y in range(y0, y1 + 1)}


def dot(x, y, w=2, h=2):
    return rect(x, y, w, h, 0)


def ring(x, y, w, h=None, ch=1):
    return outline(rect(x, y, w, h if h else w, ch))


def circle(x, y, d):
    return outline(disk(x, y, d))


def over(base, top, area=None, gap=1):
    """Put `top` over `base`, clearing a 1 px gap around `area` (the top
    shape's filled mask) - the overlapping-shapes look of the reference."""
    return (base - grow(area if area else top, gap)) | top


def mirror_x(m):
    return {(N - 1 - x, y) for (x, y) in m}
