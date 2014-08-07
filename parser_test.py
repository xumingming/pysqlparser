import unittest
from lexer import Lexer
from parser import Parser
from token1 import *
from expr import *
from op import *

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

    def test_create_table(self):
        parser = create_parser("create table xumm (id int, name string) comment 'hello' partitioned by (c1 int, c2 string)")
        stmt = parser.parse()
        self.assertEquals(2, len(stmt.partition_columns))

    def test_select(self):
        sql = "select xumm.id, name, age from xumm"
        parser = create_parser(sql)
        stmt = parser.parse()
        self.assertEqual("select", stmt.type)
        self.assertEqual(3, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0], PropertyExpr))
        self.assertEqual("xumm", stmt.columns[0].owner.name)
        self.assertEqual("id", stmt.columns[0].name)

    def test_select_number(self):
        sql = "select 1 from xumm"
        parser = create_parser(sql)
        stmt = parser.parse()
        self.assertEqual("select", stmt.type)
        self.assertEqual(1, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0], NumberExpr))
        self.assertEqual(1, stmt.columns[0].number)
