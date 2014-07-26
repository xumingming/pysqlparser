class Token:
    def __init__(self, name):
        """
        """
        self.name = name
        
    def __str__(self):
        return "[" + self.name + "]"

# sql keywords
ADD = Token("ADD")
AND = Token("AND")
ALL = Token("ALL")
ALTER = Token("ALTER")
AS = Token("AS")
ASC = Token("ASC")
BETWEEN = Token("BETWEEN")
BIGINT = Token("BIGINT")
BOOLEAN = Token("BOOLEAN")
BY = Token("BY")
CASE = Token("CASE")
CAST = Token("CAST")
COLUMN = Token("COLUMN")
COMMENT = Token("COMMENT")
CREATE = Token("CREATE")
DESC = Token("DESC")
DISTINCT = Token("DISTINCT")
DISTRIBUTE = Token("DISTRIBUTE")
DOUBLE = Token("DOUBLE")
DROP = Token("DROP")
ELSE = Token("ELSE")
FALSE = Token("FALSE")
FROM = Token("FROM")
FULL = Token("FULL")
GROUP = Token("GROUP")
IF = Token("IF")
IN = Token("IN")
INSERT = Token("INSERT")
INTO = Token("INTO")
IS = Token("IS")
JOIN = Token("JOIN")
LEFT = Token("LEFT")
LIFECYCLE = Token("LIFECYCLE")
LIKE = Token("LIKE")
LIMIT = Token("LIMIT")
MAPJOIN = Token("MAPJOIN")
NOT = Token("NOT")
NULL = Token("NULL")
ON = Token("ON")
OR = Token("OR")
ORDER = Token("ORDER")
OUTER = Token("OUTER")
OVERWRITE = Token("OVERWRITE")
PARTITION = Token("PARTITION")
RENAME = Token("RENAME")
REPLACE = Token("REPLACE")
RIGHT = Token("RIGHT")
RLIKE = Token("RLIKE")
SELECT = Token("SELECT")
SORT = Token("SORT")
STRING = Token("STRING")
TABLE = Token("TABLE")
THEN = Token("THEN")
TOUCH = Token("TOUCH")
TRUE = Token("TRUE")
UNION=Token("UNION")
VIEW = Token("VIEW")
WHEN = Token("WHEN")
WHERE = Token("WHERE")

# operators
STAR = Token("*")
QUES = Token("?")
SEMI = Token(";")
PLUS = Token("+")
MINUS = Token("-")
MULTIPLY = Token("*")
DIVIDE = Token("/")
COMMA = Token(",")
LPAREN = Token("(")
RPAREN = Token(")")
LBRACKET = Token("[")
RBRACKET = Token("]")
LBRACE = Token("{")
RBRACE = Token("}")
DOT = Token(".")



# specials
EOF = Token("EOF")
LITERAL_INT = Token("INT")
LITERAL_FLOAT = Token("FLOAT")

# miscs
NUMBER = Token("NUM")
IDENTIFIER = Token("IDENFIER")
