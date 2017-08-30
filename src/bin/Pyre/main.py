#  Python-Pyre

import tkinter as tk
from inspect import currentframe
import re
import os
import sys
import __main__

def Pyre(background="white", foreground="black"):

    global pyre_root, pyre_bg, pyre_fg, pyre_script, pyre_objects, pyre_y, pyre_canvas, pyre_frame, pyre_scrollbar

    pyre_bg, pyre_fg = background, foreground
    pyre_y = 0

    pyre_root = tk.Tk()

    pyre_root.title(os.path.basename(__main__.__file__))
    pyre_root.configure(background=pyre_bg)
    pyre_root.geometry("300x300")

    pyre_script = []
    for line in open(__main__.__file__, 'r'):
        pyre_script.append(line.strip().split())

    pyre_objects = []

    pyre_canvas = tk.Canvas(pyre_root, bd=0, bg=pyre_bg, highlightthickness=0, relief='ridge')
    pyre_canvas.pack(side="left", expand="yes")

    pyre_scrollbar = tk.Scrollbar(pyre_root, command=pyre_canvas.yview)
    pyre_scrollbar.pack(side="left", fill='y')

    pyre_canvas.configure(yscrollcommand=pyre_scrollbar.set)

    pyre_frame = tk.Frame(pyre_canvas, bg=pyre_bg, bd=0, relief="flat")
    pyre_canvas.create_window((0,0), window=pyre_frame, anchor='nw')

    #  binding for Linux
    pyre_canvas.bind("<Button-4>", pyre_mouseUpdate)
    pyre_canvas.bind("<Button-5>", pyre_mouseUpdate)
    
    #  binding for Mac OS and Windows
    pyre_canvas.bind("<MouseWheel>", pyre_mouseUpdate)

    pyre_canvas.bind("<Configure>", pyre_frameUpdate)

    pyre_root.update()

def pyre_mouseUpdate(event):
    global pyre_canvas, pyre_scrollbar
    if event.delta == -120:
        pyre_canvas.yview_scroll(10, "units")
    if event.delta == 120:
        pyre_canvas.yview_scroll(-10, "units")

def pyre_frameUpdate(*args):
    global pyre_frame, pyre_canvas, pyre_scrollbar
    width = pyre_root.winfo_width()-pyre_scrollbar.winfo_width()-1
    pyre_canvas.config(height=pyre_root.winfo_height(), width=width)
    pyre_canvas.configure(scrollregion=pyre_canvas.bbox("all"))
    pyre_canvas.move(pyre_frame, 0, 0)

def print(text=""):
    global pyre_root, pyre_bg, pyre_fg, pyre_script, pyre_objects, pyre_y, pyre_canvas, pyre_frame
    pyre_objects.insert(0, tk.Label(pyre_frame, text=text, bg=pyre_bg, fg=pyre_fg, padx=2, pady=2, font=("Courier New", 11)))
    pyre_objects[0].grid(row=pyre_y, column=0, sticky="w", padx=5, pady=5)
    pyre_y += 1
    pyre_root.update()
    pyre_canvas.configure(scrollregion=pyre_canvas.bbox("all"))
    return

def input(text=""):
    global pyre_root, pyre_bg, pyre_fg, pyre_script, pyre_objects, pyre_y, pyre_canvas, pyre_frame
    cf = currentframe()
    lineno = cf.f_back.f_lineno

    line = pyre_script[lineno-1]    #  (-1 bc zero based index in pyre_script, but not from cf.f_back.f_lineno)

    for index in range(len(line)):

        if re.search(r'(input)', line[index]) != None:

            if line[index-1] == []:
                sub = 2
            else:
                sub = 1

            if re.search(r'(=)', line[index-sub]) != None or re.search(r'=', line[index]) != None:
                match = True

    try:
        if match == True:
            pass
    except:
        match = False

    def callback():
        global pyre_breakout
        pyre_breakout = True

    if match == True:
        #  input box
        pyre_objects.insert(0, tk.Entry(pyre_frame, bg=pyre_bg, fg=pyre_fg, font=("Courier New", 11)))
        pyre_objects[0].insert(0, text)
        pyre_objects[0].configure(width=len(text)+4)

    else:
        #  button
        pyre_objects.insert(0, tk.Button(pyre_frame, text=text, command=callback, padx=5, pady=5, bg=pyre_bg, fg=pyre_fg, font=("Courier New", 11)))

    pyre_objects[0].grid(row=pyre_y, column=0, sticky="w", padx=5, pady=5)
    pyre_y += 1
    pyre_objects[0].bind("<Return>", lambda event: callback())

    global pyre_breakout
    pyre_breakout, default_cleared = False, False
    while pyre_breakout == False:
        try:
            pyre_root.update()
            pyre_canvas.configure(scrollregion=pyre_canvas.bbox("all"))
            if pyre_root.focus_get() == pyre_objects[0] and default_cleared == False:
                default_cleared = True
                pyre_objects[0].delete(0, len(text))
        except:
            sys.exit()    #  clean exit if user closes the window while in loop
    #  disable button and keybind
    pyre_objects[0].configure(state="disabled")
    pyre_objects[0].unbind("<Return>")
    pyre_root.update()
    pyre_canvas.configure(scrollregion=pyre_canvas.bbox("all"))
    

    try:
        return str(pyre_objects[0].get())
    except:
        return ""


if __name__ == "__main__":
    Pyre()

    name = input("What is your name?")

    input("Click me")

    print("Hello "+name)
