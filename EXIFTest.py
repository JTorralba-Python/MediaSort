#!/usr/bin/env python

import sys
import os
import pathlib
import datetime

from PIL import Image
from PIL.ExifTags import TAGS

def Get_Value(EXIF, Tag):
  for (Key, Value) in EXIF.items():
    if TAGS.get(Key) == Tag:
      return Value

def Get_All_Tags(EXIF):
  for (Key, Value) in EXIF.items():
    print('%s = %s' % (TAGS.get(Key), Value))

def FileCreated(File):
  CTime = datetime.datetime.fromtimestamp(pathlib.Path(File).stat().st_ctime)
  MTime = datetime.datetime.fromtimestamp(pathlib.Path(File).stat().st_mtime)
  if CTime <= MTime:
    Time = CTime
  else:
    Time = MTime
  return Time.strftime('%Y:%m:%d %H:%M:%S')


try:
  File = sys.argv[1]
  EXIF = Image.open(File)._getexif()

  #Get_All_Tags(EXIF)

  print('%s = %s' % ('Make', Get_Value(EXIF,'Make')))
  print('%s = %s' % ('Model', Get_Value(EXIF,'Model')))
  print('%s = %s' % ('DateTimeOriginal', Get_Value(EXIF,'DateTimeOriginal')))
  print('%s = %s' % ('DateTimeDigitized', Get_Value(EXIF,'DateTimeDigitized')))
  print('%s = %s' % ('DateTime', Get_Value(EXIF,'DateTime')))
  print('%s = %s x %s' % ('Dimensions', Get_Value(EXIF,'ExifImageWidth'), Get_Value(EXIF,'ExifImageHeight')))
  print('%s = %s' % ('FileCreated', FileCreated(File)))


except:
  pass
