import unittest
from lexer import Lexer
from parser import Parser
from token import *

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
        parser = create_parser("create table xumm (id int, name string) comment 'hello' partitioned by (c1 int, c2 string)")
        stmt = parser.parse()
        self.assertEquals(2, len(stmt.partition_columns))
