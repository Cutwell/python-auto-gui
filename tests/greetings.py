import logging
from pythonautogui import print, input, run, footer
run()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    var = input("What is your name?")

    print(f"Hi {var}")

    footer()
