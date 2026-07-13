#!/usr/bin/env python3
# Builds thumbnail-places.jpg: a JPEG that stores a different labelled image in
# each of the six standardised thumbnail locations (JFIF, JFXX, Exif IFD1, XMP,
# MPF, Photoshop 8BIM), each at a distinct size, to test which viewers read from
# where. MPF part follows CIPA DC-007 (2025) §A.6.
#
# Run with (-o is required):
#     uv run --with pillow python thumbnail-places.py -o thumbnail-places.jpg
#     uv run --with pillow python thumbnail-places.py --no-jfxx -o thumbnail-places-nojfxx.jpg
#     uv run --with pillow python thumbnail-places.py --only exif,jfxx -o exif-jfxx.jpg
import io, struct, base64, os, argparse
from PIL import Image, ImageDraw, ImageFont

ALL_SLOTS = ["jfif", "jfxx", "exif", "xmp", "mpf", "photoshop"]
_ALIASES = {"psd": "photoshop", "8bim": "photoshop"}

_parser = argparse.ArgumentParser(
    description="Build a JPEG with a differently-labelled thumbnail in each slot.")
_parser.add_argument(
    "-o", "--output", required=True, help="output JPEG path")
_parser.add_argument(
    "--no-jfxx", action="store_true",
    help="omit the JFXX APP0 thumbnail (Apple ImageIO fails to read any thumbnail "
         "when a JFXX segment is present). Shorthand for --only of everything but jfxx.")
_parser.add_argument(
    "--only", metavar="SLOTS",
    help="comma-separated subset of thumbnail slots to write, for per-slot tests "
         "(choices: " + ", ".join(ALL_SLOTS) + "; 'psd'=photoshop). Default: all. "
         "The main image is always written.")
_args = _parser.parse_args()

if _args.only is not None:
    SLOTS = []
    for name in _args.only.replace(",", " ").split():
        n = _ALIASES.get(name.lower(), name.lower())
        if n not in ALL_SLOTS:
            _parser.error(f"unknown slot {name!r}; choose from {', '.join(ALL_SLOTS)}")
        if n not in SLOTS:
            SLOTS.append(n)
    if not SLOTS:
        _parser.error("--only needs at least one slot")
else:
    SLOTS = [s for s in ALL_SLOTS if not (_args.no_jfxx and s == "jfxx")]

