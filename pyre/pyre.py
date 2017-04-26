#  Python-Pyre

import tkinter as tk
from inspect import currentframe
import re
import os
import sys
import __main__


def Pyre(background="white", foreground="black"):

    global pyre_root, pyre_bg, pyre_fg, pyre_script, pyre_objects

    pyre_bg, pyre_fg = background, foreground

    pyre_root = tk.Tk()

    pyre_root.title(os.path.basename(__main__.__file__))
    pyre_root.minsize(width=200, height=200)
    pyre_root.configure(background=pyre_bg)

    pyre_script = []
    for line in open(__main__.__file__, 'r'):
        pyre_script.append(line.strip().split())

    pyre_objects = []
    pyre_root.update()


def print(text):
    pyre_objects.insert(0, tk.Label(pyre_root, text=text, bg=pyre_bg, fg=pyre_fg, padx=2, pady=2))
    pyre_objects[0].pack(padx=5, pady=5)
    pyre_root.update()
    return

def input(text):
    cf = currentframe()
    lineno = cf.f_back.f_lineno

    line = pyre_script[lineno-1]    #  (-1 bc zero based index)

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
        pyre_objects.insert(0, tk.Entry(pyre_root, bg=pyre_bg, fg=pyre_fg))
        pyre_objects[0].insert(0, text)
        pyre_objects[0].configure(width=len(text)+4)

    else:
        #  button
        pyre_objects.insert(0, tk.Button(pyre_root, text=text, command=callback, padx=5, pady=5, bg=pyre_bg, fg=pyre_fg))

    pyre_objects[0].pack(padx=5, pady=5)
    pyre_objects[0].bind("<Return>", lambda event: callback())

    global pyre_breakout
    pyre_breakout = False
    default_cleared = False
    while pyre_breakout == False:
        try:
            pyre_root.update()
            if pyre_root.focus_get() == pyre_objects[0] and default_cleared == False:
                default_cleared = True
                pyre_objects[0].delete(0, len(text))
        except:
            sys.exit()    #  clean exit if user closes the window while in loop
    #  disable button and keybind
    pyre_objects[0].configure(state="disabled")
    pyre_objects[0].unbind("<Return>")
    pyre_root.update()

    try:
        return str(pyre_objects[0].get())
    except:
        return ""



if __name__ == "__main__":
    Pyre()

    name = input("What is your name?")

    input("Click me")

    print("Hello "+name)
