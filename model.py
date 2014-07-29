class CreateTableStatement:
    def __init__(self):
        self.name = None
        self.columns = []
        self.ifNotExists = False
        self.comment = None
        self.partition_columns = []
        self.lifecycle = None

class CreateTableColumn:
    def __init__(self):
        self.name = None
        self.type = None
        self.comment = None