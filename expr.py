class Expr:
    def __init__(self):
        pass


class AllColumnExpr(Expr):
    def __init__(self):
        pass


class ListExpr(Expr):
    def __init__(self):
        self.items = []


class IdentifierExpr(Expr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class PropertyExpr(Expr):
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

    def __str__(self):
        return str(self.owner) + "." + self.name


class NumberExpr(Expr):
    def __init__(self, number):
        self.number = number

class BinaryOpExpr(Expr):
    def __init__(self):
        self.left = None
        self.right = None
        self.operator = None
