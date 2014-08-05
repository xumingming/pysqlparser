class Operator:
    def __init__(self, name):
        self.name = name

Multiply = Operator("*")
Divide = Operator("/")
Modulus = Operator("%")
Add = Operator("+")
Subtract = Operator("-")
BitwiseAnd = Operator("&")
BitwiseOr = Operator("|")