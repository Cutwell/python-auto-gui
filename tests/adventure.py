import logging
import random
from pythonautogui import print, input, run, clear
run()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    characters = ["an adventurer", "a wizard", "a princess", "a tax collector"]

    # random character
    pov = characters[random.randint(0, len(characters) - 1)]

    while 1:
        
        print(f"You are {pov}. You are in a dark room. There is a door to your right and left.")
        print("Enter left / right to choose.")

        while 1:
            choice = input("Which door do you take?")

            if choice == "left" or choice == "right":
                break
            else:
                print("Please enter left or right.")
                continue

        if choice == "left":
            print("You have chosen left.")

            print("The door leads to stairs. You can go up or down.")

            print("Enter up / down to choose.")

            while 1:
                choice = input("Which stairs do you take?")

                if choice == "up" or choice == "down":
                    break
                else:
                    print("Please enter up or down.")
                    continue

            if choice == "up":
                print("You have chosen up.")
            
                print("You are in a room with a table. There is a chair by the table. There is a book on the chair.")

                pov = characters[random.randint(0, len(characters) - 1)]
                print(f"The book is a story about {pov}..")

                input("Press here to read the book.")

                clear()

            elif choice == "down":
                print("You have chosen down.")

                print("You are in a room with a table. There is a chair by the table. There is a book on the chair.")

                pov = characters[random.randint(0, len(characters) - 1)]
                print(f"The book is a story about {pov}..")

                input("Press here to read the book.")

                clear()

        elif choice == "right":
            print("You have chosen right.")

            print("The door leads to a room with a bed. There is a book on the bed.")

            pov = characters[random.randint(0, len(characters) - 1)]
            print(f"The book is a story about {pov}..")

            input("Press here to read the book.")

            clear()
        