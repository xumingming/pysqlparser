import unittest
from lexer import Lexer
from parser import Parser
from token import *
from formatter import format

def create_parser(sql):
    return Parser(sql)

class ParserTestCase(unittest.TestCase):
    def helper(self, sql):
        print "SQL: ", sql
        lexer = Lexer(sql)
        lexer.next_token()
        while lexer.token.name != EOF.name:
            print lexer.info()
            lexer.next_token()

    def test_comment_and_select(self):
        parser = create_parser("create table xumm (id int comment 'this is a id', name string comment 'this is name', age int comment 'what a fuck comment')")
        stmt = parser.parse()
        format(stmt)
        
