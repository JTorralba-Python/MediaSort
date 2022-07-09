from EXIFTool import *

try:

    File = sys.argv[1]

    print('___________________________________________________________________________Dates')
    print()
    print(Dates(File))
    print()

    print('____________________________________________________________________________Tags')
    print()
    print(Tags(File))
    print()

    print('____________________________________________________________________________Type')
    print()
    print(Type(File))
    print()

    print('_______________________________________________________________________Dimension')
    print()
    print(Dimension(File))
    print()

    print('__________________________________________________________________________System')
    print()
    print(System(File))
    print()

except:
    pass
