import unittest
from lexer import Lexer
from parser import Parser
from token1 import *
from expr import *
from op import *
from stmt import *

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
        stmt = parser.parse_create_table()
        self.assertEquals(2, len(stmt.partition_columns))

    def test_select(self):
        sql = "select xumm.id, name, age from xumm"
        parser = create_parser(sql)
        stmt = parser.parse_select()
        self.assertEqual("select", stmt.type)
        self.assertEqual(3, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0].expr, PropertyExpr))
        self.assertEqual("xumm", stmt.columns[0].expr.owner.name)
        self.assertEqual("id", stmt.columns[0].expr.name)

    def test_select_star(self):
        sql = "select * from xumm"
        parser = create_parser(sql)
        stmt = parser.parse_select()
        self.assertEqual(1, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0].expr, AllColumnExpr))

    def test_select_number(self):
        sql = "select 1 from xumm"
        parser = create_parser(sql)
        stmt = parser.parse_select()
        self.assertEqual("select", stmt.type)
        self.assertEqual(1, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0].expr, NumberExpr))
        self.assertEqual(1, stmt.columns[0].expr.number)

    def test_parse_table_name(self):
        sql = "select 1 from xumm as xumm1"
        parser = create_parser(sql)
        stmt = parser.parse_select()
        self.assertEqual("select", stmt.type)
        self.assertTrue(isinstance(stmt.table_name, TableSource))
        self.assertEqual("xumm", stmt.table_name.expr.name)
        self.assertEqual("xumm1", stmt.table_name.alias)

        # inner join
        sql = "select 1 from xumm as xumm1 " \
              "inner join xumm2 on xumm1.id = xumm2.id2 " \
              "left join xumm3 on xumm2.id2 = xumm3.id3 " \
              "right outer join xumm4"
        parser = create_parser(sql)
        stmt = parser.parse_select()
        self.assertEqual("select", stmt.type)
        self.assertTrue(isinstance(stmt.table_name, JoinTableSource))
        self.assertTrue(isinstance(stmt.table_name.left, JoinTableSource))
        self.assertTrue(isinstance(stmt.table_name.right, TableSource))
        self.assertTrue(isinstance(stmt.table_name.left.left, JoinTableSource))
        self.assertTrue(isinstance(stmt.table_name.left.left.left, TableSource))

        self.assertEqual("xumm4", stmt.table_name.right.expr.name)
        self.assertIsNone(stmt.table_name.right.alias)

        self.assertEqual("xumm3", stmt.table_name.left.right.expr.name)
        self.assertIsNone(stmt.table_name.left.right.alias)

        self.assertEqual("xumm2", stmt.table_name.left.left.right.expr.name)
        self.assertIsNone(stmt.table_name.left.left.right.alias)

        self.assertEqual("xumm", stmt.table_name.left.left.left.expr.name)
        self.assertEqual("xumm1", stmt.table_name.left.left.left.alias)

    def test_parse_mutliple_statements(self):
        sql = "select 1 from xumm as xumm1;create table xumm(id int, name string, age int);select 2 from xumm"
        parser = create_parser(sql)
        stmts = parser.parse()
        self.assertEqual(3, len(stmts))
        self.assertEqual("select", stmts[0].type)
        self.assertEqual("create", stmts[1].type)
        self.assertEqual("select", stmts[2].type)
