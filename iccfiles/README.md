iccfiles
========

Various ICC profiles.

cmyk-mft1mft2.icc
-----------------

From [a CMYK jpeg](https://upload.wikimedia.org/wikipedia/en/2/25/Channel_digital_image_CMYK_color.jpg).

Unusual class, data color space, PCS, rendering intent.
Containts mft1 and mft2 tag types, and a `'gamt'` tag.

```
v2.1.0, Output, CMYK, PCSLAB, Media-relative colorimetric
'desc': 'desc', offset 252, size 116
'cprt': 'text', offset 368, size 43
'wtpt': 'XYZ ', offset 412, size 20
'A2B0': 'mft2', offset 432, size 41478
'A2B2': 'mft2', offset 432, size 41478
'A2B1': 'mft2', offset 41912, size 41478
'B2A0': 'mft1', offset 83392, size 145588
'B2A1': 'mft1', offset 228980, size 145588
'B2A2': 'mft1', offset 374568, size 145588
'gamt': 'mft1', offset 520156, size 37009
```

lightroom.icc
-------------

From ../DSC03136-exported.jpg. Normal v2 matrix-based profile, but contains
a few additional tags and types.

```
v2.1.0, Display
'cprt': 'text', offset 336, size 51
'desc': 'desc', offset 388, size 108
'wtpt': 'XYZ ', offset 496, size 20
'bkpt': 'XYZ ', offset 516, size 20
'rXYZ': 'XYZ ', offset 536, size 20
'gXYZ': 'XYZ ', offset 556, size 20
'bXYZ': 'XYZ ', offset 576, size 20
'dmnd': 'desc', offset 596, size 112
'dmdd': 'desc', offset 708, size 136
'vued': 'desc', offset 844, size 134
'view': 'view', offset 980, size 36
'lumi': 'XYZ ', offset 1016, size 20
'meas': 'meas', offset 1036, size 36
'tech': 'sig ', offset 1072, size 12
'rTRC': 'curv', offset 1084, size 2060
'gTRC': 'curv', offset 1084, size 2060
'bTRC': 'curv', offset 1084, size 2060
```

mABmBA.icc
----------

From [a color.org test image](https://www.color.org/Upper_Left.jpg).

Contains several 'mAB ', 'mBA ' tags, some with and some without CLUT.
The CLUTs are 16-bit and small (2x2x2).

```
v4.0.0, Display, XYZ, RGB
'cprt': 'mluc', offset 264, size 110
'desc': 'mluc', offset 376, size 40
'wtpt': 'XYZ ', offset 416, size 20
'bkpt': 'XYZ ', offset 436, size 20
'chad': 'sf32', offset 456, size 44
'A2B0': 'mAB ', offset 500, size 1688
'A2B2': 'mAB ', offset 500, size 1688
'A2B1': 'mAB ', offset 2188, size 1688
'B2A0': 'mBA ', offset 3876, size 1792
'B2A2': 'mBA ', offset 3876, size 1792
'B2A1': 'mBA ', offset 5668, size 1792
```

mft2.icc
--------

From ../check\_lut.jpeg

CLUT size is 17, but it's an artificial, monochromatic CLUT.

```
v2.1.0, Input, XYZ, RGB
'desc': 'desc', offset 204, size 212
'cprt': 'text', offset 416, size 41
'wtpt': 'XYZ ', offset 460, size 20
'A2B0': 'mft2', offset 480, size 29554
'A2B1': 'mft2', offset 480, size 29554
'A2B2': 'mft2', offset 480, size 29554
```

p3-v4.icc
---------

From ../IMG\_9424.JPG

Very normal matrix-based profile for Display P3. The three curves share an
offset.

```
v4.0.0, Display
'desc': 'mluc', offset 252, size 48
'cprt': 'mluc', offset 300, size 80
'wtpt': 'XYZ ', offset 380, size 20
'rXYZ': 'XYZ ', offset 400, size 20
'gXYZ': 'XYZ ', offset 420, size 20
'bXYZ': 'XYZ ', offset 440, size 20
'rTRC': 'para', offset 460, size 32
'chad': 'sf32', offset 492, size 44
'bTRC': 'para', offset 460, size 32
'gTRC': 'para', offset 460, size 32
```

sRGB-Adobe.icc
--------------

/Library/Application\ Support/Adobe/Color/Profiles/Recommended/sRGB\ Color\ Space\ Profile.icm
with Photoshop installed on macOS.

sRGB-apple.icc
--------------

/System/Library/ColorSync/Profiles/sRGB Profile.icc on macOS 13.2.

sRGB-gimp.icc
-------------

Extracted from a jpeg written by GIMP 2.10.32 (revision 1), by making a new
image, in Advanced Options picking "Color profile: Built-in RGB (GIMP built-in
sRGB)".

sRGB-Compact-ICC-Profiles-v4.icc
--------------------------------

https://github.com/saucecontrol/Compact-ICC-Profiles/blob/8e22c54/profiles/sRGB-v4.icc

sRGB-pixel.icc
--------------

Extracted from a jpeg taken with a Pixel 7 Pro running Android 13.

sRGB-RTv4.icc
-------------

[source](https://github.com/Beep6581/RawTherapee/blob/3ba386d/rtdata/iccprofiles/output/RTv4_sRGB.icc)

Raw Therapee's sRGB profile.

sRGB\_v4\_ICC\_preference.icc
-----------------------------

[source](https://www.color.org/srgbprofiles.xalter)

A LAB sRGB profile.

Large-ish (17x17x17) CLUT with RGB data color space, in mAB / mBA tags.

```
4.2.0, ColorSpace, LAB, RGB
'desc': 'mluc', offset 240, size 118
'A2B0': 'mAB ', offset 360, size 29712
'A2B1': 'mAB ', offset 30072, size 436
'B2A0': 'mBA ', offset 30508, size 29748
'B2A1': 'mBA ', offset 60256, size 508
'rig0': 'sig ', offset 60764, size 12
'wtpt': 'XYZ ', offset 60776, size 20
'cprt': 'mluc', offset 60796, size 118
'chad': 'sf32', offset 60916, size 44
```
