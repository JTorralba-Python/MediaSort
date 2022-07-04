#!/usr/bin/env python

import sys
import os
import pathlib
import datetime

from PIL import Image
from PIL.ExifTags import TAGS

def Pillow_All(File):
  try:
    EXIF = Image.open(File)._getexif()
    Data = ''
    for (Key, Value) in EXIF.items():
      Data = Data + '%s = %s' % (TAGS.get(Key), Value)
      Data = Data + '\r\n'
    return Data
  except:
    return 'N/A'

def Pillow(File, Tag):
  try:
    EXIF = Image.open(File)._getexif()
    for (Key, Value) in EXIF.items():
      if TAGS.get(Key) == Tag:
        return Value
  except:
    return 'N/A'

def System(File):
  try:
    CTime = datetime.datetime.fromtimestamp(pathlib.Path(File).stat().st_ctime)
    MTime = datetime.datetime.fromtimestamp(pathlib.Path(File).stat().st_mtime)
    ATime = datetime.datetime.fromtimestamp(pathlib.Path(File).stat().st_atime)

    #print('C = ' + CTime.strftime('%Y:%m:%d %H:%M:%S'))
    #print('M = ' + MTime.strftime('%Y:%m:%d %H:%M:%S'))
    #print('A = ' + ATime.strftime('%Y:%m:%d %H:%M:%S'))

    Time = CTime

    if MTime < Time:
      Time = MTime
    
    if ATime < Time:
      Time = ATime

    return Time.strftime('%Y:%m:%d %H:%M:%S')
  except:
    return 'N/A'

try:

  File = sys.argv[1]

  print('__________________________________________________________________________Pillow')
  print()
  #print(Pillow_All(File))
  print('%s = %s' % ('Make', Pillow(File,'Make')))
  print('%s = %s' % ('Model', Pillow(File,'Model')))
  print('%s = %s' % ('DateTimeOriginal', Pillow(File,'DateTimeOriginal')))
  print('%s = %s' % ('DateTimeDigitized', Pillow(File,'DateTimeDigitized')))
  print('%s = %s' % ('DateTime', Pillow(File,'DateTime')))
  print('%s = %s x %s' % ('Dimensions', Pillow(File,'ExifImageWidth'), Pillow(File,'ExifImageHeight')))
  print()

  print('__________________________________________________________________________System')
  print()
  print(System(File))
  print()

except:
  pass
