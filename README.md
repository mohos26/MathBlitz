# MathBlitz

MathBlitz is a terminal-based mental-math trainer. Solve randomly generated
arithmetic questions, practice recalling stored values, and track your score
during each session.

## Requirements

- Python 3.8 or newer

The game uses only the Python standard library.

## Run

From the project directory, start a game with:

```sh
python main.py
```

Enter a numeric answer at each prompt. Each equation allows up to three
attempts. Enter one of these commands at the prompt:

- `help` — show the game instructions
- `vars` — show any stored memory variables
- `count` — show the number of correctly solved equations
- `exit` — end the session and display your score

Use Ctrl+C to interrupt a session. On platforms that support it, Ctrl+backslash
also ends the session gracefully.

## Run tests

```sh
python -m unittest discover -s tests -v
```