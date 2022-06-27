"""
Generate dynamic TKinter GUI from executing Python __script__.
"""

import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
import threading
from inspect import currentframe
import re
from functools import partial
import asynctkinter as at
from tkfontawesome import icon_to_image
from queue import Queue
import logging
import sys
import os
import csv
import subprocess
from PIL import Image
import io


def get_file_script():
    """
    Get the __script__ from the file.
    """
    # get __script__ text
    script = []
    for line in open(sys.argv[0], 'r'):
        script.append(line.strip().split())

    return script


__threadsafe_queue_tk__ = Queue()
__threadsafe_queue_io__ = Queue()
__script__ = get_file_script()
__input_log__ = []
__autogui__ = None

at.patch_unbind()


def change_theme(root, theme_button, event):
    # NOTE: The theme's real name is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
        light_icon = icon_to_image("sun", fill="#fff", scale_to_width=64)
        theme_button.configure(image=light_icon)
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")
        dark_icon = icon_to_image("moon", fill="#000", scale_to_width=64)
        theme_button.configure(image=dark_icon)


def threadsafe_print(text, end, frame):
    """
    Print text in the tkinter gui.
    """
    if text == "" or text == "\n":
        # label as spacer
        widget = tk.Label(frame, text="-----------", padx=2, pady=2)
    else:
        # label as text
        widget = tk.Label(frame, text=text, padx=2, pady=2)

    widget.pack(padx=5, pady=5)


def threadsafe_input(text, match, frame):
    """
    Get text input from tkinter gui if this function assigns output to a variable, else display a button with the text.
    """

    def disable(widget):
        # disable widget
        widget.configure(state="disabled")
        widget.unbind("<Return>")

    def callback_button(button_widget):
        disable(button_widget)

        __threadsafe_queue_io__.put(True)   # put positive Boolean on io queue

    def callback_textinput(text_widget, button_widget, prompt=""):
        disable(text_widget)
        disable(button_widget)

        text = text_widget.get()   # get text from Entry widget

        __threadsafe_queue_io__.put(text)   # put user input on io queue
        __input_log__.append([prompt, text])  # add user input to log

    if match == True:
        # row for input and button
        row = tk.Frame(frame)
        row.pack(padx=5, pady=5)

        #  input box
        text_widget = tk.Entry(row)
        text_widget.insert(0, text)
        text_widget.configure(width=len(text)+4)
        text_widget.grid(row=0, column=0, padx=5, pady=5)

        #  button
        button_widget = tk.Button(row, text="Enter", padx=5, pady=5)

        # set button command
        button_widget.configure(command=partial(
            callback_textinput, text_widget, button_widget, prompt=text))

        # set button callback on enter key
        button_widget.bind("<Return>", lambda event: partial(
            callback_textinput, text_widget, button_widget, prompt=text))

        button_widget.grid(row=0, column=1, padx=5, pady=5)

    else:
        #  button
        button_widget = tk.Button(frame, text=text, padx=5, pady=5)

        # set button command
        button_widget.configure(command=partial(
            callback_button, button_widget))

        # set button callback on enter key
        button_widget.bind("<Return>", lambda event: partial(
            callback_button, button_widget))
        button_widget.pack(padx=5, pady=5)


def main(theme_name, theme_source):
    """
    Create a rezizeable Tkinter Gui styled as a blank PDF
    """

    # init window
    root = tk.Tk()
    root.title("Tkinter GUI")
    root.geometry("800x600")
    root.resizable(True, True)

    root.protocol("WM_DELETE_WINDOW", threadsafe_exit)  # set exit callback

    # check "themes/azure.tcl" exists relative to current directory
    if os.path.isfile(theme_source):
        logging.info("Loading Azure theme")
        # set initial theme
        root.tk.call("source", theme_source)
        root.tk.call("set_theme", theme_name)
    else:
        logging.info("Azure theme not found, using default theme")

    # add light/dark mode toggle
    # light_icon = icon_to_image("sun", fill="#fff", scale_to_width=32)
    #theme_button = tk.Button(root, image=light_icon)
    #theme_button.configure(command=partial(change_theme, root, theme_button))
    #theme_button.pack(padx=5, pady=5)

    # make it scrollable
    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = tk.Canvas(root, width=800, height=600,
                       yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=canvas.yview)

    # add a frame to the canvas
    frame = tk.Frame(canvas, width=800, height=600)
    canvas.create_window((0, 0), window=frame, anchor='center')

    # return root to enter mainloop
    dynamic_mainloop(root, canvas, frame)


