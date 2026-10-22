# Hangman Word Guessing Game (Console)

A terminal-based Hangman game written in Python 3 using only the standard library.

## Features
- Random word picked from `words.txt` (falls back to built-in words if the file is missing)
- 6 wrong attempts allowed
- ASCII gallows art that updates after every wrong guess
- Shows the masked word (e.g. `_ A _ H E O N`) and all guessed letters
- Repeated guesses do not cost an attempt
- Win / game over screens and a play-again option

## How to run
1. Install Python 3
2. Keep `hangman.py` and `words.txt` in the same folder
3. Run:

```
python hangman.py
```

## Files
| File | Description |
|------|-------------|
| `hangman.py` | The game |
| `words.txt` | English word list (one word per line) |

## Concepts used
String manipulation, loops, sets, functions, file handling, `random.choice()`, input validation.
