import unittest
from lexer import Lexer
from token1 import *

def create_lexer(sql):
    return Lexer(sql)

class LexerTestCase(unittest.TestCase):
    def helper(self, sql):
        lexer = Lexer(sql)
        lexer.next_token()
        while lexer.token.name != EOF.name:
            print lexer.info()
            lexer.next_token()

    def test_identifier(self):
        # first char is lowercase
        lexer = create_lexer("x123_456")
        lexer.next_token()
        self.assertEquals(IDENTIFIER, lexer.token)
        self.assertEquals("x123_456", lexer.token_str)

        # first char is uppercase
        lexer = create_lexer("X123_456")
        lexer.next_token()
        self.assertEquals(IDENTIFIER, lexer.token)
        self.assertEquals("X123_456", lexer.token_str)

        # first char is underscore
        lexer = create_lexer("_X123_456")
        lexer.next_token()
        self.assertEquals(IDENTIFIER, lexer.token)
        self.assertEquals("_X123_456", lexer.token_str)

        # first char is dollar
        lexer = create_lexer("$123_456")
        lexer.next_token()
        self.assertEquals(IDENTIFIER, lexer.token)
        self.assertEquals("$123_456", lexer.token_str)

    def test_number(self):
        # normal integer
        lexer = create_lexer("99")
        lexer.next_token()
        self.assertEquals(LITERAL_INT, lexer.token)
        self.assertEquals("99", lexer.token_str)
        lexer.next_token()
        self.assertEquals(EOF, lexer.token)

        # normal integer end with comma
        lexer = create_lexer("99,")
        lexer.next_token()
        self.assertEquals(LITERAL_INT, lexer.token)
        self.assertEquals("99", lexer.token_str)
        lexer.next_token()
        self.assertEquals(COMMA, lexer.token)

        # another integer
        lexer = create_lexer("00009")
        lexer.next_token()
        self.assertEquals(LITERAL_INT, lexer.token)
        self.assertEquals("00009", lexer.token_str)
        lexer.next_token()
        self.assertEquals(EOF, lexer.token)

        # a minus integer
        #lexer = create_lexer("-9")
        #tokens = lexer.tokens()
        #self.assertEquals([LITERAL_INT], tokens)

        # float
        lexer = create_lexer("0.09")
        lexer.next_token()
        self.assertEquals(LITERAL_FLOAT, lexer.token)
        self.assertEquals("0.09", lexer.token_str)
        lexer.next_token()
        self.assertEquals(EOF, lexer.token)

        # a minus float
        #lexer = create_lexer("-0.09")
        #tokens = lexer.tokens()
        #self.assertEquals([LITERAL_FLOAT], tokens)

    def test_string(self):
        lexer = create_lexer("'abcde'")
        lexer.next_token()
        self.assertEquals(LITERAL_STRING, lexer.token)
        self.assertEquals("abcde", lexer.token_str)
        lexer.next_token()
        self.assertEquals(EOF, lexer.token)

    def test_comment(self):
        lexer = create_lexer("--hello")
        lexer.next_token()
        self.assertEquals(LITERAL_COMMENT, lexer.token)
        self.assertEquals("hello", lexer.token_str)
        lexer.next_token()
        self.assertEquals(EOF, lexer.token)


    def test_select(self):
        lexer = create_lexer("Select * from xumm")
        tokens = lexer.tokens()
        self.assertEquals([SELECT, STAR, FROM, IDENTIFIER], tokens)

    def test_create_table(self):
        # normal create table
        lexer = create_lexer("create table xumm(id int, name string)")
        tokens = lexer.tokens()
        self.assertEquals([CREATE, TABLE, IDENTIFIER, LPAREN, IDENTIFIER, INT, COMMA, IDENTIFIER, STRING, RPAREN], tokens)

        # create table with comment
        lexer = create_lexer("create table xumm(id int comment 'id', name string comment 'name')")
        tokens = lexer.tokens()
        self.assertEquals([CREATE, TABLE, IDENTIFIER, LPAREN,
                           IDENTIFIER, INT, COMMENT, LITERAL_STRING,
                           COMMA, IDENTIFIER, STRING, COMMENT, LITERAL_STRING, RPAREN], tokens)

        # create table if not exists
        lexer = create_lexer("create table if not exists xumm(id int, name string)")
        tokens = lexer.tokens()
        self.assertEquals([CREATE, TABLE, IF, NOT, EXISTS, IDENTIFIER, LPAREN,
                           IDENTIFIER, INT, COMMA, IDENTIFIER, STRING, RPAREN], tokens)

        # create table lifecycle
        lexer = create_lexer("create table xumm(id int, name string) lifecycle 1")
        tokens = lexer.tokens()
        self.assertEquals([CREATE, TABLE, IDENTIFIER, LPAREN,
                           IDENTIFIER, INT, COMMA, IDENTIFIER, STRING, RPAREN, LIFECYCLE, LITERAL_INT], tokens)

        # create table as
        lexer = create_lexer("create table xumm(id int, name string) as select * from auto_test")
        tokens = lexer.tokens()
        self.assertEquals([CREATE, TABLE, IDENTIFIER, LPAREN, IDENTIFIER, INT, COMMA, 
                           IDENTIFIER, STRING, RPAREN, AS, SELECT, STAR, FROM, IDENTIFIER], tokens)

        # create table like xxx
        lexer = create_lexer("create table xumm(id int, name string) like auto_test")
        tokens = lexer.tokens()
        self.assertEquals([CREATE, TABLE, IDENTIFIER, LPAREN, IDENTIFIER, INT, COMMA, 
                           IDENTIFIER, STRING, RPAREN, LIKE, IDENTIFIER], tokens)
        

