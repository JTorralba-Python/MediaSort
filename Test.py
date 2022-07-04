from EXIFTool import *

try:

    File = sys.argv[1]

    print('________________________________________________________________________EXIFTool')
    print()
    print(EXIFTool(File))
    print()

    print('________________________________________________________________________DeepScan')
    print()
    DeepScan(File)
    print()

    print('__________________________________________________________________________System')
    print()
    print(System(File))
    print()

    print('_______________________________________________________________________Dimension')
    print()
    print(Dimension(File))
    print()

except:
    pass
