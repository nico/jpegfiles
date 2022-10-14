jpegfiles
=========

Various jpeg test images, and spec PDFs

Images
------

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

Spec PDFs
---------

See `specs` folder.
