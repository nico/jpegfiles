Spec PDFs
---------

Various specs on data and metadata found in jpeg files.

## DC-007\_E.pdf

"CIPA DC-007-Translation-2009: Multi-Picture Format"

Explains APP2 "MPF" markers.

Used to be at http://www.cipa.jp/std/documents/e/DC-007_E.pdf

Obtained from [here](https://web.archive.org/web/20190713230858/http://www.cipa.jp/std/documents/e/DC-007_E.pdf)

## DC-008-Translation-2019-E.pdf

"CIPA DC-008-Translation-2019: Exchangeable image file format for digital
still cameras: Exif version 2.32"

The Exif standard.

Obtained from [here](https://www.cipa.jp/std/documents/download_e.html?DC-008-Translation-2019-E)

## DC-009-2020\_E.pdf

"CIPA DC-009-Translation-2010: Design rule for Camera File system"

Explains "DCIM" directory layout, "R98" InteropabilityIndex, 160x120 thumbnail
size, ...

Obtained from [here](https://www.cipa.jp/std/documents/download_e.html?DC-009-2010_E)

## DC-010-2020\_E.pdf

"Exif 2.32 metadata for XMP"

Maps exif fields to XMP tag names.

Obtained from [here](https://www.cipa.jp/std/documents/download_e.html?DC-010-2020_E)

## Dynamic-depth-v1.0.pdf

"Dynamic Depth"

Documents XMP use in Pixel phones, and how it bundles multiple files into
a single jpeg (cf "Media Data Encoding" -> "Concatenated File Container").
This does something similar to MPF, but differently.

Obtained from [here](https://developer.android.com/training/camera2/Dynamic-depth-v1.0.pdf)

## icc-1\_1998-09.pdf

"Specification ICC.1:1998-09"

Old version of ICC.1-2022-05.pdf below. Describes the old `textDescriptionType`
type, which the current version no longer describes. Files conforming to
ICC V2.4.0 and earlier still use this type.

Obtained from [here](https://www.color.org/icc-1_1998-09.pdf)

## ICC.1-2022-05.pdf

"Specification ICC.1:2022 (Profile version 4.4.0.0)"

Obtained from https://www.color.org/specification/ICC.1-2022-05.pdf

## ICC-Technote-ProfileEmbedding.pdf

"ICC Technical Note Embedding ICC profiles"

Obtained from https://www.color.org/technotes/ICC-Technote-ProfileEmbedding.pdf

## IIMV4.1.pdf

"IPTC - NAA Information Interchange Model Version 4"

Obtained from https://www.iptc.org/std/IIM/4.1/specification/IIMV4.1.pdf

## itu-t89.pdf

"INFORMATION TECHNOLOGY – DIGITAL COMPRESSION AND CODING OF CONTINUOUS-TONE
STILL IMAGES – REQUIREMENTS AND GUIDELINES"

The JPEG standard. Explains codec.

Obtained from https://www.w3.org/Graphics/JPEG/itu-t81.pdf

## jfif3.pdf

"JPEG File Interchange Format"

The JFIF APP0 container. For digital camera pictures, obsoleted by EXIF.

Obtained from https://www.w3.org/Graphics/JPEG/jfif3.pdf

## mwg\_guidance.pdf

"GUIDELINES FOR HANDLING IMAGE METADATA"

Overview of Exif, XMP, IPTC. Has recommendations which one to use if a file
contains several of them.

Used to be at http://www.metadataworkinggroup.org/pdf/mwg_guidance.pdf but
that server seems dead.

Obtained from [here](https://s3.amazonaws.com/software.tagthatphoto.com/docs/mwg_guidance.pdf)

## Photoshop API Guide.pdf

"Adobe Photoshop Application Programming Interface Guide"

PhotoshopFileFormats.htm below references "Appendix A" in this guide in a few
places.

Obtained from https://usermanual.wiki/Document/Photoshop20API20Guide.1445764450/view

## PhotoshopFileFormats.htm

"Adobe Photoshop File Formats Specification"

"Image Resources Section" describes the data stored in `APP13` /
'Photoshop 3.0' blocks, which is the container for IPTC data.

Obtained from https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/

## XMPSpecificationPart3.pdf

"XMP Specification Part 3: Storage in files"

Explains APP1 markers starting with "http://ns.adobe.com/xap/1.0/" and with
"http://ns.adobe.com/xmp/extension/".

Used to be at
http://www.adobe.com/content/dam/Adobe/en/devnet/xmp/pdfs/XMPSpecificationPart3.pdf
but that 404s now.

Obtained from [here](https://github.com/adobe/xmp-docs/blob/master/XMPSpecifications/XMPSpecificationPart3.pdf)
