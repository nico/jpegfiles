jpegfiles
=========

Various jpeg test images, and spec PDFs

Images
------

### GOPRO0027.JPG

Off a GoPro HERO10 Black, unmodified.

Has APP1 Exif, no APP0 JFIF.
Has an R98 Interopability IFD, and a 160x120 Exif jpeg thumbnail (the max size
allowed per R98).
Has an APP2 MPF IFD pointing at a 960x720 thumbnail.
The main image is 5568x4176.

Spec PDFs
---------

### DC-007\_E.pdf

"CIPA DC-007-Translation-2009: Multi-Picture Format"

Explains APP2 "MPF" markers.

Used to be at http://www.cipa.jp/std/documents/e/DC-007_E.pdf

Obtained from [here](https://web.archive.org/web/20190713230858/http://www.cipa.jp/std/documents/e/DC-007_E.pdf)

### DC-009-2020\_E.pdf

"CIPA DC-009-Translation-2010: Design rule for Camera File system"

Explains "DCIM" directory layout, "R98" InteropabilityIndex, 160x120 thumbnail
size, ...

Obtained from [here](https://www.cipa.jp/std/documents/download_e.html?DC-009-2010_E)

### DC-010-2020\_E.pdf

"Exif 2.32 metadata for XMP"

Maps exif fields to XMP tag names.

Obtained from [here](https://www.cipa.jp/std/documents/download_e.html?DC-010-2020_E)

### itu-t89.pdf

"INFORMATION TECHNOLOGY – DIGITAL COMPRESSION AND CODING OF CONTINUOUS-TONE
STILL IMAGES – REQUIREMENTS AND GUIDELINES"

The JPEG standard. Explains codec.

Obtained from https://www.w3.org/Graphics/JPEG/itu-t81.pdf

### XMPSpecificationPart3.pdf

"XMP Specification Part 3: Storage in files"

Explains APP1 markers starting with "http://ns.adobe.com/xap/1.0/" and with
"http://ns.adobe.com/xmp/extension/".

Used to be at
http://www.adobe.com/content/dam/Adobe/en/devnet/xmp/pdfs/XMPSpecificationPart3.pdf
but that 404s now.

Obtained from [here](https://github.com/adobe/xmp-docs/blob/master/XMPSpecifications/XMPSpecificationPart3.pdf)
