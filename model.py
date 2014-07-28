class CreateTableStatement:
    def __init__(self):
        self.name = None
        self.columns = []
        self.ifNotExists = False
        self.comment = None

class CreateTableColumn:
    def __init__(self):
        self.name = None
        self.type = None
        self.comment = None
