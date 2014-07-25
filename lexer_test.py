import unittest
from lexer import Lexer
from token import *

def create_lexer(sql):
    return Lexer(sql)

class LexerTestCase(unittest.TestCase):
    def helper(self, sql):
        lexer = Lexer(sql)
        lexer.next_token()
        while lexer.token.name != EOF.name:
            lexer.info()
            lexer.next_token()

    def test_identifier(self):
        lexer = create_lexer("x123_456")
        tokens = lexer.tokens()
        self.assertEquals([IDENTIFIER], tokens)

    def test_number(self):
        lexer = create_lexer("99")
        tokens = lexer.tokens()
        self.assertEquals([NUMBER], tokens)

    def test_select(self):
        lexer = create_lexer("Select * from xumm")
        tokens = lexer.tokens()
        self.assertEquals([SELECT, STAR, FROM, IDENTIFIER], tokens)

    def test_create_table(self):
        lexer = create_lexer("create table xumm(id int, name string)")
        tokens = lexer.tokens()
        self.assertEquals([CREATE, TABLE, IDENTIFIER, LPAREN, IDENTIFIER, IDENTIFIER, COMMA, IDENTIFIER, STRING, RPAREN], tokens)


        pass

if __name__ == '__main__':
    unittest.main()
