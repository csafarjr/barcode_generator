import os
from tkinter import StringVar, filedialog, Frame, Button, Menu, Entry, Label, Tk, BOTH
from reportlab.graphics.barcode import code39
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from barcode.codex import Code39
from barcode.writer import PNGWriter


### Setup ###
label_size = (inch*(2+(5/8)), inch)
width, height = letter
font_name = 'Helvetica'
font_size = 12
start_w = 35
start_h = 50
step_w = 198
step_h = 72
label_pos = [
            [[start_w, height-start_h], [start_w+step_w, height-start_h], [start_w+step_w*2, height-start_h]],                             # row 1
            [[start_w, height-start_h-step_h], [start_w+step_w, height-start_h-step_h], [start_w+step_w*2, height-start_h-step_h]],        # row 2
            [[start_w, height-start_h-step_h*2], [start_w+step_w, height-start_h-step_h*2], [start_w+step_w*2, height-start_h-step_h*2]],  # row 3
            [[start_w, height-start_h-step_h*3], [start_w+step_w, height-start_h-step_h*3], [start_w+step_w*2, height-start_h-step_h*3]],  # row 4
            [[start_w, height-start_h-step_h*4], [start_w+step_w, height-start_h-step_h*4], [start_w+step_w*2, height-start_h-step_h*4]],  # row 5
            [[start_w, height-start_h-step_h*5], [start_w+step_w, height-start_h-step_h*5], [start_w+step_w*2, height-start_h-step_h*5]],  # row 6
            [[start_w, height-start_h-step_h*6], [start_w+step_w, height-start_h-step_h*6], [start_w+step_w*2, height-start_h-step_h*6]],  # row 7
            [[start_w, height-start_h-step_h*7], [start_w+step_w, height-start_h-step_h*7], [start_w+step_w*2, height-start_h-step_h*7]],  # row 8
            [[start_w, height-start_h-step_h*8], [start_w+step_w, height-start_h-step_h*8], [start_w+step_w*2, height-start_h-step_h*8]],  # row 9
            [[start_w, height-start_h-step_h*9], [start_w+step_w, height-start_h-step_h*9], [start_w+step_w*2, height-start_h-step_h*9]],  # row 10
            ] 
canvas = canvas.Canvas('barcodes.pdf', pagesize=letter)
canvas.setFont(font_name, font_size)
all_files = []
#############
class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.master = master
        self.rows = 10
        self.cols = 3
        self.entries = []
        self.entrytexts = {}
        self.empty = [None, '', ' ', 0]
        self.header = ''
        self.init_window()
        global all_files
        
    def init_window(self):
        self.master.title('Barcode Generator')
        self.grid()
        self.header_ent = Entry(self.master)
        self.header_ent.focus()
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_separator()
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)
        header_lbl = Label(self.master, text='Label Header').grid(row=0, column=0)
        self.header_ent.columnconfigure(2, weight=2)
        self.header_ent.grid(row=0, column=1, columnspan=2, sticky='NESW')
        for r in range(self.rows):
            self.entries.append([])
            for c in range(self.cols):
                self.entrytexts[f'r{r}c{c}'] = StringVar()
                ent = Entry(self.master, textvariable=self.entrytexts[f'r{r}c{c}'])
                self.entries[r].append(ent)
                ent.grid(row=r+1, column=c, padx=5, pady=5)
        finish_btn = Button(self.master, text='Open', command=self.generate_barcodes)
        finish_btn.grid(row=11, column=2, padx=5, pady=5)
    
    def generate_barcodes(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.entries[r][c].get() not in self.empty:
                    self.generate_code39(canvas, label_pos[r][c], self.entries[r][c].get())
        canvas.save()
        self.open_pdf()
        self.client_exit()
            
    def open_pdf(self):
        try:
            os.system('start barcodes.pdf')
        except Exception as e:
            print(f'Error: {e}')
    
    def client_exit(self):
        self.master.destroy()
      
    def generate_code39(self, c, xy, data):
        ''' 
        Generates a barcode based on 'data'
        Saves the barcode as a png to local folder
        '''
        spacer = 55
        code39 = Code39(data, writer=PNGWriter(), add_checksum=False)
        filename = code39.save(f'.\\{data}')
        self.header = self.header_ent.get()
        if stringWidth(self.header, font_name, font_size) > 150:
            offset = -5
        else:
            offset = 150 / 2 - stringWidth(self.header, font_name, font_size) / 2
        c.drawString(xy[0] + offset, xy[1], self.header)
        c.drawImage(filename, xy[0]-8, xy[1]-spacer, width=2.2*inch, height=0.7*inch)
        all_files.append(filename)

        
def remove_file(filename):
    ''' 
    Removes generated barcode file. 
    '''
    deleted = False
    while not deleted:
        try:
            os.remove(f'{filename}')
        except:
            pass
        
        deleted = True
        
def cleanup():
    for file in all_files:
        remove_file(file)

if __name__ == '__main__':      
    root = Tk()
    root.resizable(0,0)
    root.geometry(f'{405}x{378}')
    root.iconbitmap('icon.ico')
    app = Window(root)
    root.mainloop()
    cleanup()
