class Operator:
    def __init__(self, name):
        self.name = name

Multiply = Operator("*")
Equality = Operator("=")
Divide = Operator("/")
Modulus = Operator("%")
Add = Operator("+")
Subtract = Operator("-")
BitwiseAnd = Operator("&")
BitwiseOr = Operator("|")
BooleanAnd = Operator("AND")
BooleanOr = Operator("OR")
LessThan = Operator("<")
LessThanOrEqual = Operator("<=")
GreaterThan = Operator(">")
GreaterThanOrEqual = Operator(">=")
LessThanOrGreater = Operator("<>")
Like = Operator("LIKE")
NotLike = Operator("NOT LIKE")
Is = Operator("IS")
IsNot = Operator("IS NOT")