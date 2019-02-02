#!/usr/bin/env python

from Tkinter import *
import time
import os
import sys
import thread
import traceback
import Queue
import shutil
import tkFileDialog

from PIL import Image
from PIL.ExifTags import TAGS

class StopWatch(Frame):

    def __init__(self, parent=None, **kw):

        Frame.__init__(self, parent, kw)
        self.Queue = Queue.Queue()
        self.Running = 0

        self.Timer = StringVar()
        self.Timer_Start = time.time()
        self.Timer_Elapsed = 0.0

        self.Widgets()
        self.Update()

        self.Location = WhereAmI()
        self.Queue_Add('LOC: ' + self.Location)

    def Widgets(self):
        TimerLabel = Label(self, textvariable=self.Timer)
        self.Set(self.Timer_Elapsed)
        TimerLabel.pack(fill=X, expand=NO, pady=2, padx=2)

        SBH = Scrollbar(self, orient=HORIZONTAL)
        SBH.pack(side=BOTTOM, fill=X)

        SBV = Scrollbar(self, orient=VERTICAL)
        SBV.pack(side=RIGHT, fill=Y)

        global Console
        # Windows scrollbar bug/crash.
        if (os.name == 'nt'):
            Console = Text(self, wrap=NONE)
        else:
            Console = Text(self, wrap=NONE, xscrollcommand=SBH.set, yscrollcommand=SBV.set)
        Console.pack(expand=TRUE, fill=BOTH)
        Console.bind("<Configure>", lambda e: Console.configure(width=e.width-10))
        SBH.config(command=Console.xview)
        SBV.config(command=Console.yview)

    def Set(self, Elapse):
        Minutes = int(Elapse/60)
        Seconds = int(Elapse - Minutes*60.0)
        HSeconds = int((Elapse - Minutes*60.0 - Seconds)*100)
        self.Timer.set('%02d:%02d:%02d' % (Minutes, Seconds, HSeconds))

    def StartStop(self):
        if not self.Running:
            self.Timer_Start = time.time() - self.Timer_Elapsed
            self.Update()
            self.Running = 1
        else:
            self.after_cancel(self._timer)
            self.Timer_Elapsed = time.time() - self.Timer_Start
            self.Set(self.Timer_Elapsed)
            self.Running = 0

    def Reset(self):
        with self.Queue.mutex:
            self.Queue.queue.clear()
        Console.delete(1.0, END)
        self.Timer_Start = time.time()
        self.Timer_Elapsed = 0.0
        self.Set(self.Timer_Elapsed)

    def Queue_Add(self, Line):
        self.Queue.put(Line)

    def Write(self, Line):
        try:
            Line = Line.replace('\r', '')
            RowCol = Console.index('end-1c')
            LineNumber = RowCol[:-2]
            Console.insert(END, '%s\n' % Line.encode("utf-8"))
            Console.see(END)
            Console.tag_add(LineNumber, RowCol, str(float(RowCol) + 0.4))
            if (Line[:3] == 'LOC'):
                Console.tag_config(LineNumber, background="red", foreground="black")
            else:
                if Line[:3] == 'MED':
                    Console.tag_config(LineNumber, background="blue", foreground="black")
                else:
                    if Line[:3] == 'FYI':
                        Console.tag_config(LineNumber, background="green", foreground="black")
                    else:
                        if (Line[:3] == 'EXC'):
                            Console.tag_config(LineNumber, background="yellow", foreground="black")
                        else:
                            Console.tag_config(LineNumber, background="white", foreground="black")
            Console.pack()
            Console.update_idletasks()
        except:
            print traceback.format_exc()
            pass

    def Update(self):
        if self.Running:
            self.Timer_Elapsed = time.time() - self.Timer_Start
            self.Set(self.Timer_Elapsed)
        try:
            Line = self.Queue.get_nowait()
            self.Write(Line)
        except:
            pass

        self._timer = self.after(100, self.Update)

    def MED_Button_Root_LED(self):
        if MED_Button.cget('state') == DISABLED:
            BG = MED_Button.cget('bg')
            FG = MED_Button.cget('fg')
            MED_Button.configure(bg = FG)
            MED_Button.configure(fg = BG)
            self.after(500, self.MED_Button_Root_LED)
        else:
            MED_Button.configure(bg = MED_Button_BG)
            MED_Button.configure(fg = MED_Button_FG)

    def GetLocation(self):
        Options = {}
        Options['initialdir'] = self.Location
        Options['filetypes'] = [('JPG Files','.jpg'),('JPG Files','.JPG'),('AVI Files','.avi'),('AVI Files','.AVI'),('MOV Files','.mov'),('MOV Files','.MOV'),('WAV Files','.wav'),('WAV Files','.WAV')]
        Options['title'] = 'Open Media File'
        File = tkFileDialog.askopenfilename(**Options)
        if File:
            self.Location = os.path.split(File)[0]
            self.Queue_Add('LOC: ' + self.Location)

