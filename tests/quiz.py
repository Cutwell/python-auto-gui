import logging
from pythonautogui import print, input, run, footer
run()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    print("This is a simple maths quiz.")

    input("Press here to start.")

    questions = ["What is 1 + 1?", "What is 2 + 2?", "What is 3 + 3?"]
    answers = ["2", "4", "6"]
    score = 0

    for question in questions:
        print(question)
        answer = input("Answer: ")
        if answer == answers[questions.index(question)]:
            print("Correct!")
            score += 1
        else:
            print("Incorrect!")

    print()

    print(f"You scored {score} out of {len(questions)}.")

    footer()
