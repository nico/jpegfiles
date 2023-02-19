iccfiles
========

Various ICC profiles.

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
