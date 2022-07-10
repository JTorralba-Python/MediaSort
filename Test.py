from EXIFTool import *

try:

    File = sys.argv[1]

    print('____________________________________________________________________________EXIF')
    print()
    print(EXIF(File))
    print()

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

    # print('____________________________________________________________________________Make')
    # print()
    # print(Make(File))
    # print()

    # print('___________________________________________________________________________Model')
    # print()
    # print(Model(File))
    # print()

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
