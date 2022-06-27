import logging
from autogui import print, input, run, footer
run()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    print("Hi")

    input("I am a button")

    print("2")

    var = input("What is your name?")

    print(f"Hi {var}")

    footer()
