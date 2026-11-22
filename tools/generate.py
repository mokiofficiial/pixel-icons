"""Renders the pixel icons and writes every Android icon-pack resource.

Run:  python tools/generate.py
"""
import os
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from icons import ICONS  # noqa: E402
from apps import APPS  # noqa: E402
import re  # noqa: E402
from auto import make, fnv1a  # noqa: E402
from trace import decode, from_file  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "android", "app", "src", "main")
RES = os.path.join(APP, "res")

SIZE = 192          # px per icon (xxxhdpi launcher size)
U = 4               # 1 grid px (of the 24 px icon) = 4 px  -> icon 96 px, glyph max 88 px
OFF = (SIZE - 24 * U) // 2    # glyph ~46% of the tile, like the reference (60 of 138)
BG = (0, 0, 0)                # reference background
GRID = (20, 20, 20)           # reference cell lines
COLORS = {"o": (238, 90, 45), "g": (94, 94, 94)}   # measured medians

# checkerboard orange / grey, like the reference sheet (6 per row)
for _i, _k in enumerate(list(APPS)):
    _g, _c, _comps = APPS[_k]
    APPS[_k] = (_g, "o" if (_i + _i // 6) % 2 == 0 else "g", _comps)


def load_requests():
    """Apps from tools/requests.txt get a math-made icon (see tools/auto.py)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requests.txt")
    known = {c for (_, _, comps) in APPS.values() for c in comps}
    made = []
    if not os.path.exists(path):
        return made
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "|" not in line:
            continue
        parts = [t.strip() for t in line.split("|")]
        name, comp, extra = parts[0], parts[1], (parts[2] if len(parts) > 2 else "")
        if comp in known or "/" not in comp:
            continue
        pkg = comp.split("/")[0]
        slug = "auto_" + re.sub(r"[^a-z0-9_]", "_", pkg.lower())
        opts = dict(kv.split("=", 1) for kv in extra.split() if "=" in kv)
        color = "o" if fnv1a(pkg) % 2 == 0 else "g"
        if "g" in opts:                       # traced on the phone from the real icon
            blocks, glyph, how = decode(opts["g"]), slug, "traced from app icon (phone)"
            color = opts.get("c", color)
        elif "img" in opts:                   # traced here from an icon file
            img = opts["img"]
            if not os.path.isabs(img):
                img = os.path.join(os.path.dirname(path), img)
            blocks, color = from_file(img)
            glyph, how = slug, "traced from " + os.path.basename(img)
        else:                                 # no icon given: category glyph / monogram
            glyph, blocks, how = make(name, pkg)
            if blocks is not None:
                glyph = slug
        if blocks is not None:
            ICONS[slug] = (lambda b=blocks: b)
        if slug in APPS:
            APPS[slug][2].append(comp)
        else:
            APPS[slug] = (glyph, color, [comp])
            made.append((slug, name, how))
        known.add(comp)
    return made


AUTO = load_requests()


def units(glyph):
    """Block glyph -> 24 px grid pixels (each block = 2x2), centred exactly."""
    blocks = ICONS[glyph]()
    xs = [x for x, _ in blocks]
    ys = [y for _, y in blocks]
    w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
    ox, oy = 12 - w, 12 - h        # (24 - 2w) / 2
    out = set()
    for (x, y) in blocks:
        bx, by = ox + 2 * (x - min(xs)), oy + 2 * (y - min(ys))
        out |= {(bx, by), (bx + 1, by), (bx, by + 1), (bx + 1, by + 1)}
    return out


def background():
    img = Image.new("RGB", (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)
    for p in (16, SIZE - 17):     # cell lines like the reference grid
        d.line([(p, 0), (p, SIZE)], fill=GRID)
        d.line([(0, p), (SIZE, p)], fill=GRID)
    return img


def draw_glyph(img, pixels, color, px=U, off=OFF):
    d = ImageDraw.Draw(img)
    for (x, y) in pixels:
        x0, y0 = off + x * px, off + y * px
        d.rectangle([x0, y0, x0 + px - 1, y0 + px - 1], fill=color)
    return img


def icon(glyph, color):
    return draw_glyph(background(), units(glyph), COLORS[color])


def keyline_sheet(names, path):
    """Every icon big on its 24 px grid; light lines = 2 px blocks, box = 22 px live area."""
    P, M, cols = 10, 20, 6
    cell = 24 * P + M
    rows = (len(names) + cols - 1) // cols
    img = Image.new("RGB", (cols * cell + M, rows * cell + M), (0, 0, 0))
    d = ImageDraw.Draw(img)
    for k, n in enumerate(names):
        ox, oy = M + (k % cols) * cell, M + (k // cols) * cell
        d.rectangle([ox, oy, ox + 24 * P - 1, oy + 24 * P - 1], fill=(10, 10, 10))
        for i in range(25):
            c = (34, 34, 34) if i % 2 == 1 else (20, 20, 20)
            d.line([(ox + i * P, oy), (ox + i * P, oy + 24 * P)], fill=c)
            d.line([(ox, oy + i * P), (ox + 24 * P, oy + i * P)], fill=c)
        d.rectangle([ox + P, oy + P, ox + 23 * P - 1, oy + 23 * P - 1], outline=(40, 70, 110))
        glyph, color, _ = APPS[n]
        for (x, y) in units(glyph):
            d.rectangle([ox + x * P + 1, oy + y * P + 1, ox + x * P + P - 1, oy + y * P + P - 1],
                        fill=COLORS[color])
    img.save(path)


def compare_sheet(names, path):
    """Reference sheet on the left, our icons at the same scale on the right."""
    src = os.path.join(os.path.expanduser("~"), "Downloads", "raw", "Pixel Icons #001.jpg")
    if not os.path.exists(src):           # reference image is not part of the repo
        return
    ref = Image.open(src).convert("RGB")
    ref = ref.crop((110, 110, 626, 626))           # the 3x3 icon area
    scale = 172 / 72                               # reference: 72 px per 24 px cell + gaps
    cell = 172
    mine = Image.new("RGB", (516, 516), (0, 0, 0))
    for k, n in enumerate(names[:9]):
        glyph, color, _ = APPS[n]
        t = Image.new("RGB", (24 * 3, 24 * 3), (0, 0, 0))
        draw_glyph(t, units(glyph), COLORS[color], 3, 0)
        mine.paste(t, (50 + (k % 3) * cell, 50 + (k // 3) * cell))
    out = Image.new("RGB", (516 * 2 + 20, 516), (0, 0, 0))
    out.paste(ref, (0, 0))
    out.paste(mine, (536, 0))
    out = out.resize((out.width * 2, out.height * 2), Image.NEAREST)
    out.save(path)


def auto_sheet(path):
    """Math-made icons with the app name and the rule that made them."""
    if not AUTO:
        return
    cols, cell, lab = 4, SIZE + 24, 40
    rows = (len(AUTO) + cols - 1) // cols
    img = Image.new("RGB", (cols * cell + 24, rows * (cell + lab) + 24), (0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, (slug, name, how) in enumerate(AUTO):
        glyph, color, _ = APPS[slug]
        x, y = 24 + (i % cols) * cell, 24 + (i // cols) * (cell + lab)
        img.paste(icon(glyph, color), (x, y))
        d.text((x, y + SIZE + 4), name.upper(), fill=(115, 115, 117))
        d.text((x, y + SIZE + 18), how, fill=(70, 70, 70))
    img.save(path)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    nodpi = os.path.join(RES, "drawable-nodpi")
    os.makedirs(nodpi, exist_ok=True)
    for f in os.listdir(nodpi):            # drop icons that were renamed/removed
        if f.endswith(".png"):
            os.remove(os.path.join(nodpi, f))

    for name, (glyph, color, _) in APPS.items():
        icon(glyph, color).save(os.path.join(nodpi, f"{name}.png"))


    # back plate for apps that have no icon yet (launcher shrinks their icon onto it)
    background().save(os.path.join(nodpi, "iconback.png"))

    # launcher icon of the pack itself
    for dens, s in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
        d = os.path.join(RES, f"mipmap-{dens}")
        os.makedirs(d, exist_ok=True)
        icon("pack", "o").resize((s, s), Image.NEAREST).save(os.path.join(d, "ic_launcher.png"))

    # appfilter.xml
    items = []
    for name, (_, _, comps) in APPS.items():
        for c in comps:
            items.append(f'    <item component="ComponentInfo{{{c}}}" drawable="{name}" />')
    appfilter = (
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        '    <iconback img1="iconback" />\n'
        '    <scale factor="0.62" />\n\n'
        + "\n".join(items) + "\n</resources>\n"
    )
    write(os.path.join(RES, "xml", "appfilter.xml"), appfilter)
    write(os.path.join(APP, "assets", "appfilter.xml"), appfilter)

    # drawable.xml (icon picker in Nova / Lawnchair etc.)
    drawable = (
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <version>1</version>\n'
        '    <category title="All" />\n'
        + "\n".join(f'    <item drawable="{n}" />' for n in APPS)
        + "\n</resources>\n"
    )
    write(os.path.join(RES, "xml", "drawable.xml"), drawable)
    write(os.path.join(APP, "assets", "drawable.xml"), drawable)

    # string-array used by some launchers and by our preview screen
    arr = "\n".join(f"        <item>{n}</item>" for n in APPS)
    write(os.path.join(RES, "values", "iconpack.xml"),
          '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
          f'    <string-array name="icon_pack">\n{arr}\n    </string-array>\n</resources>\n')

    # preview sheet
    names = list(APPS)
    cols = 6
    rows = (len(names) + cols - 1) // cols
    cell = SIZE + 24
    sheet = Image.new("RGB", (cols * cell + 24, rows * cell + 24), (0, 0, 0))
    for i, n in enumerate(names):
        glyph, color, _ = APPS[n]
        sheet.paste(icon(glyph, color), (24 + (i % cols) * cell, 24 + (i // cols) * cell))
    sheet.save(os.path.join(ROOT, "preview.png"))
    keyline_sheet(names, os.path.join(ROOT, "keylines.png"))
    compare_sheet(names, os.path.join(ROOT, "compare.png"))
    auto_sheet(os.path.join(ROOT, "auto_icons.png"))
    for slug, name, how in AUTO:
        print(f"  auto  {name:22s} {how}")
    print(f"{len(names)} icons, {len(items)} app mappings written")


if __name__ == "__main__":
    main()
