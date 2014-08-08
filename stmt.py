class ASTNode:
    def accept(self, visitor):
        visitor.visit(self)

class Statement(ASTNode):
    def __init__(self, type):
        self.type = type

class CreateTableStatement(Statement):
    def __init__(self):
        Statement.__init__(self, "create")
        self.name = None
        self.columns = []
        self.if_not_exists = False
        self.comment = None
        self.partition_columns = []
        self.lifecycle = None

class CreateTableColumn(ASTNode):
    def __init__(self):
        self.name = None
        self.type = None
        self.comment = None

class SelectStatement(Statement):
    def __init__(self):
        Statement.__init__(self, "select")
        self.set_quantifier = None
        self.columns = []
        self.table_name = None
        self.where = None
        self.order_by = None

class SelectItem(ASTNode):
    def __init__(self, expr, alias):
        self.expr = expr
        self.alias = alias

class JoinType:
    def __init__(self, name):
        self.name = name

LEFT_OUTER_JOIN = JoinType("LEFT JOIN")
RIGHT_OUTER_JOIN = JoinType("RIGHT JOIN")
FULL_OUTER_JOIN = JoinType("FULL JOIN")
INNER_JOIN = JoinType("INNER JOIN")
COMMA_JOIN = JoinType(",")
JOIN_JOIN = JoinType("JOIN")


class TableSourceBase(ASTNode):
    def __init__(self):
        self.alias = None


class TableSource(TableSourceBase):
    def __init__(self):
        self.expr = None
        TableSourceBase.__init__(self)

class SubQueryTableSource(TableSourceBase):
    def __init__(self):
        self.select = None
        TableSourceBase.__init__(self)


class JoinTableSource(TableSourceBase):
    def __init__(self):
        self.left = None
        self.join_type = None
        self.right = None
        self.condition = None
        TableSourceBase.__init__(self)

