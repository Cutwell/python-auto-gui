"""
Override IO functions to display in Tkinter GUI.
"""

import logging
from inspect import currentframe
import re
from autogui.internals import __script__, __threadsafe_queue_io__, __threadsafe_queue_tk__, run


def print(text, end="\n"):
    """
    Override the print function to display in the tkinter gui.
    Add print call to threadsafe queue.
    """
    logging.debug(f"print: {text}")

    # add print call to thread-safe queue
    __threadsafe_queue_tk__.put(("print", text, end))


def input(text=""):
    """
    Override the input function to get input from the tkinter gui.
    Add input call to threadsafe queue.
    """
    logging.debug(f"input prompt: {text}")

    # traceback to get the line number of the input function
    cf = currentframe()
    lineno = cf.f_back.f_lineno

    # locate __script__ line
    line = __script__[lineno-1]

    # check if the line is a variable assignment
    match = False
    for index in range(len(line)):

        if re.search(r'(input)', line[index]) != None:

            if line[index-1] == []:
                sub = 2
            else:
                sub = 1

            # check if the line is a variable assignment
            if re.search(r'(=)', line[index-sub]) != None or re.search(r'=', line[index]) != None:
                match = True
                break

    # add input call to thread-safe queue
    __threadsafe_queue_tk__.put(("input", text, match))

    def input_blocker():
        # await input from thread-safe queue
        while __threadsafe_queue_io__.qsize() == 0:
            pass

        # get input from thread-safe queue
        item = __threadsafe_queue_io__.get()

        return item

    output = input_blocker()

    return output

def exit():
    """
    Override the exit function to exit the tkinter gui.
    Add exit call to threadsafe queue.
    """
    logging.debug("exit")

    # add exit call to thread-safe queue
    __threadsafe_queue_tk__.put(("exit",))

def footer():
    """
    Push footer request to threadsafe queue.
    """
    logging.debug("footer")

    # add footer call to thread-safe queue
    __threadsafe_queue_tk__.put(("footer",))