OUT = _args.output

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SFNS.ttf",
]
def load_font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def label_image(w, h, bg, fg, lines):
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)
    # find largest font that fits ~85% of the box
    text = "\n".join(lines)
    best = 6
    for size in range(6, 400):
        f = load_font(size)
        bb = d.multiline_textbbox((0, 0), text, font=f, align="center", spacing=2)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if tw > w * 0.88 or th > h * 0.85:
            break
        best = size
    f = load_font(best)
    bb = d.multiline_textbbox((0, 0), text, font=f, align="center", spacing=2)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x = (w - tw) / 2 - bb[0]
    y = (h - th) / 2 - bb[1]
    # border so the frame edge is visible in viewers
    d.rectangle([0, 0, w - 1, h - 1], outline=fg, width=max(1, h // 40))
    d.multiline_text((x, y), text, font=f, fill=fg, align="center", spacing=2)
    return img

def jpeg(img, q=90):
    b = io.BytesIO()
    img.save(b, "JPEG", quality=q)
    return b.getvalue()

def strip_appn(j):
    # keep SOI, drop all leading APPn (FFE0..FFEF) segments
    assert j[:2] == b"\xff\xd8"
    pos = 2
    while j[pos:pos + 1] == b"\xff" and 0xE0 <= j[pos + 1] <= 0xEF:
        seglen = struct.unpack(">H", j[pos + 2:pos + 4])[0]
        pos += 2 + seglen
    return b"\xff\xd8" + j[pos:]

# ---- slot images -----------------------------------------------------------
def img_for(tag, w, h, bg, fg):
    return label_image(w, h, bg, fg, [tag, f"{w}x{h}"])

main_img   = img_for("MAIN",      1024, 768, (30, 30, 60),  (255, 255, 255))
jfif_img   = img_for("JFIF",      80,  60,  (200, 40, 40),  (255, 255, 255))
jfxx_img   = img_for("JFXX",      100, 75,  (230, 120, 20), (0, 0, 0))
exif_img   = img_for("EXIF-IFD1", 160, 120, (30, 150, 60),  (255, 255, 255))
xmp_img    = img_for("XMP",       200, 150, (120, 40, 160), (255, 255, 255))
psd_img    = img_for("PHOTOSHOP", 128, 96,  (20, 150, 160), (0, 0, 0))
mpf_img    = img_for("MPF",       640, 480, (200, 20, 120), (255, 255, 255))

# ---- encoded thumbnails ----------------------------------------------------
jfxx_jpeg = strip_appn(jpeg(jfxx_img))     # JFIF spec: embedded JPEG w/o APP0
exif_jpeg = strip_appn(jpeg(exif_img))
xmp_jpeg  = strip_appn(jpeg(xmp_img, q=80))
psd_jpeg  = strip_appn(jpeg(psd_img))
mpf_jpeg  = jpeg(mpf_img)                  # standalone, keep whole
main_jpeg = jpeg(main_img)

# =============================================================================
# Segment builders
# =============================================================================
def seg(marker, payload):
    return marker + struct.pack(">H", len(payload) + 2) + payload

# --- (1) APP0 JFIF with uncompressed RGB thumbnail --------------------------
xt, yt = jfif_img.size
jfif_payload = (b"JFIF\x00" + b"\x01\x02" + b"\x01" +
                struct.pack(">H", 72) + struct.pack(">H", 72) +
                struct.pack("B", xt) + struct.pack("B", yt) +
                jfif_img.tobytes())        # row-major RGB
app0_jfif = seg(b"\xff\xe0", jfif_payload)

# --- (2) APP0 JFXX with JPEG thumbnail (extension code 0x10) -----------------
app0_jfxx = seg(b"\xff\xe0", b"JFXX\x00" + b"\x10" + jfxx_jpeg)

# --- (3) APP1 Exif with IFD0 + IFD1(thumbnail) ------------------------------
def build_exif(thumb):
    def ascii_val(s):
        b = s.encode() + b"\x00"
        if len(b) & 1:           # word-align external ASCII offsets
            b += b"\x00"
        return b
    RAT = struct.pack(">II", 72, 1)                        # 72/1 resolution
    desc = ascii_val("Thumbnail-location test / MAIN")
    make = ascii_val("ThumbTest")
    model = ascii_val("SevenSlots")
    header = b"MM\x00\x2a" + struct.pack(">I", 8)
    def e(tag, typ, count, val):  # val already 4 bytes
        return struct.pack(">HHI", tag, typ, count) + val
    # --- IFD0 layout (offsets from TIFF start) ---
    n0 = 8
    ifd0_size = 2 + 12 * n0 + 4
    ifd0_extra_off = 8 + ifd0_size
    off_desc = ifd0_extra_off
    off_make = off_desc + len(desc)
    off_model = off_make + len(make)
    off_x0 = off_model + len(model)
    off_y0 = off_x0 + 8
    ifd1_off = off_y0 + 8
    # --- IFD1 layout ---
    n1 = 6
    ifd1_size = 2 + 12 * n1 + 4
    off_x1 = ifd1_off + ifd1_size
    off_y1 = off_x1 + 8
    thumb_off = off_y1 + 8
    # IFD0 (tags ascending)
    ifd0 = struct.pack(">H", n0)
    ifd0 += e(0x010E, 2, len("Thumbnail-location test / MAIN") + 1, struct.pack(">I", off_desc))
    ifd0 += e(0x010F, 2, len("ThumbTest") + 1, struct.pack(">I", off_make))
    ifd0 += e(0x0110, 2, len("SevenSlots") + 1, struct.pack(">I", off_model))
    ifd0 += e(0x0112, 3, 1, struct.pack(">HH", 1, 0))      # Orientation=1
    ifd0 += e(0x011A, 5, 1, struct.pack(">I", off_x0))     # XResolution
    ifd0 += e(0x011B, 5, 1, struct.pack(">I", off_y0))     # YResolution
    ifd0 += e(0x0128, 3, 1, struct.pack(">HH", 2, 0))      # ResolutionUnit=inch
    ifd0 += e(0x0213, 3, 1, struct.pack(">HH", 1, 0))      # YCbCrPositioning=centered
    ifd0 += struct.pack(">I", ifd1_off)                    # next IFD = IFD1
    ifd0_extra = desc + make + model + RAT + RAT
    # IFD1 (tags ascending)
    ifd1 = struct.pack(">H", n1)
    ifd1 += e(0x0103, 3, 1, struct.pack(">HH", 6, 0))      # Compression=JPEG
    ifd1 += e(0x011A, 5, 1, struct.pack(">I", off_x1))     # XResolution
    ifd1 += e(0x011B, 5, 1, struct.pack(">I", off_y1))     # YResolution
    ifd1 += e(0x0128, 3, 1, struct.pack(">HH", 2, 0))      # ResolutionUnit
    ifd1 += e(0x0201, 4, 1, struct.pack(">I", thumb_off))  # JPEGInterchangeFormat
    ifd1 += e(0x0202, 4, 1, struct.pack(">I", len(thumb))) # length
    ifd1 += struct.pack(">I", 0)                           # next IFD = 0
    ifd1_extra = RAT + RAT
    tiff = header + ifd0 + ifd0_extra + ifd1 + ifd1_extra + thumb
    return b"Exif\x00\x00" + tiff
app1_exif = seg(b"\xff\xe1", build_exif(exif_jpeg))

# --- (6) APP1 XMP with xmp:Thumbnails ---------------------------------------
def build_xmp(thumb, w, h):
    b64 = base64.b64encode(thumb).decode()
    packet = (
        '<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/">\n'
        ' <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '  <rdf:Description rdf:about=""\n'
        '    xmlns:xmp="http://ns.adobe.com/xap/1.0/"\n'
        '    xmlns:xapGImg="http://ns.adobe.com/xap/g/img/">\n'
        '   <xmp:Thumbnails>\n    <rdf:Alt>\n'
        '     <rdf:li rdf:parseType="Resource">\n'
        f'      <xapGImg:format>JPEG</xapGImg:format>\n'
        f'      <xapGImg:width>{w}</xapGImg:width>\n'
        f'      <xapGImg:height>{h}</xapGImg:height>\n'
        f'      <xapGImg:image>{b64}</xapGImg:image>\n'
        '     </rdf:li>\n    </rdf:Alt>\n   </xmp:Thumbnails>\n'
        '  </rdf:Description>\n </rdf:RDF>\n</x:xmpmeta>\n'
        '<?xpacket end="w"?>')
    return b"http://ns.adobe.com/xap/1.0/\x00" + packet.encode("utf-8")
app1_xmp = seg(b"\xff\xe1", build_xmp(xmp_jpeg, *xmp_img.size))

# --- (7) APP13 Photoshop 8BIM thumbnail (resource 0x040C) -------------------
def build_psd(thumb, w, h):
    bits, planes = 24, 1
    widthbytes = (w * bits + 31) // 32 * 4
    total = widthbytes * h * planes
    res = (struct.pack(">I", 1) +          # format = kJpegRGB
           struct.pack(">I", w) + struct.pack(">I", h) +
           struct.pack(">I", widthbytes) +
           struct.pack(">I", total) +
           struct.pack(">I", len(thumb)) +
           struct.pack(">H", bits) + struct.pack(">H", planes) +
           thumb)
    if len(res) & 1:
        res += b"\x00"
    block = b"8BIM" + struct.pack(">H", 0x040C) + b"\x00\x00" + struct.pack(">I", len(res)) + res
    return b"Photoshop 3.0\x00" + block
app13_psd = seg(b"\xff\xed", build_psd(psd_jpeg, *psd_img.size))

# --- (5) APP2 MPF (index for 2 images) --------------------------------------
def build_mpf(primary_size, second_size, second_rel_offset):
    # MP header (offsets from here, the 'MM')
    hdr = b"MM\x00\x2a" + struct.pack(">I", 8)
    count = 3
    def e(tag, typ, cnt, val):
        return struct.pack(">HHI", tag, typ, cnt) + val
    ifd = struct.pack(">H", count)
    ifd += e(0xB000, 7, 4, b"0100")                        # MPFVersion
    ifd += e(0xB001, 4, 1, struct.pack(">I", 2))           # NumberOfImages
    mpentry_off = 8 + (2 + 12 * count + 4)                 # after IFD + nextIFD
    ifd += e(0xB002, 7, 16 * 2, struct.pack(">I", mpentry_off))
    ifd += struct.pack(">I", 0)                            # next IFD
    def entry(attr, size, off, dep1=0, dep2=0):
        return struct.pack(">IIIHH", attr, size, off, dep1, dep2)
    # Per CIPA DC-007 §A.6 (Fig 15): Baseline primary is Dependent Parent of the
    # Large Thumbnail (child entry #2); thumbnail is the Dependent Child.
    #   attr bits: 31=Parent 30=Child 29=Representative 26-24=DataFormat 23-0=MPTypeCode
    mpentries = (entry(0x80030000, primary_size, 0, dep1=2) +          # Parent + Baseline Primary
                 entry(0x40010001, second_size, second_rel_offset))    # Child  + Large Thumb (VGA)
    return b"MPF\x00" + hdr + ifd + mpentries

# NB: CIPA DC-007 §6.1.2.1 — a Large Thumbnail shall NOT contain the MPF APP2.
# So the appended image stays a plain standalone JPEG; only the primary carries MPF.

# =============================================================================
# Assemble the file from the selected slots.
# Marker order: SOI, APP0 JFIF, APP0 JFXX, APP1 Exif, APP1 XMP, APP2 MPF,
# APP13 Photoshop, frame data, EOI, then the appended MPF image (if any).
# =============================================================================
SOI = b"\xff\xd8"
main_frame = strip_appn(main_jpeg)[2:]     # DQT..EOI (drop SOI, we add our own)

# A JFIF file needs an APP0; use the one carrying the thumbnail only if 'jfif' is
# selected, otherwise a plain APP0 with no thumbnail.
plain_app0 = (b"\xff\xe0" + struct.pack(">H", 16) +
              b"JFIF\x00\x01\x02\x01\x00\x48\x00\x48\x00\x00")

before_mpf = SOI + (app0_jfif if "jfif" in SLOTS else plain_app0)
if "jfxx" in SLOTS:
    before_mpf += app0_jfxx
if "exif" in SLOTS:
    before_mpf += app1_exif
if "xmp" in SLOTS:
    before_mpf += app1_xmp
after_mpf = (app13_psd if "photoshop" in SLOTS else b"") + main_frame

if "mpf" in SLOTS:
    mp_endian_abs = len(before_mpf) + 2 + 2 + 4            # marker+len+"MPF\0"
    app2_mpf = seg(b"\xff\xe2", build_mpf(0, 0, 0))        # placeholder (fixed size)
    primary = before_mpf + app2_mpf + after_mpf
    second_rel = len(primary) - mp_endian_abs
    app2_mpf = seg(b"\xff\xe2", build_mpf(len(primary), len(mpf_jpeg), second_rel))
    primary = before_mpf + app2_mpf + after_mpf           # same length, real offsets
    final = primary + mpf_jpeg
else:
    final = before_mpf + after_mpf

with open(OUT, "wb") as f:
    f.write(final)

print("wrote", OUT, "--", len(final), "bytes; slots:", ", ".join(SLOTS))
