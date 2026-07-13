Thumbnail places, and which macOS APIs read them
================================================

A JPEG can carry a thumbnail in several independent places. These synthetic files
put a *different, differently-sized, differently-coloured* image in each place, so
you can tell which software reads a thumbnail from where just by the size and
colour it shows.

The images
----------

| image                         | what it is |
|-------------------------------|------------|
| `thumbnail-places.jpg`        | all six thumbnail slots populated (see the slot table below) |
| `thumbnail-places-nojfxx.jpg` | same, but the JFXX APP0 segment omitted |
| `bigthumb.jpg`                | one where the Exif thumbnail (1100x825) is *larger* than the main image (1024x768) |

The slots
---------

| slot                            | format                 | size     | colour    |
|---------------------------------|------------------------|----------|-----------|
| JFIF  APP0 (uncompressed RGB)   | raw RGB                | 80x60    | red       |
| JFXX  APP0 extension            | jpeg                   | 100x75   | orange    |
| Exif  APP1 IFD1                 | jpeg                   | 160x120  | green     |
| XMP   APP1 `xmp:Thumbnails`     | base64 jpeg            | 200x150  | purple    |
| MPF   APP2 (appended image)     | jpeg (Large Thumbnail) | 640x480  | pink      |
| 8BIM  APP13 Photoshop `0x040C`  | jpeg                   | 128x96   | teal      |
| main image                      | jpeg                   | 1024x768 | dark blue |

