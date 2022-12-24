# wordle-solver
[![CI](https://github.com/oriontvv/wordle-solver/workflows/ci/badge.svg)](https://github.com/oriontvv/wordle-solver/actions)

A simple [solver](https://github.com/oriontvv/wordle-solver) for [wordle](https://en.wikipedia.org/wiki/Wordle) puzzle game.


Format:

```
x     character solved
x+    character is in the word
x-    character is NOT in the word
reset command will reset the state of the solver
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
