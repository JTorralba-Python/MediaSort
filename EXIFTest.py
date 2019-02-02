#!/usr/bin/env python

import sys

from PIL import Image
from PIL.ExifTags import TAGS

def Get_Value (EXIF, Key):
  for (K, V) in EXIF.iteritems():
    if TAGS.get(K) == Key:
      return V

def Get_All_Tags (EXIF):
  for (K, V) in EXIF.iteritems():
    print K, V


try:
  EXIF = Image.open(sys.argv[1])._getexif()
  #Get_All_Tags(EXIF)
  #print Get_Value(EXIF,'ExifVersion')
  #print Get_Value(EXIF,'Make'), Get_Value(EXIF,'Model')
  print Get_Value(EXIF,'DateTimeOriginal')
  print Get_Value(EXIF,'DateTimeDigitized')
  print Get_Value(EXIF,'DateTime')
  #print Get_Value(EXIF,'ExifImageWidth'), 'X', Get_Value(EXIF,'ExifImageHeight')
except:
  pass

