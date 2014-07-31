from lexer import Lexer
from token import *
from exception import ParserException, InvalidCharException
from model import *
from traceback import print_exc


class Parser:
    def __init__(self, sql):
        self.lexer = Lexer(sql)

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
            return self.parse_create_table()
        except ParserException,e:
            print "Exception: ", e.msg
            print_exc(e)
        except InvalidCharException,e:
            print "Exception: ", e.msg
            print_exc(e)

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
        self.next_token()

        stmt = CreateTableStatement()
        self.accept(CREATE)
        self.accept(TABLE)
        
        if self.token() == IF:
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
                    stmt.lifecycle = self.accept(LIFECYCLE)

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