def dynamic_mainloop(root, canvas, frame):
    """
    Run mainloop, with handling of thread-safe queue calls for input and print functions.
    """

    # run mainloop
    while True:
        # get next item from thread-safe queue if exists
        if __threadsafe_queue_tk__.qsize() > 0:
            item = __threadsafe_queue_tk__.get()

            # handle item
            if item[0] == "print":
                # pass text, end(line end char), frame
                threadsafe_print(item[1], item[2], frame)
            elif item[0] == "input":
                # pass text, match(button/textbox), frame
                threadsafe_input(item[1], item[2], frame)
            elif item[0] == "exit":
                # exit mainloop
                root.destroy()
                break
            elif item[0] == "footer":
                # render footer with options to export/quit
                threadsafe_footer(frame, canvas)

        # update gui
        root.update()
        canvas.configure(scrollregion=canvas.bbox("all"))


def run(theme_name="light", theme_source="themes/azure.tcl"):
    """
    Run the tkinter gui in a thread.
    """
    def tkinter_thread(theme_name, theme_source):
        main(theme_name, theme_source)

    __autogui__ = threading.Thread(target=tkinter_thread, args=(theme_name, theme_source,))
    __autogui__.start()


def threadsafe_footer(frame, canvas):
    """
    Render page footer, with options to export to CSV, PDF or quit applicaiton.
    """

    # function to push quit command to thread-safe queue
    def quit():
        __threadsafe_queue_tk__.put(("exit",))

    # function to save __input_log__ to csv
    def save_csv():
        # get file name
        file_name = tkinter.filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")])

        # write list items to csv
        with open(file_name, "w") as f:
            writer = csv.writer(f)
            writer.writerows(__input_log__)

    # function to save canvas to pdf
    def save_pdf():
        # get file name
        file_name = tkinter.filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])

        temp_file_name = file_name + ".ps"

        # save canvas to pdf
        canvas.update()
        canvas.postscript(file=temp_file_name, colormode='color')
        process = subprocess.Popen(["ps2pdf", temp_file_name, file_name], shell=True)
        process.wait()
        os.remove(temp_file_name)

    
    def screenshot():
        # get file name
        file_name = tkinter.filedialog.asksaveasfilename(
            defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])

        # save canvas to pdf
        canvas.update()
        ps = canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(file_name, 'jpeg')

    # create row for footer
    row = tk.Frame(frame)
    row.pack(padx=5, pady=5)

    #  export to csv button
    export_csv_button = tk.Button(row, text="Export to CSV", padx=5, pady=5)
    export_csv_button.configure(command=save_csv)
    export_csv_button.grid(row=0, column=0, padx=5, pady=5)

    #  export to pdf button
    export_pdf_button = tk.Button(row, text="Export to PDF", padx=5, pady=5)
    export_pdf_button.configure(command=save_pdf)
    export_pdf_button.grid(row=0, column=1, padx=5, pady=5)

    #  screen shot button
    screen_shot_button = tk.Button(row, text="Screen Shot", padx=5, pady=5)
    screen_shot_button.configure(command=screenshot)
    screen_shot_button.grid(row=0, column=2, padx=5, pady=5)

    # disable pdf and screenshot buttons
    export_pdf_button.configure(state="disabled")
    screen_shot_button.configure(state="disabled")

    #  quit button
    quit_button = tk.Button(row, text="Quit", padx=5, pady=5)
    quit_button.configure(command=quit)
    quit_button.grid(row=0, column=3, padx=5, pady=5)


def threadsafe_exit():
    """
    Exit the application.
    """
    __threadsafe_queue_tk__.put(("exit",))