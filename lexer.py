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
        self.string_val = None

        self.scan_char()

    def scan_number(self):
        self.mark = self.pos
        while '9' >= self.ch >= '0':
            self.pos += 1
            self.buf_pos += 1
            self.scan_char()

        if self.ch != ' ':
            raise InvalidCharException("invalid char: " + str(self.ch))

        self.string_val = self.sql[self.mark:self.mark + self.buf_pos]
        self.token = NUMBER

    def scan_identifier(self):
        self.mark = self.pos
        self.buf_pos = 0
        c = self.char_at(self.pos)
        while is_identifier_char(c):
            self.pos += 1
            c = self.char_at(self.pos)
            self.ch = c
            self.buf_pos += 1


        self.string_val = self.sql[self.mark:self.mark + self.buf_pos]
        tok = get_keyword(self.string_val.upper())
        if tok != None:
            self.token = tok
        else:
            self.token = IDENTIFIER

    def scan_operator(self):
        while True:
            if self.ch == '*':
                self.token = STAR
    def scan_comment(self):
        pass

    def char_at(self, i):
        """
        """
        if i >= len(self.sql):
            return EOF
        return self.sql[i]

    def scan_string(self):
        if self.is_eof():
            raise

    def next_token(self):
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
                self.string_val = ','
                return;

            if self.ch == '(':
                self.scan_char()
                self.token = LPAREN
                self.string_val = '('
                return

            if self.ch == ')':
                self.scan_char()
                self.token = RPAREN
                self.string_val = ')'
                return
            if self.ch == '\'':
                self.scan_string()
                return

            if self.ch == '*':
                self.scan_char()
                self.token = STAR
                self.string_val = '*'
                return
            elif self.ch == '+':
                self.scan_char()
                self.token = PLUS
                self.string_val = '+'
                return
            elif self.ch == '-':
                self.scan_char()
                self.token = MINUS
                self.string_val = '-'
                return
            elif self.ch == '/':
                self.scan_char()
                self.token = DIVIDE
                self.string_val = '/'
                return
            else:
                if ('a' <= self.ch <= 'z'
                    or 'A' <= self.ch <= 'Z'):
                    self.scan_identifier()
                    return
                if is_operator(self.ch):
                    self.scan_operator()
                    return

                if self.is_eof():
                    self.token = EOF
                else:
                    print "invalid char: '", self.ch, "'"
                    raise InvalidCharException("invalid char: " + self.ch)

                return

    def scan_char(self):
        self.pos += 1
        self.ch = self.char_at(self.pos)
        self.string_val = self.ch
        debug("scanning char:", self.ch, ", pos: ", self.pos)

    def info(self):
        if self.token == IDENTIFIER:
            print self.token, self.string_val
        else:
            print self.token, self.string_val

    def is_eof(self):
        return self.pos >= len(self.sql)

    def tokens(self):
        try:
            ret = []
            self.next_token()
            while self.token != EOF:
                ret.append(self.token)
                self.next_token()

                return ret
        except InvalidCharException,e:
            print e.msg
            raise e
