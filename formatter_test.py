import unittest
from lexer import Lexer
from parser import Parser
from token1 import *
from formatter import Formatter
from ast_visitor import AstVisitor

def create_parser(sql):
    return Parser(sql)

def create_formatter(sql):
    return Formatter(sql)

class ParserTestCase(unittest.TestCase):
    def helper(self, sql):
        print "SQL: ", sql
        lexer = Lexer(sql)
        lexer.next_token()
        while lexer.token.name != EOF.name:
            print lexer.info()
            lexer.next_token()

    def test_select(self):
        parser = create_parser("""
        select id, name, age from xumm""")
        stmt = parser.parse()
        visitor = AstVisitor()
        visitor.visit(stmt)
        print "".join([str(x) for x in visitor.buf])

    def test_create(self):
        parser = create_parser("""
        create table if not exists xumm (id int comment 'test', name string comment 'this is name', age int comment 'what a fuck comment')
        comment 'hello table' partitioned by (c1 int, c2 string) lifecycle 1""")
        stmt = parser.parse()
        visitor = AstVisitor()
        visitor.visit(stmt)
        print "".join([str(x) for x in visitor.buf])

        