The MPF part is a conformant CIPA DC-007 (2025) Baseline MP File: the primary is
the Dependent Parent (child = entry #2), the appended image is the Dependent
Child, its MP Type is Large Thumbnail Class 1 (VGA, 640x480, 4:3 matching the
source), and the Large Thumbnail carries no MPF APP2 of its own (§6.1.2.1).
`exiftool` reports it under `PreviewImage` (not `MPImage2`) because its type code
is Large-Thumbnail class, which ImageIO/exiftool remap to the preview slot.

Supporting scripts
------------------

The images above are generated (and probed) by these scripts:

| script                       | what it does |
|------------------------------|--------------|
| `thumbnail-places.py`        | builds a thumbnail-places image. Flags: `-o` (required), `--no-jfxx`, `--only <slots>` |
| `bigthumb.py`                | builds `bigthumb.jpg` |
| `imageio-thumbnail-probe.py` | probes `CGImageSourceCreateThumbnailAtIndex` (low-level ImageIO) |
| `finder-thumbnail-probe.py`  | probes `QLThumbnailGenerator` (what Finder's icon view uses) |

    uv run --with pillow python thumbnail-places.py -o thumbnail-places.jpg
    uv run --with pillow python thumbnail-places.py --no-jfxx -o thumbnail-places-nojfxx.jpg
    uv run --with pillow python bigthumb.py

    uv run --with pillow --with pyobjc-framework-Quartz \
            python imageio-thumbnail-probe.py
    uv run --with pillow --with pyobjc-framework-Quartz \
            --with pyobjc-framework-QuickLookThumbnailing python finder-thumbnail-probe.py

`--only` writes just a subset of slots (comma-separated from `jfif, jfxx, exif,
xmp, mpf, photoshop`; the main image is always written) for per-slot isolation
tests, e.g. `thumbnail-places.py --only exif,jfxx -o exif-jfxx.jpg`.

Both probes also take optional file arguments (default: the `thumbnail-places`
files), e.g. `imageio-thumbnail-probe.py bigthumb.jpg`.

Inspecting the slots with exiftool
----------------------------------

    exiftool -validate -warning -a FILE            # conformance check (-> "Validate: OK")
    exiftool -a -G1 -s FILE                        # all tags, grouped by IFD, short names
    exiftool -v3 FILE                              # raw hex dump of every segment / IFD
    exiftool -a -G1 -s -MPImageType -MPImageLength -MPImageStart FILE   # MPF index

Extract each slot's thumbnail to a file (`-b` = raw binary):

    exiftool -b -ThumbnailImage      FILE > exif.jpg   # Exif IFD1 (or -IFD1:ThumbnailImage)
    exiftool -b -JFXX:ThumbnailImage FILE > jfxx.jpg   # JFXX APP0
    exiftool -b -XMP:ThumbnailImage  FILE > xmp.jpg    # XMP xmp:Thumbnails
    exiftool -b -PhotoshopThumbnail  FILE > psd.jpg    # APP13 8BIM
    exiftool -b -PreviewImage        FILE > mpf.jpg    # MPF Large Thumbnail (see gotcha)
    exiftool -b -ThumbnailImage -w %f_thumb.jpg FILE   # batch: one output per input

Two gotchas, both of which these files trip over:

* The MPF Large Thumbnail comes out under `-PreviewImage`, **not** `-MPImage2`:
  exiftool remaps Large-Thumbnail-class MP images to the preview tag, so
  `-b -MPImage2` returns nothing here.
* The JFIF *uncompressed* thumbnail is not an extractable image tag. Read its
  size from `JFIF:ThumbnailWidth` / `JFIF:ThumbnailHeight`; there is no `-b` for it.

Findings (macOS, 2025)
----------------------

### 1. ImageIO only reads the Exif (IFD1) thumbnail

Of all six slots, ImageIO only ever sources a thumbnail from the Exif IFD1
thumbnail. JFIF, JFXX, XMP and Photoshop-APP13 thumbnails are never used (verified
by isolating each: adding JFIF/XMP/Photoshop leaves the Exif thumb in use; only
JFXX changes things, see #3).

*Reproduce: build isolated files with `thumbnail-places.py --only ...` (e.g.
`--only exif`, `--only exif,jfxx`, `--only exif,photoshop`) and probe each with
`imageio-thumbnail-probe.py <file>`. The Exif thumb keeps being returned until you
add `jfxx`, which is what #3 is about.*

### 2. `CGImageSourceCreateThumbnailAtIndex` behaviour

* It returns the embedded Exif thumb only when `kCGImageSourceThumbnailMaxPixelSize`
  is set. With no max size you always get the full-resolution image back, even
  with the `FromImage...` flags. (The classic "why is my thumbnail 160x120".)
* `MaxPixelSize` is a downscale cap, never a target. For the 160x120 thumb:
  `max < 160` returns it scaled down; `max >= 160` returns it at native 160x120,
  never upscaled. No max value (even 2048) makes it decode the primary instead.
* To get the primary at a bounded size, pass `kCGImageSourceCreateThumbnailFromImageAlways`.
* So it is *not* just a `scale_denom` wrapper: there is a separate embedded-thumb
  path in front of the reduced-resolution decode path (the decoder is AppleJPEG).

*Reproduce: `imageio-thumbnail-probe.py`.*

### 3. The JFXX quirk

A JFXX APP0 extension segment breaks ImageIO's embedded-thumbnail path. With JFXX
present, `CGImageSourceCreateThumbnailAtIndex` never returns the Exif thumb (it
returns None for a plain JPEG, or a reduced-res decode of the primary for an MPO).
That is the only difference between `thumbnail-places.jpg` (with JFXX, always
decodes the 1024x768 primary) and `thumbnail-places-nojfxx.jpg` (no JFXX, returns
the 160x120 Exif thumb). Only JFXX does this.

*Reproduce: `imageio-thumbnail-probe.py` (it runs both files side by side).*

### 4. Finder's icon view picks the source by icon size

`QLThumbnailGenerator` (the API Finder's icon view uses) chooses:

    requested icon <= thumb's own resolution (160 here)  -> embedded Exif thumb
    requested icon  > thumb's own resolution              -> full decode of primary

So on `thumbnail-places-nojfxx.jpg`, small Finder icons show the green EXIF thumb
and large icons show the blue MAIN image; the with-JFXX file shows MAIN at every
size (#3 suppresses the fast path). This matches dragging the Finder icon-size
slider. Measured switch: 160 -> EXIF, 192 -> MAIN.

*Reproduce: `finder-thumbnail-probe.py`.*

### 5. `qlmanage -t` is not what Finder uses

`qlmanage -t -s N` always full-renders the primary regardless of `N`, so it never
shows the embedded thumb and is a poor proxy for Finder. Per representation type
(size 64, `-nojfxx` file): `icon` full-renders (MAIN), while `lowQualityThumbnail`
and `thumbnail` use the embedded Exif thumb. (`qlmanage`'s exact call wasn't
instrumented; the legacy `QLThumbnailImageCreate` binding is absent here and
`qlmanage` is closed source, but its output is aspect-preserved MAIN at all sizes,
i.e. a full render, not the embedded thumb.)

*Reproduce: `finder-thumbnail-probe.py` for the QL side, `qlmanage -t -s 64 -o
<dir> thumbnail-places-nojfxx.jpg` for the qlmanage side (the per-representation
sweep was a throwaway script).*

### 6. How Finder uses the thumb: one decode, not two

ImageIO's thumbnail API always hands back the capped embedded thumb and never
promotes to the primary, so the "is the thumb big enough?" decision lives in
QLThumbnailGenerator. Effectively it asks ImageIO for the embedded thumb capped at
`min(requested, main_size)`, then:

* thumb big enough for the request  -> serve the thumb, decoding only that image;
* thumb too small                   -> decode the primary instead.

There is no wasteful double *full* decode. When it escalates, the thumb work it
already did is trivial (a 160x120 decode, about 128 us, versus ~357 us for a
`FromImageAlways` full decode of even this tiny 1024x768 primary; the ratio grows
enormously for a real multi-megapixel photo). `CGImageSourceCopyPropertiesAtIndex`
exposes only the *main* image's dimensions, not the thumb's, so the size check
comes from the thumbnail request itself.

*Reproduce: chiefly reasoning, backed by #7 (`bigthumb.py`); the decode timings
came from a throwaway timing loop over `CGImageSourceCreateThumbnailAtIndex`.*

### 7. Oversized thumbnails (`bigthumb.jpg`)

Nothing requires the Exif thumb to be smaller than the main image. `bigthumb.jpg`
has a 1100x825 Exif thumb and a 1024x768 main. Result:

* ImageIO returns the (down-scaled) oversized thumb at every `MaxPixelSize`, up to
  its native 1100x825, never consulting the main image:

      max=64   -> 64x48    (thumb)      max=1024 -> 1024x768  (thumb)
      max=256  -> 256x192  (thumb)      max=1100 -> 1100x825  (thumb)
      max=900  -> 900x675  (thumb)      max=2048 -> 1100x825  (thumb, capped)

* Finder/QL serves the thumb at every icon size and never decodes the main,
  clamped to the main image's 1024x768 (a thumbnail never exceeds the full image):

      size=64   -> 64x48    (thumb)     size=1024 -> 1024x768 (thumb)
      size=512  -> 512x384  (thumb)     size=1300 -> 1024x768 (thumb)
      size=800  -> 800x600  (thumb)     size=2048 -> 1024x768 (thumb)

This confirms #6: the source is picked by comparing the request to the thumb's own
size, and only one image is decoded.

*Reproduce: build with `bigthumb.py`, then point the probes at it —
`imageio-thumbnail-probe.py bigthumb.jpg` and `finder-thumbnail-probe.py
bigthumb.jpg` (both accept a file argument). The tables above use a few extra
`MaxPixelSize`/size values beyond the probes' defaults.*

Aside: iPhoto
-------------

iPhoto's fast browsing of huge libraries was mostly its own on-disk thumbnail
cache inside the library package (pre-rendered `thumb`/`mini` sizes), not live
extraction while scrolling. The embedded-Exif-thumb fast path is what made
*generating* that cache cheap at import time:
`CGImageSourceCreateThumbnailAtIndex` with `FromImageIfAbsent` + `MaxPixelSize` is
exactly "embedded thumb if present, else a reduced-resolution (`scale_denom`-style)
decode". Timeline caveat: ImageIO shipped in Mac OS X 10.4 (2005); earlier iPhoto
predates it and used QuickTime importers, so only later iPhoto could use these
CGImageSource APIs. (iPhoto internals aren't publicly documented; this is informed
inference from the library layout and macOS imaging history.)

Caveats
-------

All of the above is from one macOS/ImageIO build (2025). QuickLook caches
thumbnails aggressively; the probes write to fresh paths / unique temp names to
force regeneration. Preview was not scripted: its main canvas decodes the full
image, but whether its sidebar thumbnails use the embedded-thumb path like Finder
is untested.
