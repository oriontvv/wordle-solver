# wordle-solver
[![CI](https://github.com/oriontvv/wordle-solver/workflows/ci/badge.svg)](https://github.com/oriontvv/wordle-solver/actions)
[![Coverage badge](https://raw.githubusercontent.com/oriontvv/wordle-solver/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/oriontvv/wordle-solver/blob/python-coverage-comment-action-data/htmlcov/index.html)

A simple [solver](https://github.com/oriontvv/wordle-solver) for [wordle](https://en.wikipedia.org/wiki/Wordle) puzzle game.


## Format:

```
x     character solved
x+    character is in the word
x-    character is NOT in the word
new   start new game
exit  close program

characters should be delimeted with space:
a i- e t+ r+
```

## Install:

```bash
$ git clone https://github.com/oriontvv/wordle-solver
$ cd wordle-solver
$ python -m pip install -U poetry setuptools && poetry install
```

## Running
### telegram [bot](https://t.me/WordleGameSolverBot)

```bash
$ echo "TELEGRAM_TOKEN=### YOUR_TOKEN_HERE ###" > .env
$ python src/main.py --lang ru --bot
```

### cli repl

```bash
$ python src/main.py --lang en
```
