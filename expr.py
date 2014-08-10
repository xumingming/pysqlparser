class Expr:
    def __init__(self):
        self.parent = None

    def accept(self, visitor):
        visitor.visit(self)


class AllColumnExpr(Expr):
    def __init__(self):
        Expr.__init__(self)


class ListExpr(Expr):
    def __init__(self):
        self.items = []
        Expr.__init__(self)


class IdentifierExpr(Expr):
    def __init__(self, name):
        self.name = name
        Expr.__init__(self)


class PropertyExpr(Expr):
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        Expr.__init__(self)


class NumberExpr(Expr):
    def __init__(self, number):
        self.number = number
        Expr.__init__(self)


class BinaryOpExpr(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        Expr.__init__(self)

    @property
    def left(self):
        return self.left

    @left.setter
    def left(self, left):
        self.left = left
        self.left.parent = self

    @property
    def right(self):
        return self.right

    @right.setter
    def right(self, right):
        self.right = right
        self.right.parent = self

    @property
    def operator(self):
        return self.operator

    @operator.setter
    def operator(self, operator):
        self.operator = operator
        self.operator.parent = self


class InListExpr(Expr):
    def __init__(self):
        self.expr = None
        self.not1 = False
        self.target_list = []
        Expr.__init__(self)


class QueryExpr(Expr):
    def __init__(self, sub_query):
        self.sub_query = sub_query
        sub_query.parent = self
        Expr.__init__(self)


class InSubQueryExpr(Expr):
    def __init__(self):
        self.not1 = False
        self.expr = None
        self.sub_query = None
        Expr.__init__(self)


class BetweenExpr(Expr):
    def __init__(self, test_expr, begin_expr, end_expr):
        self.test_expr = test_expr
        self.not1 = False
        self.begin_expr = begin_expr
        self.end_expr = end_expr
        Expr.__init__(self)


class StringExpr(Expr):
    def __init__(self, str):
        self.str = str
        Expr.__init__(self)


class MethodInvokeExpr(Expr):
    def __init__(self):
        self.method_name = None
        self.owner = None
        self.parameters = []
        Expr.__init__(self)


class NullExpr(Expr):
    def __init__(self):
        Expr.__init__(self)


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


class SetQuantifier(Expr):
    def __init__(self, name):
        self.name = name
        Expr.__init__(self)

SQ_ALL = SetQuantifier("ALL")
SQ_DISTINCT = SetQuantifier("DISTINCT")
