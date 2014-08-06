class Expr:
    def __init__(self):
        self.parent = None


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
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class InListExpr(Expr):
    def __init__(self):
        self.expr = None
        self.not1 = False
        self.target_list = []


class QueryExpr(Expr):
    def __init__(self):
        self.sub_query = None

class InSubQueryExpr(Expr):
    def __init__(self):
        self.not1 = False
        self.expr = None
        self.sub_query = None
