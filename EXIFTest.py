#!/usr/bin/env python

import sys

from PIL import Image
from PIL.ExifTags import TAGS

def Get_Value(EXIF, Tag):
  for (Key, Value) in EXIF.items():
    if TAGS.get(Key) == Tag:
      return Value

def Get_All_Tags(EXIF):
  for (Key, Value) in EXIF.items():
    print('%s = %s' % (TAGS.get(Key), Value))

try:
  EXIF = Image.open(sys.argv[1])._getexif()

  #Get_All_Tags(EXIF)

  print('%s = %s' % ('Make', Get_Value(EXIF,'Make')))
  print('%s = %s' % ('Model', Get_Value(EXIF,'Model')))
  print('%s = %s' % ('DateTimeOriginal', Get_Value(EXIF,'DateTimeOriginal')))
  print('%s = %s' % ('DateTimeDigitized', Get_Value(EXIF,'DateTimeDigitized')))
  print('%s = %s' % ('DateTime', Get_Value(EXIF,'DateTime')))
  print('%s = %s x %s' % ('Dimensions', Get_Value(EXIF,'ExifImageWidth'), Get_Value(EXIF,'ExifImageHeight')))
except:
  pass
