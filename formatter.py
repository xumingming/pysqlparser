from parser import Parser


class Formatter:
    def __init__(self, sql):
        self.sql = sql
        self.stmt = Parser(sql).parse()
        self.type = self.stmt.type
        self.buf = []
        self.indent_cnt = 0

    def println(self):
        self.buf.append("\n")
        for i in range(0, self.indent_cnt):
            self.buf.append("    ")

    def increment_indent_cnt(self):
        self.indent_cnt += 1

    def decrement_indent_cnt(self):
        self.indent_cnt -= 1

    def append(self, obj):
        self.buf.append(obj)
        return self

    def format_create(self):
        pass

    def format(self):
        if self.type == 'create':
            self.format_create()
        elif self.type == 'select':
            self.format_select()

        return "".join([str(x) for x in self.buf])

    def format_select(self):
        self.append("SELECT ")

        self.increment_indent_cnt()
        idx = 0
        for column in self.stmt.columns:
            self.append(column)
            if idx < len(self.stmt.columns) - 1:
                self.append(",")

            if idx >= len(self.stmt.columns) - 1:
                self.decrement_indent_cnt()

            if idx >= 0:
                self.println()

            idx += 1

        self.append("FROM ")
        self.append(self.stmt.table_name)

        if self.stmt.where:
            self.println()
            self.append("WHERE")

    def format_create(self):
        self.append("CREATE TABLE")
        if self.stmt.if_not_exists:
            self.append(" IF NOT EXISTS")

        self.append(" ")
        self.append(self.stmt.name)
        self.append(" ")

        self.format_columns(self.stmt.columns)

        if self.stmt.comment:
            self.append(" COMMENT '")
            self.append(self.stmt.comment)
            self.append("'")

        if self.stmt.partition_columns and len(self.stmt.partition_columns) > 0:
            self.println()
            self.append("PARTITIONED BY ")
            self.format_columns(self.stmt.partition_columns)

        if self.stmt.lifecycle:
            self.println()
            self.append("LIFECYCLE ")
            self.append(self.stmt.lifecycle)

    def format_columns(self, columns):
        cnt = 0
        self.append("(")
        self.increment_indent_cnt()
        for column in columns:
            self.println()
            self.append(column.name)
            self.append(" ")
            self.append(column.type)
            if column.comment:
                self.append(" COMMENT '")
                self.append(column.comment)
                self.append("'")

            if cnt < len(columns) - 1:
                self.append(",")

            if cnt == len(columns) - 1:
                self.decrement_indent_cnt()
            cnt += 1

        self.println()
        self.append(")")

