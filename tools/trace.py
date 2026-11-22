"""Turn an app's ORIGINAL icon into a pixel icon of this pack - by math.

Same steps run inside the Android app (MissingActivity.java) on the real
icons installed on the phone; this file is the reference version for the PC.

  1. input  : 96 x 96 RGBA (adaptive icons: the foreground layer, centre 2/3)
  2. colours: opaque pixels -> k-means (k <= 3, fixed start = most common
              colours) -> every pixel gets a label; transparent = 0 (background).
              If the image border is mostly one opaque colour, that colour is
              background too (full-bleed icons).
  3. fit    : square box around the non-background pixels -> 11 x 11 blocks;
              a block takes the majority label, background if < 35 % covered.
  4. outline: a block is lit when it is non-background and touches background
              or the grid edge, or touches a different colour region with a
              higher label (so a colour border is drawn once, 1 block thick).
  5. thin   : Zhang-Suen thinning, so every line is 1 block thick
  6. sanity : > 60 lit blocks -> silhouette only; < 8 -> filled shape.
  7. colour : biggest colour of the whole icon warm (red / orange / yellow) -> orange, else grey.
Result is encoded as 31 hex digits (121 bits, row by row) so it can travel as
text: "App Name | package/activity | g=<hex> c=o"
"""
import colorsys

S = 96
G = 11


def _dist2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def trace(px):
    """px: list of S*S (r, g, b, a). Returns (set of (x, y) blocks, 'o'|'g')."""
    opaque = [i for i in range(S * S) if px[i][3] > 100]
    if not opaque:
        return set(), "g"

    # --- k-means with a fixed start: the most common 4-bit-quantised colours
    hist = {}
    for i in opaque:
        r, g, b, _ = px[i]
        k = (r >> 4, g >> 4, b >> 4)
        hist[k] = hist.get(k, 0) + 1
    cents = []
    for k, _ in sorted(hist.items(), key=lambda kv: (-kv[1], kv[0])):
        c = (k[0] * 16 + 8, k[1] * 16 + 8, k[2] * 16 + 8)
        if all(_dist2(c, o) > 60 * 60 for o in cents):
            cents.append(c)
        if len(cents) == 3:
            break
    lab = [0] * (S * S)
    for _ in range(6):
        sums = [[0, 0, 0, 0] for _ in cents]
        for i in opaque:
            p = px[i]
            j = min(range(len(cents)), key=lambda c: _dist2(p, cents[c]))
            lab[i] = j + 1
            s = sums[j]
            s[0] += p[0]; s[1] += p[1]; s[2] += p[2]; s[3] += 1
        cents = [(s[0] // s[3], s[1] // s[3], s[2] // s[3]) if s[3] else cents[j]
                 for j, s in enumerate(sums)]

    # --- full-bleed: a colour that covers most of the border is background
    border = [i for i in range(S * S) if i % S in (0, S - 1) or i // S in (0, S - 1)]
    cnt = {}
    for i in border:
        cnt[lab[i]] = cnt.get(lab[i], 0) + 1
    top, n = max(cnt.items(), key=lambda kv: kv[1])
    bg = {0}
    if top != 0 and n > 0.6 * len(border):
        bg.add(top)

    fg = [i for i in range(S * S) if lab[i] not in bg]
    if not fg:
        return set(), "g"
    xs = [i % S for i in fg]
    ys = [i // S for i in fg]
    x0, x1, y0, y1 = min(xs), max(xs) + 1, min(ys), max(ys) + 1
    side = max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    bx0, by0 = cx - side / 2, cy - side / 2

    # --- 11 x 11 grid, majority label per block
    grid = [[0] * G for _ in range(G)]
    for gy in range(G):
        for gx in range(G):
            votes = {}
            tot = 0
            for yy in range(int(by0 + gy * side / G), int(by0 + (gy + 1) * side / G)):
                for xx in range(int(bx0 + gx * side / G), int(bx0 + (gx + 1) * side / G)):
                    tot += 1
                    if 0 <= xx < S and 0 <= yy < S:
                        l = lab[yy * S + xx]
                        if l not in bg:
                            votes[l] = votes.get(l, 0) + 1
            if tot and sum(votes.values()) >= 0.35 * tot:
                grid[gy][gx] = max(votes.items(), key=lambda kv: (kv[1], -kv[0]))[0]

    def at(x, y):
        return grid[y][x] if 0 <= x < G and 0 <= y < G else 0

    def outline(colour_edges):
        out = set()
        for y in range(G):
            for x in range(G):
                l = grid[y][x]
                if not l:
                    continue
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    m = at(nx, ny)
                    if m == 0 or (colour_edges and m != l and m > l):
                        out.add((x, y))
                        break
        return out

    blocks = thin(outline(True))
    if len(blocks) > 60:
        blocks = thin(outline(False))
    if len(blocks) < 8:
        blocks = {(x, y) for y in range(G) for x in range(G) if grid[y][x]}

    return blocks, "o" if warm(px) else "g"


def warm(px):
    """Colour rule on the whole icon: most common 4-bit colour, averaged with its
    neighbours (distance < 60) -> warm (red / orange / yellow) means orange."""
    hist = {}
    for (r, g, b, a) in px:
        if a > 100:
            k = (r >> 4) << 8 | (g >> 4) << 4 | (b >> 4)
            hist[k] = hist.get(k, 0) + 1
    if not hist:
        return False
    k = min(hist, key=lambda q: (-hist[q], q))
    c0 = ((k >> 8 & 15) * 16 + 8, (k >> 4 & 15) * 16 + 8, (k & 15) * 16 + 8)
    near = [p for p in px if p[3] > 100 and _dist2(p, c0) < 3600]
    r = sum(p[0] for p in near) // len(near)
    g = sum(p[1] for p in near) // len(near)
    b = sum(p[2] for p in near) // len(near)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return s > 0.35 and 0.15 < l < 0.85 and (h < 0.17 or h > 0.92)



def thin(b):
    """Zhang-Suen thinning: 2-block-thick parts -> 1 block (the pack's stroke)."""
    b = set(b)
    while True:
        changed = False
        for step in (0, 1):
            kill = []
            for (x, y) in b:
                n = [(x, y - 1) in b, (x + 1, y - 1) in b, (x + 1, y) in b, (x + 1, y + 1) in b,
                     (x, y + 1) in b, (x - 1, y + 1) in b, (x - 1, y) in b, (x - 1, y - 1) in b]
                B = sum(n)
                A = sum(1 for k in range(8) if not n[k] and n[(k + 1) % 8])
                p2, p4, p6, p8 = n[0], n[2], n[4], n[6]
                if 2 <= B <= 6 and A == 1 and (
                        (step == 0 and not (p2 and p4 and p6) and not (p4 and p6 and p8)) or
                        (step == 1 and not (p2 and p4 and p8) and not (p2 and p6 and p8))):
                    kill.append((x, y))
            if kill:
                b -= set(kill)
                changed = True
        if not changed:
            return b


def encode(blocks):
    v = 0
    for (x, y) in blocks:
        v |= 1 << (y * G + x)
    return f"{v:031x}"


def decode(hexstr):
    v = int(hexstr, 16)
    return {(i % G, i // G) for i in range(G * G) if v >> i & 1}


def from_file(path):
    from PIL import Image
    im = Image.open(path).convert("RGBA").resize((S, S), Image.LANCZOS)
    data = im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata()
    return trace(list(data))