def Clear():
    global CMD
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def S_Action(SW):
    SW.StartStop()

def R_Action(SW):
    SW.Reset()

def Worker(SW, Thread):
    Button_X = Thread + '_Button'
    Button_X_BG = Thread + '_Button_BG'
    Button_X_FG = Thread + '_Button_FG'

    globals()[Button_X_BG] = globals()[Button_X].cget('bg')
    globals()[Button_X_FG] = globals()[Button_X].cget('fg')
    globals()[Button_X].configure(state=DISABLED)

    CMD = 'SW.' + Button_X + '_Root_LED()'
    exec CMD
    thread.start_new(globals()[Thread], (SW,))

def Sleep():
    time.sleep(0)

def WhereAmI():
    return os.path.dirname(os.path.realpath(__import__("__main__").__file__))

def Get_Value (EXIF, Key):
    for (K, V) in EXIF.iteritems():
        if TAGS.get(K) == Key:
            # print K, V
            return V

def MED(SW):
    SW.StartStop()
    Current_Location = SW.Location
    if Current_Location != 'CANCEL':
        for File in os.listdir(Current_Location):
            if os.path.isfile(os.path.join(Current_Location, File)):
                From = Current_Location + '/' + File
                EXT = File[-3:].upper()
                if EXT.upper() == 'JPG':
                    SW.Queue_Add('FYI: ' + File)
                    try:
                        EXIF = Image.open(From)._getexif()

                        DateTimeOriginal = Get_Value(EXIF,'DateTimeOriginal')
                        if DateTimeOriginal == None:
                            SW.Queue_Add('FYI: DateTimeOriginal N/A')
                            DateTimeOriginal = Get_Value(EXIF,'DateTimeDigitized')
                            if DateTimeOriginal == None:
                                SW.Queue_Add('FYI: DateTimeDigitized N/A')
                                DateTimeOriginal = Get_Value(EXIF,'DateTime')
                                if DateTimeOriginal == None:
                                    FileName = File[:-4].upper().replace("-",":").replace(".",":")
                                    Length = len(FileName)
                                    Space = FileName[10:11]
                                    Colons = FileName.count(':')
                                    if (Length == 19) and (Space == " ") and (Colons == 4):
                                        DateTimeOriginal = FileName
                                    else:
                                        SW.Queue_Add('FYI: DateTime N/A')
                        SW.Queue_Add('MED: ' + DateTimeOriginal)

                        Date_YYYY = DateTimeOriginal[0:4]
                        Date_MM = DateTimeOriginal[5:7]
                        Date_DD = DateTimeOriginal[8:10]
                        Time_HH = DateTimeOriginal[11:13]
                        Time_MM = DateTimeOriginal[14:16]
                        Time_SS = DateTimeOriginal[17:19]

                        New_Location = Current_Location + '/' + Date_YYYY + '/' + Date_MM + '/' + Date_DD + '/' + Time_HH + '00' + '/'
                        New_File = Date_YYYY + '-' + Date_MM + '-' + Date_DD + '_' + Time_HH + Time_MM + Time_SS
                        To = New_Location + New_File + '.' + EXT.lower()

                        if not os.path.exists(New_Location):
                            os.makedirs(New_Location, 0777);
                        shutil.move(From, To)
                        SW.Queue_Add('MED: ' + File + ' --> ' + To)
                    except:
                        #print traceback.format_exc()
                        SW.Queue_Add('EXC: EXIF N/A')
                        pass
            Sleep()
    MED_Button.configure(state=NORMAL)
    SW.StartStop()

def LOC_Action(SW):
    SW.GetLocation()

def main():
    root = Tk()
    root.title("MediaSort")
    root.geometry("640x480")
    root.resizable(0,0)

    SW = StopWatch(root)
    SW.pack(side=TOP, expand=TRUE, fill=BOTH)

    PadX = 10

    global MED_Button
    MED_Button = Button(root, text='MED', padx=PadX*2, command=lambda:Worker(SW,'MED'))
    MED_Button.pack(side=LEFT)

    LOC_Button = Button(root, text='LOC', padx=PadX*2, command=lambda:LOC_Action(SW))
    LOC_Button.pack(side=LEFT)

    Q_Button = Button(root, text='Q', padx=PadX, command=root.destroy)
    Q_Button.pack(side=RIGHT)

    R_Button = Button(root, text='R', padx=PadX, command=lambda:R_Action(SW))
    R_Button.pack(side=RIGHT)

    S_Button = Button(root, text='S', padx=PadX, command=lambda:S_Action(SW))
    S_Button.pack(side=RIGHT)

    root.mainloop()

if __name__ == '__main__':
    Clear()
    main()
