from lexer import Lexer
from token import *
from exception import ParserException

class Parser:
    def __init__(self, sql):
        self.lexer = Lexer(sql)

    def parse(self):
        self.lexer.next_token()

        stmt = CreateTableStatement()
        self.accept(CREATE)
        self.accept(TABLE)
        #self.accept(IDENTIFIER)
        
        print "very good!"

    def accept(self, token):
        if self.lexer.token == token:
            self.lexer.next_token()
        else:
            actual_token_name = None
            if self.lexer.token != None:
                actual_token_name = self.lexer.token.name

            raise ParserException("expect " + token.name + ", actual: " + self.lexer.token.name)


class CreateTableStatement:
    def __init__(self):
        self.name = None
        self.columns = []
