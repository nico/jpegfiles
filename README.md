jpegfiles
=========

Various jpeg test images, and spec PDFs

Images
------

### 12-bit.jpg

Has 12 bits per channel.

Created a 16 bpc image in Acorn.app, saved it as (16-bit) tiff, then ran:

    sips -s format pbm -o 16-bit.ppm 16-bit.tiff

to convert it to (16-bit) ppm, then ran

    ./cjpeg -verbose -precision 12 -outfile 12-bit.jpg 16-bit.ppm

with a recent build of libjpeg-turbo (rev 6c61033349) to create the 12-bit
jpeg file. (I built libjpeg-turbo using just `cmake -GNinja .. ; ninja`.)

(The `Warning: unexpected GIF version number '@?` message it prints is benign.)

### 12-bit.jpg

Same as `12-bit.jpg` above, but also passed `-progressive` to `cjpeg`:

    ./cjpeg -verbose -precision 12 -progressive \
        -outfile 12-bit-progressive.jpg 16-bit.ppm

### 16-bit.tiff

See `12-bit.jpg` description above.

### check\_lut.jpeg

Has `A2B0`, `A2B1`, `A2B1` (of type `mft2`) in its color profile instead of the
much more common `rXYZ`, `gXYZ`, `bXYZ`, `rTRC`, `gTRC`, `bTRC`, `wtpt`.

Obtained from https://littlecms.com/blog/2020/09/09/browser-check/

### check\_full.jpeg

Has `A2B0`, `A2B1`, `A2B1` (of type `mft2`) as well as
`rXYZ`, `gXYZ`, `bXYZ`, `rTRC`, `gTRC`, `bTRC`, `wtpt` in its color profile.

Obtained from https://littlecms.com/blog/2020/09/09/browser-check/

### DJI\_406.JPG

Off a DJI Mini 2, unmodified.

* Has APP1 Exif, no APP0 JFIF.
* Has an R98 Interopability IFD, but a 256x192 Exif jpeg thumbnail
  (larger than allowed per R98 from what I understand).
* Has GPS IFD.
* Has an APP2 MPF IFD pointing at a 960x720 thumbnail.
* Has an XMP section.
* No colorspace information

### DSC03136.JPG

Off a Sony a7iv, unmodified, manually copied off the memory card.

* Has APP1 Exif, no APP0 JFIF.
* Has an R98 Interopability IFD, and a 160x120 Exif jpeg thumbnail
  (the max size allowed per R98).
* Has an APP2 MPF IFD pointing at a 1616x1080 thumbnail.
* The main image is 7008x4672.
* Has a mostly empty XMP section.
* No colorspace information (!)

### DSC03136-exported.jpg

Like DSC03136.JPG, but made by importing the raw file DSC03136.ARW into
Lightroom Classic and exporting it as jpeg.

It's interesting to compare to DSC03136.JPG. Some Exif tags get added
(ShutterSpeedValue, ApertureValue, ...), some removed (InteropabilityIFD,
MakerNote, ...). An `APP2`/`ICC_PROFILE` got added, ICMP got added, `RST`
markers inserted, the `MPF` thumbnail removed, and the Exif thumbnail is
now 256x171. (Which is fine since the InteropabilityIFD no longer claims that
this is an R98 JPEG, which would limit Exif thumbnail size to 160x120).

* Has APP1 Exif, no APP0 JFIF.
* The main image is 7008x4672.
* Has a mostly empty XMP section.
* Has v2 `ICC_PROFILE`.
* Has ICMP section (...I think).

### GOPRO0027.JPG

Off a GoPro HERO10 Black, unmodified.

* Has APP1 Exif, no APP0 JFIF.
* Has an R98 Interopability IFD, and a 160x120 Exif jpeg thumbnail
  (the max size allowed per R98).
* Has an APP2 MPF IFD pointing at a 960x720 thumbnail.
* The main image is 5568x4176.
* No colorspace information.

### IMG\_9424.JPG

Off an iPhone SE (2nd generation), unmodified. iPhone configured to write
jpeg files (as opposed to the default HEIF).

* Has APP1 Exif, no APP0 JFIF.
* No R98 Interopability IFD, but still a 160x120 Exif jpeg thumbnail.
* Has a GPS IFD.
* No XMP section.
* The main image is 4032x3024.

### long-icc.jpeg

* Has an ICC profile that's spread over several chunks.

Obtained from https://github.com/drewnoakes/metadata-extractor/issues/65

### PXL\_20221005\_164629049.jpg

Taken with a Pixel Pro 6 with the main camera, unmodified.

* Has APP1 Exif, but also an APP0 JFIF later on.
* Has an R98 Interopability IFD, but a 510x384 jpeg thumbnail (not allowed
  per R98)
* Contains GPS IFD.
* Has XMP data split over several markers, using
  `http://ns.adobe.com/xmp/extension/` and `xmpNote:HasExtendedXMP`.
  * XMP data stores `hdrp_makernote` using `xmlns:GCamera`.
* Does _not_ contain depth information.
* Has v4 `ICC_PROFILE` with `para` curves.
* Has trailing debug data after EOI marker.

### stress.jpeg

Has `A2B0` (type `mAB `), `B2A0` (type `mBA `) in its color profile.

Obtained from https://littlecms.com/blog/2020/09/09/browser-check/

Spec PDFs
---------

See `specs` folder.

Where JPEGs can have thumbnails
-------------------------------

* In the JFIF APP0 jfif marker segment (uncompressed 24-bit RGB)
* In the JFXX APP0 jfif extension marker segment (jpeg, 8-bit palletized, or
  uncompressed 24-bit RGB)
* In the Exif APP1 exif segment
* In the 'Photoshop 3.0' APP13 marker segment
* After the main image data, with the MPF extension (indicated by the MPF APP2
  marker segment -- but the image data is outside a marker, so this is the
  only thumbnail that can be larger than 64 kiB)
