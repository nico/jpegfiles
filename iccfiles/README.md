iccfiles
========

Various ICC profiles.

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

```
v4.0.0, Display
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

```
v2.1.0, Input
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
