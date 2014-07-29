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

    def parse_create_table(self):
        self.next_token()

        stmt = CreateTableStatement()
        self.accept(CREATE)
        self.accept(TABLE)
        
        if self.token() == IF:
            self.accept(NOT)
            self.accept(EXISTS)
            self.ifNotExists = True

        stmt.name = self.lexer.token_str
        self.next_token()

        if self.token() != LIKE:
            self.accept(LPAREN)
            while True:
                column = CreateTableColumn()
                column.name = self.lexer.token_str
                self.next_token()

                column.type = self.lexer.token_str
                self.next_token()

                if self.token() == COMMENT:
                    self.accept(COMMENT)
                    column.comment = self.lexer.token_str
                    self.next_token()

                stmt.columns.append(column)
                if self.token() == COMMA:
                    self.accept(COMMA)
                else:
                    break

            self.accept(RPAREN)
            
            if self.token() == COMMENT:
                self.next_token()
                stmt.comment = self.lexer.token_str
                self.next_token()

            if self.token() == PARTITIONED:
                self.next_token()
                if self.token() != BY:
                    raise ParserException("PARTITIONED should be followed by BY!")
                self.next_token()

                self.accept(LPAREN)
                while True:
                    column = CreateTableColumn()
                    column.name = self.lexer.token_str
                    self.next_token()

                    column.type = self.lexer.token_str
                    self.next_token()

                    if self.token() == COMMENT:
                        self.next_token()
                        column.comment = self.lexer.token_str
                    stmt.partition_columns.append(column)

                    if self.token() != COMMA:
                        break
                    else:
                        self.next_token()
                self.accept(RPAREN)

                if self.token() == LIFECYCLE:
                    self.next_token()
                    stmt.lifecycle = self.lexer.token_str
        return stmt

    def accept(self, token):
        if self.token() == token:
            self.next_token()
        else:
            actual_token_name = None
            if self.token() != None:
                actual_token_name = self.lexer.token.name
                
            raise ParserException("expect " + token.name + ", actual: " + self.lexer.token.name
                                  + "[" + self.lexer.token_str + "]")
