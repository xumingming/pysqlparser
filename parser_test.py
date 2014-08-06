import unittest
from lexer import Lexer
from parser import Parser
from token import *
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

    def test_multiplicative_operator(self):
        sql = "select 1 * 2 / 3 % 4 from xumm"
        parser = create_parser(sql)
        stmt = parser.parse()
        self.assertEqual("select", stmt.type)
        self.assertEqual(1, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0], BinaryOpExpr))
        self.assertTrue(isinstance(stmt.columns[0].left, BinaryOpExpr))
        self.assertEqual(Modulus, stmt.columns[0].operator)
        self.assertTrue(isinstance(stmt.columns[0].right, NumberExpr))
        self.assertEqual(4, stmt.columns[0].right.number)

        self.assertTrue(isinstance(stmt.columns[0].left.left, BinaryOpExpr))
        self.assertEqual(Divide, stmt.columns[0].left.operator)
        self.assertTrue(isinstance(stmt.columns[0].left.right, NumberExpr))
        self.assertEqual(3, stmt.columns[0].left.right.number)

        self.assertTrue(isinstance(stmt.columns[0].left.left.left, NumberExpr))
        self.assertEqual(Multiply, stmt.columns[0].left.left.operator)
        self.assertTrue(isinstance(stmt.columns[0].left.left.right, NumberExpr))
        self.assertEqual(1, stmt.columns[0].left.left.left.number)
        self.assertEqual(2, stmt.columns[0].left.left.right.number)

    def test_additive_operator(self):
        sql = "select 1 + 2 - 3 from xumm"
        parser = create_parser(sql)
        stmt = parser.parse()
        self.assertEqual("select", stmt.type)
        self.assertEqual(1, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0], BinaryOpExpr))
        self.assertTrue(isinstance(stmt.columns[0].left, BinaryOpExpr))
        self.assertEqual(Subtract, stmt.columns[0].operator)
        self.assertTrue(isinstance(stmt.columns[0].right, NumberExpr))
        self.assertEqual(3, stmt.columns[0].right.number)

        self.assertTrue(isinstance(stmt.columns[0].left.left, NumberExpr))
        self.assertEqual(Add, stmt.columns[0].left.operator)
        self.assertTrue(isinstance(stmt.columns[0].left.right, NumberExpr))
        self.assertEqual(1, stmt.columns[0].left.left.number)
        self.assertEqual(2, stmt.columns[0].left.right.number)

    def test_bit_and_operator(self):
        sql = "select 1 & 2 & 3 from xumm"
        parser = create_parser(sql)
        stmt = parser.parse()
        self.assertEqual("select", stmt.type)
        self.assertEqual(1, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0], BinaryOpExpr))
        self.assertTrue(isinstance(stmt.columns[0].left, BinaryOpExpr))
        self.assertEqual(BitwiseAnd, stmt.columns[0].operator)
        self.assertTrue(isinstance(stmt.columns[0].right, NumberExpr))
        self.assertEqual(3, stmt.columns[0].right.number)

        self.assertTrue(isinstance(stmt.columns[0].left.left, NumberExpr))
        self.assertEqual(BitwiseAnd, stmt.columns[0].left.operator)
        self.assertTrue(isinstance(stmt.columns[0].left.right, NumberExpr))
        self.assertEqual(1, stmt.columns[0].left.left.number)
        self.assertEqual(2, stmt.columns[0].left.right.number)

    def test_bit_or_operator(self):
        sql = "select 1 | 2 | 3 from xumm"
        parser = create_parser(sql)
        stmt = parser.parse()
        self.assertEqual("select", stmt.type)
        self.assertEqual(1, len(stmt.columns))
        self.assertTrue(isinstance(stmt.columns[0], BinaryOpExpr))
        self.assertTrue(isinstance(stmt.columns[0].left, BinaryOpExpr))
        self.assertEqual(BitwiseOr, stmt.columns[0].operator)
        self.assertTrue(isinstance(stmt.columns[0].right, NumberExpr))
        self.assertEqual(3, stmt.columns[0].right.number)

        self.assertTrue(isinstance(stmt.columns[0].left.left, NumberExpr))
        self.assertEqual(BitwiseOr, stmt.columns[0].left.operator)
        self.assertTrue(isinstance(stmt.columns[0].left.right, NumberExpr))
        self.assertEqual(1, stmt.columns[0].left.left.number)
        self.assertEqual(2, stmt.columns[0].left.right.number)

    def test_in_rest(self):
        sql = "select id from xumm where id in (1, 2, 3)"

        parser = create_parser(sql)
        stmt = parser.parse()
        self.assertEqual("select", stmt.type)
        self.assertTrue(isinstance(stmt.where, InListExpr))
        self.assertTrue(isinstance(stmt.where.expr, IdentifierExpr))
        self.assertEqual("id", stmt.where.expr.name)
        self.assertEqual(3, len(stmt.where.target_list))
        self.assertTrue(isinstance(stmt.where.target_list[0], NumberExpr))
        self.assertEqual(1, stmt.where.target_list[0].number)
        self.assertTrue(isinstance(stmt.where.target_list[1], NumberExpr))
        self.assertEqual(2, stmt.where.target_list[1].number)
        self.assertTrue(isinstance(stmt.where.target_list[2], NumberExpr))
        self.assertEqual(3, stmt.where.target_list[2].number)

        sql = "select id, name, age from xumm where id in (select id from test)"
        parser = create_parser(sql)
        stmt = parser.parse()
        self.assertTrue(isinstance(stmt.where, InSubQueryExpr))
        self.assertFalse(stmt.where.not1)
        self.assertTrue(isinstance(stmt.where.expr, IdentifierExpr))
        self.assertEqual("id", stmt.where.expr.name)

        sub_query = stmt.where.sub_query
        self.assertEqual(1, len(sub_query.columns))
        self.assertEqual("id", sub_query.columns[0].name)
        self.assertEqual("test", sub_query.table_name)
