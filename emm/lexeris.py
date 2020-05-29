import ply.lex as lex
import emm.exceptions
#Python failas aprasantis Lex lexeri

#reserved - Rezervuoti žodžiai, kurių negalime naudoti savo kintamųjų pavadinimuose
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'in': 'IN',
    'exit': 'EXIT',
    'func': 'FUNCTION',
    'return': 'RETURN',
    'print': 'PRINT',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'upp': 'TOUPPER',
    'low': 'TOLOWER',
}

#Tokenų sąrašas
tokens = [
    'KEYWORD',
    'STMT_END',
    'EQUALS',
    'IDENTIFIER',
    'NUM_INT',
    'NUM_FLOAT',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    'COMMA',
    'STRING',
    'NEWLINE',
    'LSQBRACK',
    'RSQBRACK',
    'LNGTH',
    'PLUS',
    'EXP',
    'MINUS',
    'MUL',
    'DIV',
    'MOD',
    'DOUBLE_PLUS',
    'DOUBLE_MINUS',
    'PLUS_EQ',
    'MINUS_EQ',
    'TRUE',
    'FALSE',
    'EQ',
    'NEQ',
    'GT',
    'GTE',
    'LT',
    'LTE',
    'ARROW_LTR',
    'ARROW_RTL'
] + list(reserved.values())

#Nurodome tokneų reikšmes, kai kuriems reikia naudoti regex. Pagal PLY taisykles visi kintamieji turi prasideti t_
t_COMMA = ','
t_PLUS = r'\+'
t_EXP = r'\*\*'
t_MINUS = '-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = '%'
t_STMT_END = ';'
t_EQUALS = '='
t_ignore_WS = r'\s+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = '{'
t_RBRACK = '}'
t_LSQBRACK = r'\['
t_RSQBRACK = r'\]'
t_EQ = '=='
t_NEQ = '!='
t_GT = '>'
t_GTE = '>='
t_LT = '<'
t_LTE = '<='
t_ARROW_LTR = '->'
t_ARROW_RTL = '<-'
t_ignore_COMMENTS = r'//.+'
t_PLUS_EQ = r'\+='
t_MINUS_EQ = r'-='
t_LNGTH = '\#'
t_DOUBLE_PLUS = r'\+\+'
t_DOUBLE_MINUS = '--'


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.linepos = 0
    pass


def t_TRUE(t):
    'true'
    t.value = True
    return t


def t_FALSE(t):
    'false'
    t.value = False
    return t

#Apibudiname indentifikatoriaus forma - zodziai
def t_IDENTIFIER(t):
    r'[\$_a-zA-Z]\w*'

    t.type = reserved.get(t.value, t.type)

    return t


def t_NUM_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t


def t_NUM_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

#String formos apibudinimas
def t_STRING(t):
    r'"(?:\\"|.)*?"'

    # For processing unicode strings
    t.value = bytes(t.value.lstrip('"').rstrip('"'), "utf-8").decode("unicode_escape")

    return t


def t_error(t):
    raise ntp.exceptions.UnexpectedCharacter("Unexpected character '%s' at line %d" % (t.value[0], t.lineno))


lexer = lex.lex()