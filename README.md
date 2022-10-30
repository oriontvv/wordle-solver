# wordle-solver
[![CI](https://github.com/oriontvv/wordle-solver/workflows/Python%20package/badge.svg)](https://github.com/oriontvv/wordle-solver/actions)

A simle [solver](https://github.com/oriontvv/wordle-solver) for [wordle](https://en.wikipedia.org/wiki/Wordle) puzzle game.


Format:

```
x  character solved
x+ character is in the word
x- character is NOT in the word

characters should be delimeted with space:
a i- e t+ r+
```

Running:

`python src/cli.py --lang ru`

`reset` command will reset the state of the solver
