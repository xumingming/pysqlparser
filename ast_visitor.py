import visit as v
from stmt import *
from expr import *

class AstVisitor:
    def __init__(self):
        self.buf = []
        self.indent_cnt = 0

    def increment_indent_cnt(self):
        self.indent_cnt += 1

    def decrement_indent_cnt(self):
        self.indent_cnt -= 1

    def append(self, obj):
        self.buf.append(obj)
        return self

    def println(self):
        self.buf.append("\n")
        for i in range(0, self.indent_cnt):
            self.buf.append("    ")

    @v.on('node')
    def visit(self, node):
        """
        hello
        """

    @v.when(CreateTableColumn)
    def visit(self, column):
        self.append(column.name)
        self.append(" ")
        self.append(column.type)
        if column.comment:
            self.append(" COMMENT '")
            self.append(column.comment)
            self.append("'")

    def visit_columns(self, columns):
        self.append("(")
        self.increment_indent_cnt()
        self.println()
        cnt = 0

        for column in columns:
            column.accept(self)
            if cnt < len(columns) - 1:
                self.append(",")
                self.println()
            cnt += 1
        self.decrement_indent_cnt()
        self.println()
        self.append(")")


    @v.when(CreateTableStatement)
    def visit(self, stmt):
        self.append("CREATE TABLE")
        if stmt.if_not_exists:
            self.append(" IF NOT EXISTS")

        self.append(" ")
        self.append(stmt.name)
        self.append(" ")
        self.visit_columns(stmt.columns)

        if stmt.comment:
            self.append(" COMMENT '")
            self.append(stmt.comment)
            self.append("'")

        if stmt.partition_columns and len(stmt.partition_columns) > 0:
            self.println()
            self.append("PARTITIONED BY ")
            self.visit_columns(stmt.partition_columns)

        if stmt.lifecycle:
            self.println()
            self.append("LIFECYCLE ")
            self.append(stmt.lifecycle)

    @v.when(SelectItem)
    def visit(self, select_item):
        select_item.expr.accept(self)
        if select_item.alias:
            self.append(" AS ")
            self.append(select_item.alias)

    def visit_select_columns(self, stmt):
        self.increment_indent_cnt()
        idx = 0
        for column in stmt.columns:
            #self.append(column)
            column.accept(self)
            if idx < len(stmt.columns) - 1:
                self.append(",")

            if 0 <= idx < len(stmt.columns) - 1:
                self.println()
            idx += 1
        self.decrement_indent_cnt()
        self.println()

    @v.when(SelectStatement)
    def visit(self, stmt):
        self.append("SELECT ")
        self.visit_select_columns(stmt)
        self.append("FROM ")
        self.append(stmt.table_name)

        if stmt.where:
            self.println()
            self.append("WHERE ")
            stmt.where.accept(self)

    @v.when(NumberExpr)
    def visit(self, expr):
        self.append(expr.number)

    @v.when(StringExpr)
    def visit(self, expr):
        self.append("'")
        self.append(expr.str)
        self.append("'")

    @v.when(IdentifierExpr)
    def visit(self, expr):
        self.append(expr.name)

    @v.when(InListExpr)
    def visit(self, expr):
        expr.expr.accept(self)
        if expr.not1:
            self.append(" NOT")
        self.append(" IN (")

        cnt = 0
        for item in expr.target_list:
            item.accept(self)
            if cnt < len(expr.target_list) - 1:
                self.append(", ")

            cnt += 1
        self.append(")")

    @v.when(InSubQueryExpr)
    def visit(self, expr):
        expr.expr.accept(self)

        if expr.not1:
            self.append(" NOT")
        self.append(" IN (")
        self.increment_indent_cnt()
        self.println()
        expr.sub_query.accept(self)
        self.decrement_indent_cnt()
        self.println()
        self.append(")")

    @v.when(BinaryOpExpr)
    def visit(self, expr):
        if isinstance(expr.left, Expr):
            expr.left.accept(self)
        else:
            self.append(expr.left)
        self.append(" ")
        self.append(expr.operator.name)
        self.append(" ")

        if isinstance(expr.right, Expr):
            expr.right.accept(self)
        else:
            self.append(expr.right)
