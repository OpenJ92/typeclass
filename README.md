# typeclass

Haskell → Python typeclass isomorphism

⚠️ STATUS: Private Research Project

A symbolic algebraic framework for compositional computation in Python.

## Install

```bash
pip install typeclass-core
```

Requires Python 3.14+

## Example

```python
from typeclass import fmap, run

expr = 1 |fmap| (lambda x: x + 1)
result = run(expr)
```

## Overview

* Build programs as expressions (AST)
* Interpret them with `run`
* Supports common algebraic structures (Functor, Monad, Arrow, etc.)

## License

See `LICENSE`
