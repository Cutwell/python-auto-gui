# Python-Pyre
---
_Generate a TkInter GUI from any Python program using Pyre_

 - Creates a TkInter GUI to replace any command line interface
 - Interprets your existing code, removing the need for programming a GUI by hand.
 - Capable of being integrated with any existing Python (3.5+) code

Python-Pyre is a Python Library built to generate simple GUI's for applications.
It can take absolutely any user-orientated Python Program and produce tidy applications.

### Quick-start
---
```python
from pyre import *
Pyre()
```
This will override any input() or print() functions used in the program to create a GUI

### 10 Second Example
---
Get up and running with basics of Pyre using this simple example:
```python
from pyre import *
Pyre()

myAnswer = input("What is your name? >")

input("press anywhere to continue")

print("Hello, "+myAnswer)
```


### Quick Reference
---
(_for more in-depth explanations, etc., read the docs._)

| Setup               | Command                                      |
| :-----------------: | :------------------------------------------: |
| install from pip    | ```bash $ pip3 install pyre```               |
---
| Function            | New Function                                                |
| :-----------------: | :---------------------------------------------------------: |
| ```input()```       | Creates a button and waits for the user to press it         |
| ```var = input()``` | Creates a text box and waits for the user to enter an input |
| ```print()```       | Creates a label with the passed text                        |

### Compatibility and Notes
---
Pyre is not system-specific, and should work on Windows and Unix systems (including Apple OS).

Pyre's compatibility with different modules can vary - if a particular module doesn't work well with Pyre, report it in Issues or contribute a fix to improve the project.

Pyre uses TkInter, and as such programs that already make use of TkInter may not work together well. All of Pyres global variables use the pyre_ prefix to prevent logic errors, meaning that it is possible to use Pyre to generate GUI interfaces that may have previously been confined to the command line.
When incorporating Pyre into your programs, be aware that print() and input() are both overridden by the library - but you can print to the console using the sys library:
```python
import sys
sys.stdout.write("writes to console")
```

Be aware that the TkInter GUI will only update while print() or input() is being called (due to issues with concurrency and TkInter). For this reason, your GUI will hang during periods of inactivity (e.g.: during long computations or while the program is sleeping).
