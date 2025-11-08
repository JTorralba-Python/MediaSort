#!/usr/bin/env python

import sys
import os
import pathlib
import datetime

def File_Base(File):
    File = os.path.splitext(File)
    Base = File[0]
    return Base

def File_Extension(File):
    File = os.path.splitext(File)
    Extension = File[1].replace('.','').upper()
    return Extension

def EXIF(File):
    Data = ''
    if os.path.isfile(File):
        CMD = 'EXIFTool\\EXIFTool' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()
        Data = CON
    return Data

def Dates(File):
    Data = ''
    if os.path.isfile(File):
        CMD = 'exiftool -' + '*date*' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()
        Data = CON
    return Data

def Tags(File):
    Data = ''
    if os.path.isfile(File):
        Tags = ('datetimeoriginal', 'createdate', 'modifydate', 'contentcreatedate', 'creationdate', 'trackcreatedate', 'trackmodifydate', 'mediacreatedate', 'mediamodifydate', 'filemodifydate', 'filecreatedate', 'fileaccessdate')
        for Tag in Tags:
            CMD = 'exiftool -s -s -s -' + Tag + ' ' + '"' + File + '"'
            CON = os.popen(CMD).read()
            if CON:
                Data = Data + Tag + ' ' + CON[:19] + '\r\n'
    return Data

def Type(File):
    Data = ''
    if os.path.isfile(File):
        Oldest = None
        Newest = None

        FMT = 'EXIFTool\\' + File_Extension(File) + '.fmt'
        if not os.path.isfile(FMT):
            if File_Extension(File) in ('7Z', 'AI', 'AIFF', 'AC3', 'AU', 'BMP', 'DOC', 'DOCX', 'M2V', 'MP3', 'MPEG', 'PNG', 'WAV'):
                return System(File)
            else:
                return Data

        CMD = 'exiftool -q -q -p ' + FMT + ' "' + File + '"'
        #EXIFTool\EXIFTool -list
        #EXIFTool\EXIFTool -s -s -s -"datetimeoriginal" "Sample\Sample.jpg"
        #EXIFTool\EXIFTool -s -s -s -"*date*" "Sample\Sample.jpg"
        #EXIFTool\EXIFTool -q -q -p Format.fmt "Sample\Sample.jpg"

        #Output = os.popen('exiftool -q -q -p EXIFTool\\JPG.fmt ' + File).read()
        CON = os.popen(CMD).read()

        if CON:
            EXIF = eval(CON)
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

            Data = Oldest[:19]
    return Data

def Make(File):
    Data = ''
    if os.path.isfile(File):
        CMD = 'exiftool -s -s -s -' + 'make' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()
        Data = CON.upper()
        Data = Data.replace('\r','')
        Data = Data.replace('\n','')
        Data = Data.replace(':',' ')
        Data = Data.replace('/',' ')
        Data = Data.replace('?',' ')
        Data = Data.replace('<',' ')
        Data = Data.replace('>',' ')
    return Data

def Model(File):
    Data = ''
    if os.path.isfile(File):
        CMD = 'exiftool -s -s -s -' + 'model' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()
        Data = CON.upper()
        Data = Data.replace('\r','')
        Data = Data.replace('\n','')
        Data = Data.replace(':',' ')
        Data = Data.replace('/',' ')
        Data = Data.replace('?',' ')
        Data = Data.replace('<',' ')
        Data = Data.replace('>',' ')
    return Data

def Dimension(File):
    #imagesize
    #exifimagewidth, imagewidth, sourceimagewidth
    #exifimageheight, imageheight, sourceimageheight
    Data = ''
    if os.path.isfile(File):
        CMD = 'exiftool -s -s -s -' + 'imagesize' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()
        Data = CON.replace('x', ' x ')
        Data = Data.replace('\r','')
        Data = Data.replace('\n','')
        Data = Data.replace('0 x 0', '')
    return Data

def Artist(File):
    Data = ''
    if os.path.isfile(File):
        CMD = 'exiftool -s -s -s -' + 'artist' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()
        Data = CON.upper()
        Data = Data.replace('\r','')
        Data = Data.replace('\n','')
        Data = Data.replace(':',' ')
        Data = Data.replace('/',' ')
        Data = Data.replace('?',' ')
        Data = Data.replace('<',' ')
        Data = Data.replace('>',' ')
    return Data

def Album(File):
    Data = ''
    if os.path.isfile(File):
        CMD = 'exiftool -s -s -s -' + 'album' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()
        Data = CON.upper()
        Data = Data.replace('\r','')
        Data = Data.replace('\n','')
        Data = Data.replace(':',' ')
        Data = Data.replace('/',' ')
        Data = Data.replace('?',' ')
        Data = Data.replace('<',' ')
        Data = Data.replace('>',' ')
    return Data

def Title(File):
    Data = ''
    if os.path.isfile(File):
        CMD = 'exiftool -s -s -s -' + 'Title' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()
        Data = CON.upper()
        Data = Data.replace('\r','')
        Data = Data.replace('\n','')
        Data = Data.replace(':',' ')
        Data = Data.replace('/',' ')
        Data = Data.replace('?',' ')
        Data = Data.replace('<',' ')
        Data = Data.replace('>',' ')
    return Data

def System(File):
    Data = ''
    if os.path.isfile(File):
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

        Data = Time.strftime('%Y:%m:%d %H:%M:%S')
    return Data
