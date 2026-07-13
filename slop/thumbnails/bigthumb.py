#!/usr/bin/env python3
# Builds bigthumb.jpg: a JPEG whose *embedded Exif thumbnail is larger than the
# main image* (thumb 1100x825, main 1024x768). Nothing forbids this -- the Exif
# thumbnail is just a JPEG in APP1 IFD1, capped only by the ~64 KB APP1 segment.
#
# It's a probe for how macOS chooses a thumbnail source: with an oversized thumb,
# ImageIO's CGImageSourceCreateThumbnailAtIndex keeps returning the (down-scaled)
# embedded thumb at every MaxPixelSize, and QLThumbnailGenerator (Finder) serves
# it at every icon size, capped at the main image's 1024x768 resolution -- i.e.
# the main image is never decoded. See README.md, "Oversized thumbnails".
#
# Run with:
#     uv run --with pillow python bigthumb.py
#
# The thumb is filled with a flat colour + label and encoded at low quality so
# the whole 1100x825 JPEG still fits in the 64 KB APP1 segment.

import io, os, struct
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bigthumb.jpg")

def load_font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

def label_image(w, h, bg, fg, text):
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    best = 6
    for s in range(6, 400):
        bb = d.multiline_textbbox((0, 0), text, font=load_font(s), align="center")
        if bb[2] - bb[0] > w * 0.88 or bb[3] - bb[1] > h * 0.85:
            break
        best = s
    f = load_font(best)
    bb = d.multiline_textbbox((0, 0), text, font=f, align="center")
    d.rectangle([0, 0, w - 1, h - 1], outline=fg, width=max(1, h // 40))
    d.multiline_text(((w - (bb[2] - bb[0])) / 2 - bb[0],
                      (h - (bb[3] - bb[1])) / 2 - bb[1]),
                     text, font=f, fill=fg, align="center")
    return im

def jpeg(im, q):
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q)
    return b.getvalue()

def strip_appn(j):
    p = 2
    while j[p:p + 1] == b"\xff" and 0xE0 <= j[p + 1] <= 0xEF:
        p += 2 + struct.unpack(">H", j[p + 2:p + 4])[0]
    return b"\xff\xd8" + j[p:]

def build_exif(thumb):
    def a(s):
        b = s.encode() + b"\x00"
        return b + (b"\x00" if len(b) & 1 else b"")
    RAT = struct.pack(">II", 72, 1)
    desc, mk, md = a("bigthumb: Exif thumb larger than main"), a("slop"), a("bigthumb")
    e = lambda t, ty, c, v: struct.pack(">HHI", t, ty, c) + v
    n0 = 8
    ex0 = 8 + (2 + 12 * n0 + 4)
    od = ex0; omk = od + len(desc); omd = omk + len(mk)
    ox0 = omd + len(md); oy0 = ox0 + 8; ifd1 = oy0 + 8
    n1 = 6
    ox1 = ifd1 + (2 + 12 * n1 + 4); oy1 = ox1 + 8; toff = oy1 + 8
    i0 = struct.pack(">H", n0)
    i0 += e(0x010E, 2, len("bigthumb: Exif thumb larger than main") + 1, struct.pack(">I", od))
    i0 += e(0x010F, 2, len("slop") + 1, struct.pack(">I", omk))
    i0 += e(0x0110, 2, len("bigthumb") + 1, struct.pack(">I", omd))
    i0 += e(0x0112, 3, 1, struct.pack(">HH", 1, 0))
    i0 += e(0x011A, 5, 1, struct.pack(">I", ox0))
    i0 += e(0x011B, 5, 1, struct.pack(">I", oy0))
    i0 += e(0x0128, 3, 1, struct.pack(">HH", 2, 0))
    i0 += e(0x0213, 3, 1, struct.pack(">HH", 1, 0))
    i0 += struct.pack(">I", ifd1)
    i1 = struct.pack(">H", n1)
    i1 += e(0x0103, 3, 1, struct.pack(">HH", 6, 0))
    i1 += e(0x011A, 5, 1, struct.pack(">I", ox1))
    i1 += e(0x011B, 5, 1, struct.pack(">I", oy1))
    i1 += e(0x0128, 3, 1, struct.pack(">HH", 2, 0))
    i1 += e(0x0201, 4, 1, struct.pack(">I", toff))
    i1 += e(0x0202, 4, 1, struct.pack(">I", len(thumb)))
    i1 += struct.pack(">I", 0)
    return b"Exif\x00\x00" + b"MM\x00\x2a" + struct.pack(">I", 8) + \
        i0 + desc + mk + md + RAT + RAT + i1 + RAT + RAT + thumb

# main 1024x768 (blue); Exif thumb 1100x825 (green) -- larger than the main image
main = label_image(1024, 768, (30, 30, 60), (255, 255, 255), "MAIN\n1024x768")
big = label_image(1100, 825, (30, 150, 60), (255, 255, 255), "BIG EXIF\n1100x825")
thumb = strip_appn(jpeg(big, 25))       # low quality so 1100x825 fits in APP1
assert len(thumb) < 64000, f"thumb too big for APP1: {len(thumb)}"

app0 = b"\xff\xe0" + struct.pack(">H", 16) + b"JFIF\x00\x01\x02\x01\x00\x48\x00\x48\x00\x00"
exif_payload = build_exif(thumb)
app1 = b"\xff\xe1" + struct.pack(">H", len(exif_payload) + 2) + exif_payload
main_frame = strip_appn(jpeg(main, 90))[2:]

with open(OUT, "wb") as f:
    f.write(b"\xff\xd8" + app0 + app1 + main_frame)
print("wrote", OUT, "-- Exif thumb", len(thumb), "bytes (1100x825), main 1024x768")
