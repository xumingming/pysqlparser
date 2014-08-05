class Statement:
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

class CreateTableColumn:
    def __init__(self):
        self.name = None
        self.type = None
        self.comment = None

class SelectStatement(Statement):
    def __init__(self):
        Statement.__init__(self, "select")
        self.columns = []
        self.table_name = None


class SelectItem:
    def __init__(self):
        self.expr = None
        self.alias = None