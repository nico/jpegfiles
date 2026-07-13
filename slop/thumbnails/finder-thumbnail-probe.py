#!/usr/bin/env python3
# Probe what Finder's icon view / QuickLook actually shows for a JPEG, using the
# real API that Finder's thumbnails go through: QLThumbnailGenerator. This is the
# companion to imageio-thumbnail-probe.py (which pokes the lower-level
# CGImageSourceCreateThumbnailAtIndex directly).
#
# Run with:
#     uv run --with pillow --with pyobjc-framework-Quartz \
#             --with pyobjc-framework-QuickLookThumbnailing python finder-thumbnail-probe.py
#
# ---------------------------------------------------------------------------
# Why this exists (and why `qlmanage -t` is NOT the right tool):
# ---------------------------------------------------------------------------
# `qlmanage -t -s N` always does a full-quality render of the primary image
# regardless of N, so it hides the behaviour below. Finder's icon view does not:
# it picks the thumbnail *source by icon size*.
#
# Findings (macOS, 2025), confirmed against Finder's icon-size slider:
#   * For icon sizes up to the embedded Exif thumbnail's own resolution (160x120
#     here, long edge 160), QuickLook serves the fast embedded Exif thumbnail.
#     For larger icons it decodes the full primary image for sharpness.
#   * That fast path is the same one CGImageSourceCreateThumbnailAtIndex uses, so
#     it inherits the JFXX quirk: if a JFXX APP0 segment is present ImageIO won't
#     return the embedded thumb, and Finder shows the full primary (MAIN) at ALL
#     sizes. Remove JFXX and small icons show the Exif thumb, large ones MAIN.
#
# Expected output (the switch happens between 160 and 192 -> the thumb's 160px):
#   size=160  with-JFXX: MAIN   no-JFXX: EXIF
#   size=192  with-JFXX: MAIN   no-JFXX: MAIN
#
# The two inputs differ only in the JFXX segment; build them with:
#   thumbnail-places.py
#   thumbnail-places.py --no-jfxx -o thumbnail-places-nojfxx.jpg
# ---------------------------------------------------------------------------

import io
import os
import sys
import time
import Quartz
import Foundation
import QuickLookThumbnailing as QL
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [("with-JFXX", os.path.join(HERE, "thumbnail-places.jpg")),
         ("no-JFXX",   os.path.join(HERE, "thumbnail-places-nojfxx.jpg"))]
SIZES = [32, 64, 128, 160, 192, 256, 384, 512]

# background colour of each slot's label image -> identifies the source slot
SLOTS = {
    "MAIN": (30, 30, 60), "JFIF": (200, 40, 40), "JFXX": (230, 120, 20),
    "EXIF": (30, 150, 60), "XMP": (120, 40, 160), "PHOTOSHOP": (20, 150, 160),
    "MPF": (200, 20, 120),
}

def nearest_slot(rgb):
    return min(SLOTS, key=lambda k: sum((a - b) ** 2 for a, b in zip(SLOTS[k], rgb)))

def cgimage_to_pil(cg):
    data = Foundation.NSMutableData.data()
    dst = Quartz.CGImageDestinationCreateWithData(data, "public.png", 1, None)
    Quartz.CGImageDestinationAddImage(dst, cg, None)
    Quartz.CGImageDestinationFinalize(dst)
    return Image.open(io.BytesIO(bytes(data)))

def corner_color(im):
    # sample a text-free patch (labels are centred; slot bg fills the corners)
    im = im.convert("RGB")
    w, h = im.size
    box = (int(w * 0.10), int(h * 0.12), int(w * 0.20), int(h * 0.28))
    return im.crop(box).resize((1, 1)).getpixel((0, 0))

def thumbnail_slot(gen, path, size):
    url = Foundation.NSURL.fileURLWithPath_(path)
    req = QL.QLThumbnailGenerationRequest.alloc().initWithFileAtURL_size_scale_representationTypes_(
        url, Foundation.NSMakeSize(size, size), 1.0,
        QL.QLThumbnailGenerationRequestRepresentationTypeThumbnail)
    box = {}
    def handler(rep, err):
        box["rep"] = rep
        box["done"] = True
    gen.generateBestRepresentationForRequest_completionHandler_(req, handler)
    # the generator runs on its own dispatch queue; just wait for the callback
    t0 = time.time()
    while not box.get("done") and time.time() - t0 < 8:
        time.sleep(0.02)
    if not box.get("done"):
        return "TIMEOUT"
    rep = box.get("rep")
    if rep is None:
        return "None"
    im = cgimage_to_pil(rep.CGImage())
    return f"{im.size[0]}x{im.size[1]} {nearest_slot(corner_color(im))}"

def main():
    # optional: pass file paths to probe (e.g. bigthumb.jpg); label = basename
    files = [(os.path.basename(p), p) for p in sys.argv[1:]] or FILES
    missing = [p for _, p in files if not os.path.exists(p)]
    if missing:
        print("missing inputs:", ", ".join(missing),
              "\nbuild them with thumbnail-places.py (and --no-jfxx)")
        return
    gen = QL.QLThumbnailGenerator.sharedGenerator()
    print("QLThumbnailGenerator (what Finder's icon view uses), representationType=thumbnail:")
    for size in SIZES:
        cells = [f"{label}: {thumbnail_slot(gen, path, size):14}" for label, path in files]
        print(f"  size={size:<4}  " + "  ".join(cells))

if __name__ == "__main__":
    main()
