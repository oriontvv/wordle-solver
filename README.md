# wordle-solver
[![CI](https://github.com/oriontvv/wordle-solver/workflows/ci/badge.svg)](https://github.com/oriontvv/wordle-solver/actions)
[![Coverage badge](https://raw.githubusercontent.com/oriontvv/wordle-solver/python-coverage-comment-action-data/badge.svg)](https://github.com/oriontvv/wordle-solver/actions/workflows/python-package.yml)

A simple [solver](https://github.com/oriontvv/wordle-solver) for [wordle](https://en.wikipedia.org/wiki/Wordle) puzzle game.


Format:

```
x     character solved
x+    character is in the word
x-    character is NOT in the word
new   start new game
exit  close program

characters should be delimeted with space:
a i- e t+ r+
```

Running:

```bash
$ git clone https://github.com/oriontvv/wordle-solver
$ cd wordle-solver
$ python src/cli.py --lang ru
```
