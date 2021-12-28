#!/usr/bin/python3
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from math import ceil
from string import ascii_letters, digits, punctuation

### Global vars ###
fileName = ''

### Create the window ####
root = Tk()
root.title('HexEdit')
root.geometry('800x500')


### Create components ###
menuBar = Menu(root)


### imp functions ###
def openNewFile(event=1):
    pass


def formatData(data):
    hexData = ''
    ascii = ''
    cnt = 0
    for c in data:
        # print(f'{c:0{2}x}', end='.')
        cnt += 1
        hexData += f'{c:0{2}x}'
        if chr(c) in ascii_letters+punctuation+digits:
            ascii += chr(c)
        else:
            ascii += '.'
        if cnt % 16 == 0:
            ascii += ' '

        if cnt & 1 == 0:
            hexData += ' '

    addr = ''
    x = 0
    for i in range(ceil(cnt/16)):
        addr += f'0x{x:0{8}x} '
        x += 0x10

    hexArea.insert(1.0, hexData)
    addrArea.insert(1.0, addr)
    asciiArea.insert(1.0, ascii)


def openBinaryFile(event=1):
    global fileName
    fileName = fd.askopenfilename(title='Select File')
    if str(fileName) != '()' or fileName != '':
        root.title(f'HexEdit - {fileName}')
        hexArea.delete(1.0, END)
        with open(fileName, 'rb') as file:
            data = file.read()
            formatData(data)
            file.close()
    else:
        fileName = ''
        print('[-] no file name found')

def openFile(event=1):
    global fileName
    fileName = fd.askopenfilename(title='Select File')
    print(f'{fileName=}, {type(fileName)}')
    print(f'{str(fileName)}')
    if str(fileName) != '()' or fileName != '':
        root.title(f'HexEdit - {fileName}')
        hexArea.delete(1.0, END)
        with open(fileName, 'r') as file:
            hexArea.insert(1.0, file.read())
            file.close()
    else:
        fileName = ''
        print('[-] no file name found')


def saveFile(event=1):
    global fileName
    if fileName == '':
        fileName = fd.asksaveasfilename(title='Select folder')
        # print(fileName)

    fp = open(fileName, 'w')
    # print(textArea.get(1.0, END))
    # print('----------')
    fp.write(hexArea.get(1.0, END))
    fp.close()
    mb.showinfo('Success', '[+] File successfully saved')


def saveFileAs(event=1):
    fileName = fd.asksaveasfilename(title='Save File As', filetypes=[('All', '*.*')])
    fp = open(fileName, 'w')
    fp.write(hexArea.get(1.0, END))
    fp.close()
    root.title(f'HexEdit - {fileName}')
    mb.showinfo('Success', '[+] File successfully saved')


def copyText(event=1):
    hexArea.event_generate('<<Copy>>')


def cutText(event=1):
    hexArea.event_generate('<<Cut>>')


def pasteText(event=1):
    hexArea.event_generate('<<Paste>>')


def selectAllText(event=1):
    pass
    # textArea.event_generate('<<Control->>')


def aboutHexedit(event=1):
    mb.showinfo('Info', 'This is a hex editor created by Raahil')


### menus ###
editMenu = Menu(menuBar, tearoff=False, activebackground='DodgerBlue')
fileMenu = Menu(menuBar, tearoff=False, activebackground='DodgerBlue')
helpMenu = Menu(menuBar, tearoff=False, activebackground='DodgerBlue')

fileMenu.add_command(label="New File", accelerator="Ctrl+N", command=openNewFile)
fileMenu.add_command(label="Open File", accelerator="Ctrl+O", command=openFile)
fileMenu.add_command(label="Open Binary File", accelerator="Ctrl+B", command=openBinaryFile)
fileMenu.add_command(label="Save File", accelerator="Ctrl+S", command=saveFile)
fileMenu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=saveFileAs)

editMenu.add_command(label="Copy", accelerator="Ctrl+C", command=copyText)
editMenu.add_command(label="Cut", accelerator="Ctrl+X", command=cutText)
editMenu.add_command(label="Paste", accelerator="Ctrl+V", command=pasteText)
editMenu.add_command(label="Select All", accelerator="Ctrl+A", command=selectAllText)

helpMenu.add_command(label="About HexEdit", accelerator="Ctrl+H", command=aboutHexedit)


### Add submenus ###
menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Edit", menu=editMenu)
menuBar.add_cascade(label='Help', menu=helpMenu)

mainW = PanedWindow(root)
mainW.pack(fill=BOTH, expand=1)


# scroll_y = Scrollbar(mainW, orient=VERTICAL, width=1)
hexArea = Text(mainW, relief=GROOVE, width=40)
asciiArea = Text(mainW, relief=GROOVE, width=17)
addrArea = Text(mainW, relief=GROOVE, width=11)
extraArea = Text(mainW, relief=GROOVE)

mainW.add(addrArea)
mainW.add(hexArea)
mainW.add(asciiArea)
mainW.add(extraArea)
# mainW.add(scroll_y)

# textArea.pack(side=LEFT, fill=Y, expand=1)
# textArea2.pack(side=RIGHT, fill=Y, expand=1)
# scroll_y.pack(side=LEFT, fill=Y)


### Shortcuts ###
root.bind('<Control-o>', openFile)
root.bind('<Control-n>', openNewFile)
root.bind('<Control-s>', saveFile)
root.bind('<Control-Shift-s>', saveFileAs)
root.bind('<Control-x>', cutText)
root.bind('<Control-c>', copyText)
root.bind('<Control-p>', pasteText)
root.bind('<Control-h>', aboutHexedit)
# textArea.bind('<Control->',)
# textArea.bind('<Control->',)
# textArea.bind('<Control->',)
# textArea.bind('<Control->',)


### render everything and inf loop ###
root.config(menu=menuBar)
# root.update() ## what does this do ????
root.mainloop()
