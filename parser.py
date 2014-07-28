from lexer import Lexer
from token import *
from exception import ParserException
from model import *

class Parser:
    def __init__(self, sql):
        self.lexer = Lexer(sql)

    def parse(self):
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
                stmt.comment = self.lexer.token_str

        print "very good!"
        return stmt

    def accept(self, token):
        if self.lexer.token == token:
            self.lexer.next_token()
        else:
            actual_token_name = None
            if self.lexer.token != None:
                actual_token_name = self.lexer.token.name
                
            raise ParserException("expect " + token.name + ", actual: " + self.lexer.token.name)
