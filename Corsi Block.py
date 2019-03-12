import tkinter as tk
from tkinter import *
import random
import csv
import sys
import time
import os

def dirCreate():
    try:
        os.mkdir('data')
    except:
        pass

def directFile():
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]
    return script_dir

def start_up():
    global corRounds, spanNum, numRounds, Results, canvas
    Results = []
    corRounds = 0
    spanNum = 2
    numRounds = 0
    root = tk.Tk()
    root.state('zoomed')
    try:
        with open('settings.txt', mode = 'r') as R:
            scaleVal = int(next(R))
            settings_set = 1
        startButton = tk.Button(root, text = 'Start', width = 10, height = 5, bg = 'green', command = lambda: selector(pEntry, pGroup, root, scaleVal, settings_set, pracOpt.get()))
    except:
        scaleSelect = tk.Scale(root, from_=0, to=1800, orient=HORIZONTAL, command = lambda x: lineLength(scaleSelect.get(), root), bigincrement = 10)
        L1 = tk.Label(root, text = 'Make the length of the line measure 10cm on your screen')
        scaleSelect.pack()
        L1.pack()
        canvas = tk.Canvas(root)
        settings_set = 0
        startButton = tk.Button(root, text = 'Start', width = 10, height = 5, bg = 'green', command = lambda: selector(pEntry, pGroup, root, scaleSelect.get(), settings_set, pracOpt.get()))
    L2 = tk.Label(root, text = 'Participant number:')
    L3 = tk.Label(root, text = 'Practice Block:')
    L4 = tk.Label(root, text = 'Direction:')
    pEntry = Entry(root)
    pGroup = tk.StringVar(root)
    pGroup.set('Forward') # default value
    Opt = tk.OptionMenu(root, pGroup, 'Forward', 'Backward')
    pracOpt = tk.StringVar(root)
    pracOpt.set('Yes')
    Opt1 = tk.OptionMenu(root, pracOpt, 'Yes', 'No')
    startButton.pack(side = BOTTOM)
    Opt.pack(side = BOTTOM)
    L4.pack(side = BOTTOM)
    Opt1.pack(side = BOTTOM)
    L3.pack(side = BOTTOM)
    pEntry.pack(side = BOTTOM)
    L2.pack(side = BOTTOM)
    root.mainloop()

def lineLength(scaleVal, root):
    global canvas
    canvas.destroy()
    xval = scaleVal + 60
    canvas = tk.Canvas(root)
    canvas.create_line(60, 25, xval, 25)
    canvas.pack(fill = BOTH, expand = 1)

def selector(pNum, group, root, scaleVal, settings_set, pracBlock):
    Results.append(pNum.get())
    root.destroy()
    if settings_set == 0:
        with open('settings.txt', mode = 'w') as f:
            f.write(str(scaleVal))
            f.close()
    else:
        pass
    global mmToPix
    mmToPix = scaleVal / 100
    Group = group.get()
    Results.append(Group)
    if Group == 'Forward':
        if pracBlock == 'Yes':
            randList(2, 'Forward', 'Yes')
            randList(2, 'Forward')
        elif pracBlock == 'No':
            randList(2, 'Forward')
    if Group == 'Backward':
        if pracBlock == 'Yes':
            randList(2, 'Backward', 'Yes')
            randList(2, 'Backward')
        elif pracBlock == 'No':
            randList(2, 'Backward')
    
def start_time():
    global initTime
    initTime = time.time()

def change_colour(button, position):
    corButList.append(position)
    button.config(bg = 'yellow')
    button.after(1000, lambda: button.config(bg = 'blue'))

def ButtonHolderRefresh():
    global ButtonList
    ButtonList = []

def ButtonHolderBuild(value):  
    ButtonList.append(value)

