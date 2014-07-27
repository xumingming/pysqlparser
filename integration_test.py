import unittest
from lexer import Lexer
from token import *

def create_lexer(sql):
    return Lexer(sql)

class IntegrationTestCase(unittest.TestCase):
    def test_comment_and_select(self):
        sql = """
        -- this is a comment
        select * from xumm;
        """
        lexer = create_lexer(sql)
        tokens = lexer.tokens()
        self.assertEquals([LITERAL_COMMENT, SELECT, STAR,
                           FROM, IDENTIFIER, SEMI], tokens)
