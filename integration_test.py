import unittest
from lexer import Lexer
from token import *

def create_lexer(sql):
    return Lexer(sql)

class IntegrationTestCase(unittest.TestCase):
    def helper(self, sql):
        print "SQL: ", sql
        lexer = Lexer(sql)
        lexer.next_token()
        while lexer.token.name != EOF.name:
            print lexer.info()
            lexer.next_token()

    def test_comment_and_select(self):
        sql = """
        -- this is a comment
        select * from xumm;
        """
        lexer = create_lexer(sql)
        tokens = lexer.tokens()
        self.assertEquals([LITERAL_COMMENT, SELECT, STAR,
                           FROM, IDENTIFIER, SEMI], tokens)

    def test_select_a_string(self):
        sql = """
        select 'hello' from xumm;
        create table person(id int, name string, age int);
        drop table helloworld;
        """
        
