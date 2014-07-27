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
            
        if self.ch != ' ' and self.ch != None:
            raise InvalidCharException("invalid char: " + str(self.ch))

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
        while True:
            if self.ch == '*':
                self.token = STAR

        debug("scanning operator: ", self.ch)

    def scan_comment(self):
        pass

    def char_at(self, i):
        """
        """
        ret = None
        if i < len(self.sql):
            ret = self.sql[i]

        debug("char_at: i:", i, ", None, sql: ", self.sql)
        return ret

    def scan_string(self):
        self.scan_char()
        self.mark = self.pos
        self.buf_pos = 0

        while True and self.pos < 10:
            debug("in scan_string, ch: ", self.ch, "=? ", self.ch == "'")
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
                self.scan_char()
                self.token = MINUS
                self.token_str = '-'
                return
            elif self.ch == '/':
                self.scan_char()
                self.token = DIVIDE
                self.token_str = '/'
                return
            else:
                debug("next_token, in the ELSE branch")
                if ('a' <= self.ch <= 'z'
                    or 'A' <= self.ch <= 'Z'):
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
