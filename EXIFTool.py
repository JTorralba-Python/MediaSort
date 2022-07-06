#!/usr/bin/env python

import sys
import os
import pathlib
import datetime

def Extension(File):
    Input = os.path.splitext(File)
    Root = Input[0]
    Extension = Input[1].upper()
    return Extension

def EXIFTool(File):
    try:
        Oldest = None
        Newest = None

        CMD = 'EXIFTool\\EXIFTool -q -q -p EXIFTool\\' + Extension(File) + '.fmt ' + '"' + File + '"'
        #EXIFTool\EXIFTool -list
        #EXIFTool\EXIFTool -s -s -s -"datetimeoriginal" "Sample\Sample.jpg"
        #EXIFTool\EXIFTool -s -s -s -"*date*" "Sample\Sample.jpg"
        #EXIFTool\EXIFTool -q -q -p Format.fmt "Sample\Sample.jpg"

        #Output = os.popen('EXIFTool\\EXIFTool -q -q -p EXIFTool\\JPG.fmt ' + File).read()
        Data = os.popen(CMD).read()

        if not Data:
            CMD = 'EXIFTool\\EXIFTool -q -q -p EXIFTool\\' + 'System.fmt ' + '"' + File + '"'
            Data = os.popen(CMD).read()

        if Data:
            EXIF = eval(Data)
            ASC = tuple(sorted(EXIF))
            DSC = tuple(sorted(EXIF, reverse = True))

            X = len(ASC)
            I = 0
            while I < X:
                Oldest = ASC[I]
                if Oldest == '0000:00:00 00:00:00':
                    I += 1
                else:
                    I = X

            X = len(DSC)
            I = 0
            while I < X:
                Newest = ASC[I]
                if Newest == '0000:00:00 00:00:00':
                    I += 1
                else:
                    I = X

            return Oldest[:19]

    except:
        print('EXIFTool(File): ' + traceback.format_exc())
        return None

def DeepScan(File):
    Tags = ('datetimeoriginal', 'createdate', 'modifydate', 'contentcreatedate', 'creationdate', 'trackcreatedate', 'trackmodifydate', 'mediacreatedate', 'mediamodifydate', 'filemodifydate', 'filecreatedate', 'fileaccessdate')

    for Tag in Tags:
        CMD = 'EXIFTool\\EXIFTool -s -s -s -' + Tag + ' ' + '"' + File + '"'
        Data = os.popen(CMD).read()
        if Data:
            print(Data[:19])

def Dimension(File):
    #exifimagewidth, imagewidth, sourceimagewidth
    #exifimageheight, imageheight, sourceimageheight

    CMD = 'EXIFTool\\EXIFTool -q -q -p ' + 'EXIFTool\Dimension.fmt' + ' ' + '"' + File + '"'
    Dimension = os.popen(CMD).read()
    if not Dimension:
        Dimension = '0 x 0'

    Dimension = Dimension.replace('\n', '')
    Dimension = Dimension.replace('\r', '')

    return Dimension

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

