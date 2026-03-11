def pretty(tree, prefix="", is_last=True):
    connector = "└─ " if is_last else "├─ "
    print(prefix + connector + repr(tree.value))

    children = list(tree.children)
    next_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(children):
        pretty(child, next_prefix, i == len(children) - 1)

def size(tree):
    return 1 + sum(size(child) for child in self.children)

def depth(tree):
    if tree.children == Nil():
        return 1
    return 1 + max(depth(child) for child in tree.children)
