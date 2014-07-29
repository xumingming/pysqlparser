from lexer import Lexer
from token import *
from exception import ParserException, InvalidCharException
from model import *
from traceback import print_exc

class Parser:
    def __init__(self, sql):
        self.lexer = Lexer(sql)

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
        self.lexer.next_token()

        stmt = CreateTableStatement()
        self.accept(CREATE)
        self.accept(TABLE)
        
        if self.lexer.token == IF:
            self.accept(NOT)
            self.accept(EXISTS)
            self.ifNotExists = True

        stmt.name = self.lexer.token_str

        self.lexer.next_token()

        if self.lexer.token != LIKE:
            self.accept(LPAREN)
            while True:
                column = CreateTableColumn()
                column.name = self.lexer.token_str
                self.lexer.next_token()

                column.type = self.lexer.token_str
                self.lexer.next_token()

                if self.lexer.token == COMMENT:
                    self.accept(COMMENT)
                    column.comment = self.lexer.token_str
                    self.lexer.next_token()

                stmt.columns.append(column)
                if self.lexer.token == COMMA:
                    self.accept(COMMA)
                else:
                    break

            self.accept(RPAREN)
            
            if self.lexer.token == COMMENT:
                self.lexer.next_token()
                stmt.comment = self.lexer.token_str
                self.lexer.next_token()

            if self.lexer.token == PARTITIONED:
                self.lexer.next_token()
                if self.lexer.token != BY:
                    raise ParserException("PARTITIONED should be followed by BY!")
                self.lexer.next_token()

                self.accept(LPAREN)
                while True:
                    column = CreateTableColumn()
                    column.name = self.lexer.token_str
                    self.lexer.next_token()

                    column.type = self.lexer.token_str
                    self.lexer.next_token()

                    if self.lexer.token == COMMENT:
                        self.lexer.next_token()
                        column.comment = self.lexer.token_str
                    stmt.partition_columns.append(column)

                    if self.lexer.token != COMMA:
                        break
                    else:
                        self.lexer.next_token()
                self.accept(RPAREN)

                if self.lexer.token == LIFECYCLE:
                    self.lexer.next_token()
                    stmt.lifecycle = self.lexer.token_str
        return stmt

    def accept(self, token):
        if self.lexer.token == token:
            self.lexer.next_token()
        else:
            actual_token_name = None
            if self.lexer.token != None:
                actual_token_name = self.lexer.token.name
                
            raise ParserException("expect " + token.name + ", actual: " + self.lexer.token.name
                                  + "[" + self.lexer.token_str + "]")
