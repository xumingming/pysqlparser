class Expr:
    def __init__(self):
        self.parent = None

    def accept(self, visitor):
        visitor.visit(self)


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
    def __init__(self, sub_query):
        self.sub_query = sub_query
        sub_query.parent = self


class InSubQueryExpr(Expr):
    def __init__(self):
        self.not1 = False
        self.expr = None
        self.sub_query = None


class BetweenExpr(Expr):
    def __init__(self, test_expr, begin_expr, end_expr):
        self.test_expr = test_expr
        self.not1 = False
        self.begin_expr = begin_expr
        self.end_expr = end_expr


class StringExpr(Expr):
    def __init__(self, str):
        self.str = str

class NullExpr(Expr):
    def __init__(self):
        pass

class OrderingSpec:
    def __init__(self, name):
        self.name = name

ORDER_BY_ASC = OrderingSpec("ASC")
ORDER_BY_DESC = OrderingSpec("DESC")

class SelectOrderByItem:
    def __init__(self):
        self.expr = None
        self.type = ORDER_BY_ASC

class SelectOrderBy:
    def __init__(self):
        self.items = []

class SelectGroupBy:
    def __init__(self):
        self.items = []
        self.having = None
