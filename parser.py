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
            column.name = self.token_str()
            self.next_token()

            column.type = self.token_str()
            self.next_token()

            if self.token() == COMMENT:
                self.next_token()
                column.comment = self.accept(LITERAL_STRING)
            columns.append(column)

            if self.token() != COMMA:
                break
            else:
                self.next_token()
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

        stmt.name = self.token_str()
        self.next_token()

        if self.token() != LIKE:
            stmt.columns = self.parse_column_definition()
            
            if self.token() == COMMENT:
                self.next_token()
                stmt.comment = self.accept(LITERAL_STRING)

            if self.token() == PARTITIONED:
                self.next_token()
                if self.token() != BY:
                    raise ParserException("PARTITIONED should be followed by BY!")
                self.next_token()

                stmt.partition_columns = self.parse_column_definition()

                if self.token() == LIFECYCLE:
                    self.next_token()
                    stmt.lifecycle = self.token_str()
        return stmt

    def accept(self, token):
        if self.token() == token:
            ret = self.token_str()
            self.next_token()
            return ret
        else:
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
