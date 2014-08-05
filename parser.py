from lexer import Lexer
from token import *
from exception import ParserException, InvalidCharException
from stmt import *
from expr import *
from op import *
from traceback import print_exc
from keywords import is_keyword


class Parser:
    def __init__(self, sql):
        self.lexer = Lexer(sql)
        self.next_token()

    def token(self):
        """
        get the current token
        """
        return self.lexer.token

    def token_str(self):
        return self.lexer.token_str

    def next_token(self):
        self.lexer.next_token()

    def parse(self):
        try:
            if self.match(SELECT):
                return self.parse_select()
            elif self.match(CREATE):
                return self.parse_create_table()

        except ParserException,e:
            print "Exception: ", e.msg
            print_exc(e)
        except InvalidCharException,e:
            print "Exception: ", e.msg
            print_exc(e)

    def parse_select(self):
        self.accept(SELECT)

        stmt = SelectStatement()
        while not self.match(FROM):
            column = self.expr()
            stmt.columns.append(column)
            if self.match(COMMA):
                self.accept(COMMA)
            else:
                break
        self.accept(FROM)

        stmt.table_name = self.accept(IDENTIFIER)

        return stmt

    def expr(self):
        if self.token() == STAR:
            return AllColumnExpr()

        ret = self.primary()

        if self.token() == COMMA:
            return ret

        return self.expr_rest(ret)

    def expr_rest(self, expr):
        expr = self.multiplicative_rest(expr)
        expr = self.additive_rest(expr)
        expr = self.bit_and_rest(expr)
        expr = self.bit_or_rest(expr)
        #expr = self.in_rest(expr)
        #expr = self.relational_rest(expr)
        #expr = self.equality_rest(expr)
        #expr = self.and1_rest(expr)
        #expr = self.or1_rest(expr)

        return expr

    def multiplicative(self):
        expr = self.primary()
        return self.multiplicative_rest(expr)

    def multiplicative_rest(self, expr):
        if self.token() == STAR:
            self.next_token()
            right_expr = self.primary()
            expr = BinaryOpExpr(expr, Multiply, right_expr)
            expr = self.multiplicative_rest(expr)
        elif self.token() == SLASH:
            self.next_token()
            right_expr = self.primary()
            expr = BinaryOpExpr(expr, Divide, right_expr)
            expr = self.multiplicative_rest(expr)
        elif self.token() == PERCENT:
            self.next_token()
            right_expr = self.primary()
            expr = BinaryOpExpr(expr, Modulus, right_expr)
            expr = self.multiplicative_rest(expr)

        return expr

    def additive(self):
        expr = self.multiplicative()
        return self.additive_rest(expr)

    def additive_rest(self, expr):
        if self.token() == PLUS:
            self.next_token()
            right_expr = self.multiplicative()
            expr = BinaryOpExpr(expr, Add, right_expr)
            expr = self.additive_rest(expr)
        elif self.token() == MINUS:
            self.next_token()
            right_expr = self.multiplicative()
            expr = BinaryOpExpr(expr, Subtract, right_expr)
            expr = self.additive_rest(expr)

        return expr

    def bit_and(self):
        expr = self.additive()
        return self.bit_and_rest(expr)

    def bit_and_rest(self, expr):
        while self.token() == AMP:
            self.next_token()
            right_expr = self.additive()
            expr = BinaryOpExpr(expr, BitwiseAnd, right_expr)

        return expr

    def bit_or(self):
        expr = self.bit_and()
        return self.bit_or_rest(expr)

    def bit_or_rest(self, expr):
        while self.token() == BAR:
            self.next_token()
            right_expr = self.bit_and()
            expr = BinaryOpExpr(expr, BitwiseOr, right_expr)

        return expr

    def in_rest(self, expr):
        pass

    def equality(self):
        expr = self.bit_or()
        return self.equaility_rest(expr)

    def equality_rest(self, expr):
        pass

    def relational(self):
        expr = self.equaility()
        return self.relational_rest(expr)

    def relational_rest(self, expr):
        pass

    def and1(self):
        expr = self.relational()
        return self.and1_rest(expr)

    def and1_rest(self, expr):
        pass

    def or1(self):
        expr = self.and1()
        return self.or1_rest(expr)

    def or1_rest(self, expr):
        pass

    def primary(self):
        expr = None
        tok = self.token()
        if tok == IDENTIFIER:
            expr = IdentifierExpr(self.token_str())
            self.next_token()
        elif tok == LITERAL_INT:
            expr = NumberExpr(int(self.token_str()))
            self.next_token()
        elif tok == LITERAL_FLOAT:
            expr = NumberExpr(float(self.token_str()))
            self.next_token()

        return self.primary_rest(expr)

    def primary_rest(self, expr):
        if not expr:
            raise ParserException("expr is None!")

        if self.token() == DOT:
            self.accept(DOT)
            expr = self.dot_rest(expr)
            return self.primary_rest(expr)
        return expr

    def dot_rest(self, expr):
        if self.token() == STAR:
            self.accept(STAR)
            expr = PropertyExpr(expr, "*")
        else:
            name = None

            if (self.token() == IDENTIFIER
                or self.token() == LITERAL_STRING):
                name = self.token_str()
                self.next_token()
            elif is_keyword(self.token()):
                name = self.token_str()
                self.next_token()
            else:
                raise ParserException("error: " + self.token_str())

            expr = PropertyExpr(expr, name)

        return expr

    def parse_column_definition(self):
        columns = []
        self.accept(LPAREN)
        while True:
            column = CreateTableColumn()
            column.name = self.accept(IDENTIFIER)
            column.type = self.accept_data_type()

            if self.match(COMMENT):
                self.accept(COMMENT)
                column.comment = self.accept(LITERAL_STRING)
            columns.append(column)

            if not self.match(COMMA):
                break
            else:
                self.accept(COMMA)
        self.accept(RPAREN)

        return columns

    def parse_create_table(self):
        stmt = CreateTableStatement()
        self.accept(CREATE)
        self.accept(TABLE)
        
        if self.match(IF):
            self.accept(IF)
            self.accept(NOT)
            self.accept(EXISTS)
            stmt.if_not_exists = True

        stmt.name = self.accept(IDENTIFIER)

        if not self.match(LIKE):
            stmt.columns = self.parse_column_definition()
            
            if self.match(COMMENT):
                self.accept(COMMENT)
                stmt.comment = self.accept(LITERAL_STRING)

            if self.match(PARTITIONED):
                self.accept(PARTITIONED)
                self.accept(BY)
                stmt.partition_columns = self.parse_column_definition()

                if self.match(LIFECYCLE):
                    self.accept(LIFECYCLE)
                    stmt.lifecycle = self.accept(LITERAL_INT)

        return stmt

    def match(self, token):
        return self.token() == token

    def match_any(self, tokens):
        for tk in tokens:
            if self.match(tk):
                return True

        return False

    def parser_error(self, token):
        actual_token_name = 'None'
        actual_token_str = 'None'
        if self.token():
            actual_token_name = str(self.token())
            actual_token_str = self.token_str()
        raise ParserException("expect " + token.name + ", actual: " + actual_token_name
                              + "[" + actual_token_str + "], pos: " + str(self.lexer.pos)
                              + ", error near: "
                              + "\n=====================================================\n"
                              + self.lexer.surroudings()
                              + "\n=====================================================\n")

    def accept_data_type(self):
        matched = self.match_any([STRING, INT, BIGINT, DATETIME])
        if matched:
            ret = self.token_str()
            self.next_token()
            return ret
        else:
            self.parse_error([STRING, INT, BIGINT, DATETIME])

    def accept(self, token):
        if self.match(token):
            ret = self.token_str()
            self.next_token()
            return ret
        else:
            self.parser_error(token)
