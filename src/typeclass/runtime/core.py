from functools import wraps
from inspect import signature

from typeclass.interpret.run import run

def curry(fn):
    arity = len(signature(fn).parameters)

    @wraps(fn)
    def curried(*args):
        if len(args) >= arity:
            return fn(*args)
        return lambda *more: curried(*(args + more))
    return curried

def interpret(expression):
    return run(expression, None, None)

def interpreted(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return fn(
            *[interpret(a) for a in args],
            **{k: interpret(v) for k, v in kwargs.items()},
        )
    return wrapped

def evaluate(expression):
    return interpret(expression).force()

def evaluated(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return fn(
            *[evaluate(a) for a in args],
            **{k: evaluate(v) for k, v in kwargs.items()},
        )
    return wrapped


