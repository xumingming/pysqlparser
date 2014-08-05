from token import *
from utils import *
from keywords import get_keyword
from exception import EofException, InvalidCharException

class Lexer:
    def __init__(self, sql):
        self.sql = sql
        self.ch = None
        self.token = None
        self.pos = -1

        self.mark = -1
        self.buf_pos = 0
        self.token_str = None

        self.scan_char()

    def scan_number(self):
        self.mark = self.pos
        self.buf_pos = 0
        is_float = False
        while is_digit(self.ch):
            self.buf_pos += 1
            self.scan_char()
        
        if self.ch == '.' and is_digit(self.char_at(self.pos + 1)):
            is_float = True
            self.scan_char()
            
            while is_digit(self.ch):
                self.buf_pos += 1
                self.scan_char()
            
        if not is_whitespace(self.ch) and self.ch != None:
            raise InvalidCharException("scan_number: invalid char: " + str(self.ch))

        if is_float:
            self.token = LITERAL_FLOAT
        else:
            self.token = LITERAL_INT
        self.token_str = self.sql[self.mark:self.mark + self.buf_pos + 1]
        debug("scanning number: ", self.token_str)


    def scan_identifier(self):
        debug("scanning identifier: ch:", self.ch)
        self.mark = self.pos
        self.buf_pos = 0
        c = self.char_at(self.pos)
        while is_identifier_char(c):
            self.pos += 1
            c = self.char_at(self.pos)
            self.ch = c
            self.buf_pos += 1


        self.token_str = self.sql[self.mark:self.mark + self.buf_pos]
        tok = get_keyword(self.token_str.upper())
        if tok != None:
            self.token = tok
        else:
            self.token = IDENTIFIER

        debug("scanning identifier: ", self.token)

    def scan_operator(self):
        if self.ch == '+':
            self.scan_char()
            self.token = PLUS
            self.token_str = '+'
        elif self.ch == '-':
            self.scan_char()
            self.token = MINUS
            self.token_str = '-'
        elif self.ch == '*':
            self.scan_char()
            self.token = STAR
            self.token_str = '*'
        elif self.ch == '/':
            self.scan_char()
            self.token = SLASH
            self.token_str = '/'            
        elif self.ch == '=':
            self.scan_char()
            self.token = EQ
            self.token_str = '='
        elif self.ch == '>':
            self.scan_char()
            if self.ch == '=':
                self.token = GTEQ
                self.token_str = '>='
            else:
                self.token = GT
                self.token_str = '>'
        elif self.ch == '<':
            self.scan_char()()
            if self.ch == '=':
                self.token = LTEQ
                self.token_str = '<='
                return
            elif self.ch == '>':
                self.token = NEQ
                self.token_str = '<>'
                return
            else:
                self.token = LT
                self.token_str = '<'
        elif self.ch == '?':
            self.token = QUES
            self.token_str = '?'
        else:
            raise InvalidCharException("invalid char: " + self.ch)

        debug("scanning operator: ", self.ch)

    def scan_comment(self):
        if self.ch != '-':
            raise InvalidCharException("invalid char: " + self.ch)

        self.scan_char()
        if self.ch != '-':
            raise InvalidCharException("not a valid comment: " + self.ch)
        self.mark = self.pos + 1
        self.buf_pos = 0
        while self.ch != '\n' and self.ch != None:
            self.scan_char()
            self.buf_pos += 1

        self.token = LITERAL_COMMENT
        self.token_str = self.sql[self.mark : self.mark + self.buf_pos]
        
    def char_at(self, i):
        """
        """
        ret = None
        if i < len(self.sql):
            ret = self.sql[i]

        debug("char_at: i:", i, ", None, sql: ", self.sql)
        return ret
    def unscan(self):
        self.pos -= 1
        self.ch = self.sql[self.pos]

    def scan_string(self):
        self.scan_char()
        self.mark = self.pos
        self.buf_pos = 0

        while True:
            debug("in scan_string, ch: ", self.ch, "=? ", self.ch == "'")
            if self.ch == '\n':
                raise InvalidCharException("uncompleted string")
            if self.ch == "'":
                break
            else:
                self.buf_pos += 1
                self.scan_char()

        self.scan_char()
        self.token = LITERAL_STRING
        self.token_str = self.sql[self.mark : self.mark + self.buf_pos]

    def next_token(self):
        debug("next_token: ch: ", self.ch)
        while True:
            if is_whitespace(self.ch):
                self.scan_char()
                continue

            if is_first_identifier_char(self.ch):
                self.scan_identifier()
                return
                
            if is_digit(self.ch):
                self.scan_number()
                return
            
            if self.ch == '0':
                if self.char_at(self.pos + 1) == 'x':
                    self.scan_char()
                    self.scan_char()
                    self.scan_hex_decimal()
                else:
                    self.scan_number()
                return

            if (self.ch == '1' or self.ch == '2' or self.ch == '3' or
                self.ch == '4' or self.ch == '5' or self.ch == '6' or
                self.ch == '7' or self.ch == '8' or self.ch == '9'):
                self.scan_number()
                return

            if self.ch == ',':
                self.scan_char()
                self.token = COMMA
                self.token_str = ','
                return

            if self.ch == '(':
                self.scan_char()
                self.token = LPAREN
                self.token_str = '('
                return

            if self.ch == ')':
                self.scan_char()
                self.token = RPAREN
                self.token_str = ')'
                return
            if self.ch == '\'':
                self.scan_string()
                return
            if self.ch == ';':
                self.scan_char()
                self.token = SEMI
                self.token_str = ';'
                return
            if self.ch == '*':
                self.scan_char()
                self.token = STAR
                self.token_str = '*'
                return
            elif self.ch == '+':
                self.scan_char()
                self.token = PLUS
                self.token_str = '+'
                return
            elif self.ch == '-':
                next_char = self.char_at(self.pos + 1)
                if next_char == '-':
                    self.scan_comment()
                else:
                    self.scan_operator()

                return
            elif self.ch == '/':
                self.scan_char()
                self.token = SLASH
                self.token_str = '/'
                return
            elif self.ch == '.':
                self.scan_char()
                if is_digit(self.ch):
                    self.unscan()
                    self.scan_number()
                else:
                    self.token = DOT
                    self.token_str = '.'
                return
            else:
                debug("next_token, in the ELSE branch")
                if is_first_identifier_char(self.ch):
                    self.scan_identifier()
                    return
                if is_operator(self.ch):
                    self.scan_operator()
                    return

                if self.is_eof():
                    debug("it is end of file, ch: ", self.ch, ", pos: ", self.pos)
                    self.token = EOF
                else:
                    print "invalid char: '", self.ch, "'"
                    raise InvalidCharException("invalid char: " + self.ch)

                return

    def scan_char(self):
        self.pos += 1
        self.ch = self.char_at(self.pos)
        self.token_str = self.ch
        debug("scanning char:", self.ch, ", pos: ", self.pos)

    def info(self):
        return "%s %s" % (self.token, self.token_str)

    def surroudings(self):
        start_idx = self.pos
        cnt = 20
        while start_idx >= 0 and cnt > 0:
            start_idx -= 1
            cnt -= 1

        end_idx = self.pos
        cnt = 20
        while end_idx < len(self.sql) and cnt > 0:
            end_idx += 1
            cnt -= 1

        ret = []
        ret.append(self.sql[start_idx:end_idx])
        ret.append("\n")
        for i in range(0, self.pos - start_idx):
            ret.append(" ")
        ret.append("^")

        return "".join(ret)

    def is_eof(self):
        return self.pos >= len(self.sql)

    def tokens(self):
        try:
            ret = []
            self.next_token()
            while self.token.name != EOF.name:
                ret.append(self.token)
                self.next_token()

            return ret
        except InvalidCharException,e:
            print e.msg
            raise e

    def token_strs(self):
        try:
            ret = []
            self.next_token()
            while self.token.name != EOF.name:
                ret.append(self.info())
                self.next_token()

            return ret
        except InvalidCharException,e:
            print e.msg
            raise e
