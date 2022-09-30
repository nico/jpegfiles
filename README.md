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

### DC-008-Translation-2019-E.pdf

"CIPA DC-008-Translation-2019: Exchangeable image file format for digital
still cameras: Exif version 2.32"

The Exif standard.

Obtained from [here](https://www.cipa.jp/std/documents/download_e.html?DC-008-Translation-2019-E)

### DC-009-2020\_E.pdf

"CIPA DC-009-Translation-2010: Design rule for Camera File system"

Explains "DCIM" directory layout, "R98" InteropabilityIndex, 160x120 thumbnail
size, ...

Obtained from [here](https://www.cipa.jp/std/documents/download_e.html?DC-009-2010_E)

### DC-010-2020\_E.pdf

"Exif 2.32 metadata for XMP"

Maps exif fields to XMP tag names.

Obtained from [here](https://www.cipa.jp/std/documents/download_e.html?DC-010-2020_E)

### mwg\_guidance.pdf

"GUIDELINES FOR HANDLING IMAGE METADATA"

Overview of Exif, XMP, IPTC. Has recommendations which one to use if a file
contains several of them.

Used to be at http://www.metadataworkinggroup.org/pdf/mwg_guidance.pdf but
that server seems dead.

Obtained from [here](https://s3.amazonaws.com/software.tagthatphoto.com/docs/mwg_guidance.pdf)

### icc-1\_1998-09.pdf

"Specification ICC.1:1998-09"

Old version of ICC.1-2022-05.pdf below. Describes the old `textDescriptionType`
type, which the current version no longer describes. Files conforming to
ICC V2.4.0 and earlier still use this type.

Obtained from [here](https://www.color.org/icc-1_1998-09.pdf)

### ICC.1-2022-05.pdf

"Specification ICC.1:2022 (Profile version 4.4.0.0)"

Obtained from https://www.color.org/specification/ICC.1-2022-05.pdf

### ICC-Technote-ProfileEmbedding.pdf

"ICC Technical Note Embedding ICC profiles"

Obtained from https://www.color.org/technotes/ICC-Technote-ProfileEmbedding.pdf

### itu-t89.pdf

"INFORMATION TECHNOLOGY – DIGITAL COMPRESSION AND CODING OF CONTINUOUS-TONE
STILL IMAGES – REQUIREMENTS AND GUIDELINES"

The JPEG standard. Explains codec.

Obtained from https://www.w3.org/Graphics/JPEG/itu-t81.pdf

### jfif3.pdf

"JPEG File Interchange Format"

The JFIF APP0 container. For digital camera pictures, obsoleted by EXIF.

Obtained from https://www.w3.org/Graphics/JPEG/jfif3.pdf

### XMPSpecificationPart3.pdf

"XMP Specification Part 3: Storage in files"

Explains APP1 markers starting with "http://ns.adobe.com/xap/1.0/" and with
"http://ns.adobe.com/xmp/extension/".

Used to be at
http://www.adobe.com/content/dam/Adobe/en/devnet/xmp/pdfs/XMPSpecificationPart3.pdf
but that 404s now.

Obtained from [here](https://github.com/adobe/xmp-docs/blob/master/XMPSpecifications/XMPSpecificationPart3.pdf)
