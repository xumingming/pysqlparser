# -*- encoding: utf-8 -*-
DEBUG = False

def is_whitespace(ch):
    ret = (ch == ' ' or ch == '\t' or ch == '\r'
            or ch == '\n')
    return ret

def is_first_identifier_char(ch):
    """
    Whether the specified char is the head of an identifier
    """
    if not ch:
        return False

    ret = (('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ch == '`' or ch == '_' or ch == '$'
           or (ord(ch) > 256 and ch != ' ' and ch != '，'))
    return ret

def is_identifier_char(ch):
    """
    Whether the specified char is the head of an identifier
    """
    if not ch:
        return False

    ret = (('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ('0' <= ch <= '9') or ch == '`' or ch == '_' or ch == '$'
           or (ord(ch) > 256 and ch != ' ' and ch != '，'))
    return ret


def is_digit(ch):
    """
    is the specified char a digit
    """
    return '0' <= ch <= '9'

def is_operator(ch):
    """
    """
    return (ch == '*' or ch == '+' or ch == '-'
            or ch == '/' or ch == '<' or ch == '>'
            or ch == '=')
    
def debug(*args):
    """
    """
    if DEBUG:
        print "".join([str(x) for x in args])

