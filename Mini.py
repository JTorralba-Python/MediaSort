import os
import shutil
import sys
import traceback

def Global():

    global Slash

    if os.name == 'nt':
        Slash = '\\'
    else:
        Slash = '/'

def Clear():

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def Destination(File):

    if os.path.isfile(File):

        Target_Path = Location + Slash + '..'
        Target_File = '0000-00-00_000000'

        Extension = ''
        Make = ''
        Model = ''
        Dimension = ''
        Date = ''

        String = os.path.splitext(File)
        Extension = String[1].replace('.','').upper()

        if Extension != '':
            Target_Path = Target_Path + Slash + Extension

        CMD = 'EXIFTool\\EXIFTool -s' + ' ' + '-*date* -make -model -imagesize' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read().upper()

        Data = CON
        Data = Data.replace('\r', '')
        Data = Data.split('\n')

        DateList = []

        for Record in Data:

            Key = Record[:32].strip()
            Value = Record[34:].strip()

            if 'DATE' in Key and 'EXTENSION' not in Key and 'PROFILE' not in Key:
                Date = Value[:19]

                Filter = Date
                Filter = Filter.replace(' ', '')
                Filter = Filter.replace(':', '')

                if Date != '0000:00:00 00:00:00' and Filter.isnumeric() and len(Filter) == 14:
                    DateList.append(Date)
            else:
                if Key == 'MAKE':
                    Make = Value.replace(':', ' ').replace('/', ' ').replace('.', ' ').replace(',', ' ').replace('  ', ' ').strip()
                    if Make != '':
                        Target_Path = Target_Path + Slash + Make
                else:
                    if Key == 'MODEL':
                        Model = Value.replace(':', ' ').replace('/', ' ').replace('.', ' ').replace(',', ' ').replace('  ', ' ').strip()
                        if Model != '':
                            Target_Path = Target_Path + Slash + Model
                    else:
                        if Key == 'IMAGESIZE':
                            Dimension = Value.replace('X', ' x ')
                            if Dimension != '':
                                Target_Path = Target_Path + Slash + Dimension

        DateList.sort()

        Date = DateList[0]
        
        if Date != '':

            Date_YYYY = Date[0:4]
            Date_MM = Date[5:7]
            Date_DD = Date[8:10]

            Time_HH = Date[11:13]
            Time_MM = Date[14:16]
            Time_SS = Date[17:19]

            Target_File = Date_YYYY + '-' + Date_MM + '-' + Date_DD + '_' + Time_HH + Time_MM + Time_SS

        Unique_File = Target_File
        I = 0
        while os.path.isfile(Target_Path + Slash + Unique_File + '.' + Extension.lower()):
            I += 1
            Unique_File = Target_File + '_' + str(I).zfill(6)

        Target_File = Unique_File + '.' + Extension.lower()

    return Target_Path, Target_File

def Process():

    for Path, Folders, Files in os.walk(Location, topdown = False):

        for File in sorted(Files, reverse = True):

            Source = Path + Slash + File

            Target_Path, Target_File = Destination(Source)
            Target = Target_Path + Slash + Target_File

            if not os.path.exists(Target_Path):
                try:
                    os.makedirs(Target_Path, 777)
                except:
                    print(traceback.format_exc())

            try:
                shutil.move(Source, Target)
            except:
                print(traceback.format_exc())

            print(Target_Path + Slash + Target_File)

        try:
            if len(os.listdir(Path)) == 0:
                os.rmdir(Path)
        except:
            pass

def Main():

    Process()

if __name__ == '__main__':

    global Location
    try:
        Location = sys.argv[1]
    except:
        Location = None

    Clear()

    Global()

    if Location != None and os.path.exists(Location):
        Main()
    else:
        print('Location not defined or not found or invalid.')
