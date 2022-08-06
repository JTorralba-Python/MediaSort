import os
import sys

def HelloWorld():

    print('HelloWorld')

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

def AIO(File):

    if os.path.isfile(File):

        Extension = ''
        Make = ''
        Model = ''
        Dimension = ''
        Date = ''

        String = os.path.splitext(File)
        Extension = String[1].replace('.','').upper()

        CMD = 'EXIFTool\\EXIFTool -s' + ' ' + '-*date* -imagesize -make -model' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read().upper()

        Data = CON

        Data = Data.replace('\r', '')
        Data = Data.split('\n')

        DateList = []

        for Record in Data:

            Key = Record[:32].strip()
            Value = Record[34:].strip()

            if 'DATE' in Key:
                
                Date = Value[:19]

                Filter = Date
                Filter = Filter.replace(' ', '')
                Filter = Filter.replace(':', '')

                if Filter.isnumeric()and len(Filter) == 14:
                    DateList.append(Date)

            else:

                if Key == 'IMAGESIZE':

                    Dimension = Value.replace('X', ' x ')

                else:

                    if Key == 'MAKE':

                        Make = Value.replace(':', ' ').replace('/', ' ')

                    else:

                        if Key == 'MODEL':

                            Model = Value.replace(':', ' ').replace('/', ' ')

        DateList.sort()

        Extension = Extension + ' '
        Make = Make + ' '
        Model = Model + ' '
        Dimension = Dimension + ' '
        Date = DateList[0] + ' '

        Detail = Extension.lstrip() + Make.lstrip() + Model.lstrip() + Dimension.lstrip() + Date.lstrip()
        print(Detail)

    return

def Process():

    for Path, Folders, Files in os.walk(Location, topdown=False):

        for File in sorted(Files, reverse=True):

            Source = Path + Slash + File
            AIO(Source)

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
        Location = 'Test'

    Clear()
    Global()
    Main()