def presFeedback(text, spanNum, Type, pracBlock, end = 0):
    root1 = tk.Tk()
    root1.geometry('300x200+810+440')
    L1 = tk.Label(root1, text = text, font = ('Helvetica', 14))
    L1.place(relx=0.5, rely=0.5, anchor=CENTER)
    root1.after(2000, lambda: root1.destroy())
    root1.mainloop()
    if end == 0:
         randList(spanNum, Type, pracBlock)
    elif end == 1:
        presEndPrac()
            
def presEndPrac():
    root1 = tk.Tk()
    root1.geometry('500x200+710+440')
    L1 = tk.Label(root1, text = 'This is the end of the practice trials, press go to begin the experiment')
    button = tk.Button(root1, text = 'Go', bg = 'green', command = lambda: root1.destroy())
    L1.place(relx=0.5, rely=0.4, anchor=CENTER)
    button.place(relx=0.5, rely=0.5, anchor=CENTER)

def ansCheck(rootVal, Type):
    RespTime = int(round((time.time()- initTime), 4) * 1000)
    rootVal.destroy()
    Results.append(len(corButList))
    Results.append(RespTime)
    global corRounds, spanNum, numRounds
    numRounds += 1
    if Type == 'Forward':
        if ButtonList == corButList:
            corRounds += 1
            Results.append('correct')
            if numRounds < 2:
                randList(spanNum, Type)
            elif numRounds == 2:
                spanNum += 1
                corRounds = 0
                numRounds = 0
                if spanNum > 9:
                    with open(directFile() + '\\data\\Corsi_data.csv', mode = 'a') as dataFile:
                        data_writer = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        data_writer.writerow(Results)
                    dataFile.close()
                    sys.exit()
                else:
                    randList(spanNum, Type)
        elif ButtonList!= corButList:
            Results.append('incorrect')
            if numRounds < 2:
                randList(spanNum, Type)
            elif numRounds == 2 and corRounds == 0:
                Results.append(spanNum-1)
                with open(directFile() + '\\data\\Corsi_data.csv', mode = 'a') as dataFile:
                    data_writer = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    data_writer.writerow(Results)
                dataFile.close()
                sys.exit()
            elif numRounds == 2 and corRounds >= 1:
                spanNum += 1
                corRounds = 0
                numRounds = 0
                if spanNum > 9:
                    with open(directFile() + '\\data\\Corsi_data.csv', mode = 'a') as dataFile:
                        data_writer = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        data_writer.writerow(Results)
                    dataFile.close()
                    sys.exit()
                else:
                    randList(spanNum, Type)
    if Type == 'Backward':
        corButList.reverse()
        if ButtonList == corButList:
            corRounds += 1
            Results.append('correct')
            if numRounds < 2:
                randList(spanNum, Type)
            elif numRounds == 2:
                spanNum += 1
                corRounds = 0
                numRounds = 0
                if spanNum > 8:
                    with open(directFile() + '\\data\\Corsi_data.csv', mode = 'a') as dataFile:
                        data_writer = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        data_writer.writerow(Results)
                    dataFile.close()
                    sys.exit()
                else:
                    randList(spanNum, Type)
        elif ButtonList!= corButList:
            Results.append('incorrect')
            if numRounds < 2:
                randList(spanNum, Type)
            elif numRounds == 2 and corRounds == 0:
                Results.append(spanNum-1)
                with open(directFile() + '\\data\\Corsi_data.csv', mode = 'a') as dataFile:
                    data_writer = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    data_writer.writerow(Results)
                dataFile.close()
                sys.exit()
            elif numRounds == 2 and corRounds >= 1:
                spanNum += 1
                corRounds = 0
                numRounds = 0
                if spanNum > 8:
                    with open(directFile() + '\\data\\Corsi_data.csv', mode = 'a') as dataFile:
                        data_writer = csv.writer(dataFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        data_writer.writerow(Results)
                    dataFile.close()
                    sys.exit()
                else:
                    randList(spanNum, Type)
            
def ansCheckPrac(rootVal, Type, pracBlock):
    rootVal.destroy()
    global corRounds, spanNum, numRounds
    numRounds += 1
    if Type == 'Forward':
        if ButtonList == corButList:
            corRounds += 1
            if numRounds < 2:
                presFeedback('Correct', spanNum, Type, pracBlock)
            elif numRounds == 2:
                spanNum += 1
                corRounds = 0
                numRounds = 0
                if spanNum == 4:
                    spanNum = 2
                    presFeedback('Correct', spanNum, Type, pracBlock, end = 1)
                else:
                    presFeedback('Correct', spanNum, Type, pracBlock)
        elif ButtonList!= corButList:
            if numRounds < 2:
                presFeedback('Incorrect', spanNum, Type, pracBlock)
            elif numRounds == 2 and corRounds == 0:
                numRounds = 0
                spanNum = 2
                presFeedback('Incorrect', spanNum, Type, pracBlock, end = 1)
            elif numRounds == 2 and corRounds >= 1:
                spanNum += 1
                corRounds = 0
                numRounds = 0
                if spanNum == 4:
                    spanNum = 2
                    presFeedback('Incorrect', spanNum, Type, pracBlock, end = 1)
                else:
                    presFeedback('Incorrect', spanNum, Type, pracBlock)             
    if Type == 'Backward':
        corButList.reverse()
        if ButtonList == corButList:
            corRounds += 1
            if numRounds < 2:
                presFeedback('Correct', spanNum, Type, pracBlock)
            elif numRounds == 2:
                spanNum += 1
                corRounds = 0
                numRounds = 0
                if spanNum == 4:
                    spanNum = 2
                    presFeedback('Correct', spanNum, Type, pracBlock, end = 1)
                else:
                    presFeedback('Correct', spanNum, Type, pracBlock)
        elif ButtonList!= corButList:
            if numRounds < 2:
                presFeedback('Incorrect', spanNum, Type, pracBlock)
            elif numRounds == 2 and corRounds == 0:
                numRounds = 0
                spanNum = 2
                presFeedback('Incorrect', spanNum, Type, pracBlock, end = 1)
            elif numRounds == 2 and corRounds >= 1:
                spanNum += 1
                corRounds = 0
                numRounds = 0
                if spanNum == 4:
                    spanNum = 2
                    presFeedback('Incorrect', spanNum, Type, pracBlock, end = 1)
                else:
                    presFeedback('Incorrect', spanNum, Type, pracBlock)

def randList(numBlocks, Type, pracBlock = 'No'):
    global randomSamp, corButList
    ButtonHolderRefresh()
    if Type == 'Forward':
        corButList = []
        randomSamp = random.sample(range(1, numBlocks + 1), numBlocks)      # get n values
        randomTimes = [x*1000 for x in randomSamp]                          # get time values incremented by 1000ms for n
        blockTime = ['' for x in range(9)]                                  # initialise list of buttons to be displayed at set times
        randomAssign = random.sample(range(0, 9), numBlocks)                # get a random sample of buttons of length n
        n = 0
        for x in randomAssign:
            blockTime[x] = randomTimes[n]                                   # assign time values to the given number of buttons in the trial
            n += 1
    if Type == 'Backward':
        corButList = []
        randomSamp = random.sample(range(1, numBlocks + 1), numBlocks)      # get n values
        randomTimes = [x*1000 for x in randomSamp]                          # get time values incremented by 1000ms for n
        blockTime = ['' for x in range(9)]                                  # initialise list of buttons to be displayed at set times
        randomAssign = random.sample(range(0, 9), numBlocks)                # get a random sample of buttons of length n
        n = 0
        for x in randomAssign:
            blockTime[x] = randomTimes[n]                                   # assign time values to the given number of buttons in the trial
            n += 1
    CorsiBlockDisp(blockTime, Type, pracBlock)

def CorsiBlockDisp(blockTime, Type, pracBlock = 'No'):
    root = tk.Tk()
    root.geometry(str(int(mmToPix*255)) + 'x' + str(int(mmToPix*205)) + '+' + str(int(((1920 - mmToPix * 255) / 2))) + '+' + str(int(((1080 - mmToPix * 205) / 2))))
    f1 = tk.Frame(root, background = 'black')
    f1.pack(fill = 'both', expand = True)
    pixel = tk.PhotoImage(width=1, height=1)
    button1 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    button2 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    button3 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    button4 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    button5 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    button6 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    button7 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    button8 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    button9 = tk.Button(root, text='', image = pixel, width = int(mmToPix*30), height = int(mmToPix*30), compound = 'c', bg = 'blue')
    if pracBlock == 'No':
        button10 = tk.Button(root, text= 'Continue', bg = 'red', command = lambda: ansCheck(root, Type))
    elif pracBlock == 'Yes':
        button10 = tk.Button(root, text= 'Continue', bg = 'red', command = lambda: ansCheckPrac(root, Type, pracBlock))
    button1.place(x = int(mmToPix*130), y = int(mmToPix*20))
    button2.place(x = int(mmToPix*30), y = int(mmToPix*30))
    button3.place(x = int(mmToPix*180), y = int(mmToPix*55))
    button4.place(x = int(mmToPix*70), y = int(mmToPix*65))
    button5.place(x = int(mmToPix*140), y = int(mmToPix*85))
    button6.place(x = int(mmToPix*195), y = int(mmToPix*115))
    button7.place(x = int(mmToPix*15), y = int(mmToPix*125))
    button8.place(x = int(mmToPix*75), y = int(mmToPix*155))
    button9.place(x = int(mmToPix*135), y = int(mmToPix*145))
    try:
        button1.after(blockTime[0], lambda: change_colour(button1, 1))
    except:
        pass
    try:
        button2.after(blockTime[1], lambda: change_colour(button2, 2))
    except:
        pass
    try:
        button3.after(blockTime[2], lambda: change_colour(button3, 3))
    except:
        pass
    try:
        button4.after(blockTime[3], lambda: change_colour(button4, 4))
    except:
        pass
    try:
        button5.after(blockTime[4], lambda: change_colour(button5, 5))
    except:
        pass
    try:
        button6.after(blockTime[5], lambda: change_colour(button6, 6))
    except:
        pass
    try:
        button7.after(blockTime[6], lambda: change_colour(button7, 7))
    except:
        pass
    try:
        button8.after(blockTime[7], lambda: change_colour(button8, 8))
    except:
        pass
    try:
        button9.after(blockTime[8], lambda: change_colour(button9, 9))
    except:
        pass
    button1.after((len(randomSamp)*1000 + 1500), lambda: button1.config(command = lambda: ButtonHolderBuild(1)))
    button2.after((len(randomSamp)*1000 + 1500), lambda: button2.config(command = lambda: ButtonHolderBuild(2)))
    button3.after((len(randomSamp)*1000 + 1500), lambda: button3.config(command = lambda: ButtonHolderBuild(3)))
    button4.after((len(randomSamp)*1000 + 1500), lambda: button4.config(command = lambda: ButtonHolderBuild(4)))
    button5.after((len(randomSamp)*1000 + 1500), lambda: button5.config(command = lambda: ButtonHolderBuild(5)))
    button6.after((len(randomSamp)*1000 + 1500), lambda: button6.config(command = lambda: ButtonHolderBuild(6)))
    button7.after((len(randomSamp)*1000 + 1500), lambda: button7.config(command = lambda: ButtonHolderBuild(7)))
    button8.after((len(randomSamp)*1000 + 1500), lambda: button8.config(command = lambda: ButtonHolderBuild(8)))
    button9.after((len(randomSamp)*1000 + 1500), lambda: button9.config(command = lambda: ButtonHolderBuild(9)))
    button10.after((len(randomSamp)*1000 + 1500), lambda: start_time())
    button10.after((len(randomSamp)*1000 + 1500), lambda: button10.place(x = int(mmToPix*220), y = int(mmToPix*180)))
    root.mainloop()

dirCreate()
start_up()

