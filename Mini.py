import os
import sys

def Clear():

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def Date():

    Date = []

    Data = ''
    if os.path.isfile(File):
        CMD = 'EXIFTool\\EXIFTool -s -s -s -' + '*date*' + ' ' + '"' + File + '"'
        CON = os.popen(CMD).read()

        Data = CON
        Data = Data.replace('\r', '')
        Data = Data.replace('\n', '|')
        Data = Data.split('|')

        for Record in Data:
            DateTime = Record[:19]
            Filter = DateTime
            Filter = Filter.replace(' ', '')
            Filter = Filter.replace(':', '')
            if Filter.isnumeric()and len(Filter) == 14:
                Date.append(DateTime)

        Date.sort()
       
        return Date[0]

def Main():

    print(Date())

if __name__ == '__main__':

    global File
    try:
        File = sys.argv[1]
    except:
        File = 'Sample\\Sample.jpg'

    Clear()
    Main()
