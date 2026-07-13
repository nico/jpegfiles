#!/usr/bin/env python3
# Probe what Apple's ImageIO / CoreGraphics thumbnail API actually returns for a
# JPEG, using thumbnail-places.jpg (which stores a differently-sized, differently-
# coloured image in each thumbnail slot) so the *source* of the returned thumbnail
# can be identified by size and background colour.
#
# Run with:
#     uv run --with pillow --with pyobjc-framework-Quartz python imageio-thumbnail-probe.py
#
# ---------------------------------------------------------------------------
# Background: CGImageSourceCreateThumbnailAtIndex(src, index, options)
# ---------------------------------------------------------------------------
# This is the "load a low-res version of a JPEG" API. It is *both* of the things
# you might guess: it can hand back an embedded thumbnail, and it can synthesise
# one by decoding the full image at reduced resolution. The options dict decides:
#
#   kCGImageSourceCreateThumbnailFromImageIfAbsent : make one from the full image
#                                                    only if none is embedded
#   kCGImageSourceCreateThumbnailFromImageAlways   : always decode the full image,
#                                                    ignore any embedded thumbnail
#   kCGImageSourceThumbnailMaxPixelSize            : cap the long edge (px)
#   kCGImageSourceCreateThumbnailWithTransform     : apply the EXIF orientation
#
# When it does synthesise from the full image it uses a reduced-resolution DCT
# decode (the libjpeg scale_denom / 1-2-4-8 idea) and then scales — but via
# Apple's own decoder (AppleJPEG, HW-accelerated on some devices), not stock
# libjpeg. So "just a scale_denom wrapper" is not quite right: there's a separate
# embedded-thumbnail path in front of the reduced-res decode path.
#
# ---------------------------------------------------------------------------
# What this file's probing actually established (macOS, ImageIO 2025):
# ---------------------------------------------------------------------------
#  * Of the six thumbnail slots, ImageIO only ever sources from the *Exif IFD1*
#    thumbnail. JFIF-uncompressed, XMP and Photoshop-APP13 thumbnails are ignored
#    (the Exif thumb is still used when they are also present).
#  * It returns the embedded Exif thumbnail ONLY when kCGImageSourceThumbnailMaxPixelSize
#    is supplied. With no max-size hint you always get the full-resolution image
#    back — even with the "FromImage..." flags — so the classic "why is my
#    thumbnail 160x120" surprise only bites once you pass a max size.
#  * MaxPixelSize is a pure *downscale cap*, not a target. Given a 160x120 Exif
#    thumb: max<160 hands back the thumb scaled DOWN (max=64 -> 64x48); max>=160
#    hands back the thumb at its native 160x120 and NEVER upscales it. There is no
#    max value that makes ImageIO decode the primary instead — even max=2048 still
#    returns the 160x120 thumb. The only ways to get the primary are omitting
#    MaxPixelSize (full res) or kCGImageSourceCreateThumbnailFromImageAlways.
#  * Quirk: a *JFXX* APP0 extension segment breaks the embedded-thumbnail path —
#    ImageIO then returns None (plain JPEG) or falls back to a reduced-res decode
#    of the primary (MPO). This probe demonstrates it directly by running against
#    two files that differ only in the JFXX segment:
#      thumbnail-places.jpg        (with JFXX)  -> always decodes the 1024x768 primary
#      thumbnail-places-nojfxx.jpg (no JFXX)    -> returns the 160x120 Exif thumbnail
#    Build the second with:  thumbnail-places.py --no-jfxx -o thumbnail-places-nojfxx.jpg
# ---------------------------------------------------------------------------

import io
import os
import sys
import Quartz
import Foundation
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [os.path.join(HERE, "thumbnail-places.jpg"),
         os.path.join(HERE, "thumbnail-places-nojfxx.jpg")]

# background colour of each slot's label image -> lets us identify the source
SLOTS = {
    "MAIN":      (30, 30, 60),
    "JFIF":      (200, 40, 40),
    "JFXX":      (230, 120, 20),
    "EXIF-IFD1": (30, 150, 60),
    "XMP":       (120, 40, 160),
    "PHOTOSHOP": (20, 150, 160),
    "MPF":       (200, 20, 120),
}

def nearest_slot(rgb):
    return min(SLOTS, key=lambda k: sum((a - b) ** 2 for a, b in zip(SLOTS[k], rgb)))

def cgimage_to_png(img):
    data = Foundation.NSMutableData.data()
    dst = Quartz.CGImageDestinationCreateWithData(data, "public.png", 1, None)
    Quartz.CGImageDestinationAddImage(dst, img, None)
    Quartz.CGImageDestinationFinalize(dst)
    return bytes(data)

def probe(src, name, options):
    img = Quartz.CGImageSourceCreateThumbnailAtIndex(src, 0, options)
    if img is None:
        print(f"  {name:38}: None (no thumbnail returned)")
        return
    pil = Image.open(io.BytesIO(cgimage_to_png(img))).convert("RGB")
    avg = pil.resize((1, 1)).getpixel((0, 0))
    w, h = pil.size
    print(f"  {name:38}: {w}x{h:<5} avgRGB={avg!s:16} -> {nearest_slot(avg)}")

def probe_file(path):
    K = Quartz
    if not os.path.exists(path):
        print(f"{path}: (missing — build it with thumbnail-places.py)")
        return
    src = Quartz.CGImageSourceCreateWithURL(
        Foundation.NSURL.fileURLWithPath_(path), None)
    print(f"{path}: CGImageSourceGetCount = {Quartz.CGImageSourceGetCount(src)}")
    cases = [
        ("no flags, no max size", {}),
        ("no flags, MaxPixelSize=64",   {K.kCGImageSourceThumbnailMaxPixelSize: 64}),
        ("no flags, MaxPixelSize=256",  {K.kCGImageSourceThumbnailMaxPixelSize: 256}),
        ("no flags, MaxPixelSize=2048", {K.kCGImageSourceThumbnailMaxPixelSize: 2048}),
        ("FromImageIfAbsent, MaxPixelSize=256",
         {K.kCGImageSourceCreateThumbnailFromImageIfAbsent: True,
          K.kCGImageSourceThumbnailMaxPixelSize: 256}),
        ("FromImageAlways, MaxPixelSize=256",
         {K.kCGImageSourceCreateThumbnailFromImageAlways: True,
          K.kCGImageSourceThumbnailMaxPixelSize: 256}),
    ]
    for name, opts in cases:
        probe(src, name, opts)

def main():
    files = sys.argv[1:] or FILES        # optional: pass file paths to probe (e.g. bigthumb.jpg)
    for i, path in enumerate(files):
        if i:
            print()
        probe_file(path)

if __name__ == "__main__":
    main()
