class Infix:
    """
    Enables infix-style function application using `|op|` syntax.
    """
    def __init__(self, func):
        self.func = func

    def __ror__(self, left):
        return Infix(lambda right: self.func(left, right))

    def __or__(self, right):
        return self.func(right)

