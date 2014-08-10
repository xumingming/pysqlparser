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
        select id as id1, name name1, age from xumm
        where id > 1 and name > 'hello' or age <> 10 and id not in (1, 2, 3, 4)
        or id in (select id from ids where id in (select id1 from ids1 where id2 in (select id from hello)))
        and cnt in (select name from xumm)""")
        #parser = create_parser("select id from xumm where id not in (1,2,3)")
        stmt = parser.parse()
        #print stmt.where.right.operator.name
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

    def test_it(self):
        sql = """select id, name, age, *
        from xumm.table1 a
        where a.id ='1234'
              and a.dt='20140807'"""

        #self.helper(sql)
        parser = create_parser(sql)
        stmt = parser.parse()
        visitor = AstVisitor()
        visitor.visit(stmt)
        print "".join([str(x) for x in visitor.buf])

    def test_visit_method(self):
        sql = """select count(a.atn) from xumm"""
        parser = create_parser(sql)
        stmt = parser.parse()
        visitor = AstVisitor()
        visitor.visit(stmt)
        print "".join([str(x) for x in visitor.buf])

    def test_2(self):
        sql = """select count(a.atn) from
            (select distinct id as id1, name
            from xumm.table1
            where name = 'james'  and tag = 'bond'
             and   to_date(gmt_create,'yyyy-mm-dd')  <  to_date('2014-04-01','yyyy-mm-dd') and dt='20140807') a
             join
            (select id as id1 from xumm.table2
            where name = '600' and to_date(gmt_create,'yyyy-mm-dd')  <  to_date('2014-04-01','yyyy-mm-dd') and dt='joke') b
            on a.atn=b.btn"""

        parser = create_parser(sql)
        stmt = parser.parse()
        visitor = AstVisitor()
        visitor.visit(stmt)
        print "".join([str(x) for x in visitor.buf])


