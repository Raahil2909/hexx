from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from string import ascii_letters, digits, punctuation


class Hexx:
    def __init__(self, _root):
        self.root = _root
        self.root.title('Hexx')
        self.root.geometry('800x500')

        self.filename = ''
        self.data = b''

        self.file_menu = Menu(self.root, tearoff=False, activebackground='DodgerBlue')
        self.edit_menu = Menu(self.root, tearoff=False, activebackground='DodgerBlue')
        self.help_menu = Menu(self.root, tearoff=False, activebackground='DodgerBlue')

        self.file_menu.add_command(label='Open File', accelerator='Ctrl+O', command=self.open_file)
        self.file_menu.add_command(label='Save File', accelerator='Ctrl+S', command=self.save_file)
        self.file_menu.add_command(label='Save As', accelerator='Ctrl+Shift+S', command=self.save_file_as)

        self.edit_menu.add_command(label='Cut', accelerator='Ctrl+X', command=self.cut_text)
        self.edit_menu.add_command(label='Copy', accelerator='Ctrl+C', command=self.copy_text)
        self.edit_menu.add_command(label='Paste', accelerator='Ctrl+V', command=self.paste_text)
        self.help_menu.add_command(label='About', accelerator='Ctrl+H', command=self.about_hexx)

        self.menu_bar = Menu(self.root)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)

        self.main_window = PanedWindow(self.root)
        self.main_window.pack(fill=BOTH, expand=1)

        self.addr_area = Text(self.main_window, relief=GROOVE, width=11, wrap=NONE, fg='#00ff00', bg='black')
        self.hex_area = Text(self.main_window, relief=GROOVE, width=40, wrap=NONE, fg='#00ff00', bg='black')
        self.ascii_area = Text(self.main_window, relief=GROOVE, width=17, wrap=NONE, fg='#00ff00', bg='black')
        self.analysis_area = Text(self.main_window, relief=GROOVE, wrap=NONE, fg='#00ff00', bg='black')

        self.main_window.add(self.addr_area)
        self.main_window.add(self.hex_area)
        self.main_window.add(self.ascii_area)
        self.main_window.add(self.analysis_area)

        self.root.config(menu=self.menu_bar)

        self.shortcuts()

    def show_formatted(self):
        self.addr_area.delete(1.0, END)
        self.hex_area.delete(1.0, END)
        self.ascii_area.delete(1.0, END)

        addr_data = f'0x{0:0{8}x}\n'
        hex_data = ''
        ascii_data = ''

        cnt = 0
        for c in self.data:
            cnt += 1
            hex_data += f'{c:0{2}x}'
            if chr(c) in ascii_letters+punctuation+digits:
                ascii_data += chr(c)
            else:
                ascii_data += '.'

            if cnt & 1 == 0:
                hex_data += ' '

            if cnt % 16 == 0:
                addr_data += f'0x{cnt:0{8}x}\n'
                ascii_data += '\n'
                hex_data += '\n'

        self.addr_area.insert(1.0, addr_data)
        self.hex_area.insert(1.0, hex_data)
        self.ascii_area.insert(1.0, ascii_data)

    def extract_data(self):
        tmp = self.hex_area.get(1.0, END)
        ftmp = b''
        for c in tmp.split():
            ftmp += (int(c[:2], 16)).to_bytes(1, byteorder='little')
            if len(c) == 4:
                ftmp += (int(c[2:], 16)).to_bytes(1, byteorder='little')
        self.data = ftmp
        pass

    def open_file(self, *args):
        self.filename = fd.askopenfilename(title='Select File')
        if self.filename != '':
            self.root.title(f'Hexx - {self.filename}')
            with open(self.filename, 'rb') as f:
                self.data = f.read()
                self.show_formatted()
                f.close()

    def save_file(self, *args):
        if self.filename == '':
            self.save_file_as()
        else:
            self.extract_data()
            with open(self.filename , 'wb') as f:
                f.write(self.data)
                f.close()
                mb.showinfo('Saved', '[+] Successfully saved the file')
                self.show_formatted()

    def save_file_as(self, *args):
        self.filename = fd.asksaveasfilename(title='Hehe')
        self.save_file()

    def cut_text(self, *args):
        self.hex_area.event_generate('<<Cut>>')

    def copy_text(self, *args):
        self.hex_area.event_generate('<<Copy>>')

    def paste_text(self, *args):
        self.hex_area.event_generate('<<Paste>>')

    def about_hexx(self, *args):
        mb.showinfo('Info', 'This is a hex editor created by Raahil')

    def shortcuts(self):
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-d>", self.save_file_as)
        self.root.bind("<Control-x>", self.cut_text)
        self.root.bind("<Control-c>", self.copy_text)
        self.root.bind("<Control-p>", self.paste_text)
        self.root.bind("<Control-h>", self.about_hexx)


root = Tk()
Hexx(root)
root.mainloop()
