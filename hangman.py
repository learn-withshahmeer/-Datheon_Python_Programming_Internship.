# Hangman Game - Task 1
# Run: python hangman.py  (keep words.txt in the same folder)

import random
import os

MAX_WRONG = 6

backup_words = ["python", "hangman", "keyboard", "program", "variable",
                "function", "internet", "computer", "network", "software"]

# ASCII art for 0 to 6 wrong guesses
stages = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========""",
]


def load_words():
    words = []
    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, "words.txt")

    try:
        file = open(path, "r")
        for line in file:
            word = line.strip().lower()
            # use every word from the file (skip 1-2 letter junk like 'c', 'pm')
            if word.isalpha() and len(word) >= 3:
                words.append(word)
        file.close()
    except FileNotFoundError:
        print("words.txt not found, using backup words.")

    if len(words) == 0:
        words = backup_words
    return words


def show_word(secret, guessed):
    # shows letters guessed so far and _ for the rest
    result = ""
    for letter in secret:
        if letter in guessed:
            result += letter.upper() + " "
        else:
            result += "_ "
    return result


def play():
    words = load_words()
    secret = random.choice(words)

    guessed = set()      # all letters tried
    wrong = 0

    print("\n===== HANGMAN =====")
    print("The word has", len(secret), "letters. You get", MAX_WRONG, "mistakes.")

    while wrong < MAX_WRONG:
        print(stages[wrong])
        print("\nWord:", show_word(secret, guessed))
        print("Guessed letters:", " ".join(sorted(guessed)).upper())
        print("Attempts left:", MAX_WRONG - wrong)

        guess = input("\nEnter a letter: ").strip().lower()

        # check input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter only one letter.")
            continue

        # same letter again -> no penalty
        if guess in guessed:
            print("You already tried that letter!")
            continue

        guessed.add(guess)

        if guess in secret:
            print("Correct!")
        else:
            wrong += 1
            print("Wrong!")

        # check win
        won = True
        for letter in secret:
            if letter not in guessed:
                won = False
        if won:
            print("\n*********************************")
            print("  YOU WON! The word was:", secret.upper())
            print("*********************************")
            return

    # loop ended = lost
    print(stages[MAX_WRONG])
    print("\n*********************************")
    print("  GAME OVER! The word was:", secret.upper())
    print("*********************************")


def main():
    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


main()
