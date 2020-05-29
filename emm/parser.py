import ply.yacc as yacc
import emm.ast as ast
from emm.lexeris import *
from emm.exceptions import *

disable_warnings = False

#MAtemetiniu operaciju tvarkos nustatymas
precedence = (
    ('left', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'EXP', 'MOD','TOUPPER'),
    ('right', 'UMINUS'),
    ('right', 'UPLUS'),
)

#YACC gramatines taisykles naudojant Backus Naur forma
#Paruosta pagal PLY bibliotekos dokumentacija


#Teiginiu eile
def p_statement_list(p):
    '''
    statement_list : statement
                   | statement_list statement
    '''
    if len(p) == 2:
        p[0] = ast.InstructionList([p[1]])
    else:
        p[1].children.append(p[2])
        p[0] = p[1]

#Teiginys
def p_statement(p):
    '''
    statement : identifier
              | expression
              | if_statement
    '''
    p[0] = p[1]

#Identifikatorius
def p_identifier(p):
    '''
    identifier : IDENTIFIER
    '''
    p[0] = ast.Identifier(p[1])

#Teiginio uzbaigimas
def p_exit_stmt(p):
    '''
    statement : EXIT STMT_END
    '''
    p[0] = ast.ExitStatement()


#Primityvo apibudinimas
def p_primitive(p):
    '''
    primitive : NUM_INT
              | NUM_FLOAT
              | STRING
              | boolean
    '''
    if isinstance(p[1], ast.BaseExpression):
        p[0] = p[1]
    else:
        p[0] = ast.Primitive(p[1])

#Dvinarine operacija (metematines operacijos)
def p_binary_op(p):
    '''
    expression : expression PLUS expression %prec PLUS
            | expression MINUS expression %prec MINUS
            | expression MUL expression %prec MUL
            | expression DIV expression %prec DIV
            | expression EXP expression %prec EXP
            | expression MOD expression %prec MOD
    '''
    p[0] = ast.BinaryOperation(p[1], p[3], p[2])

#Boolean logikos logika
def p_boolean_operators(p):
    '''
    boolean : expression EQ expression
            | expression NEQ expression
            | expression GT expression
            | expression GTE expression
            | expression LT expression
            | expression LTE expression
            | expression AND expression
            | expression OR expression
    '''
    p[0] = ast.BinaryOperation(p[1], p[3], p[2])

#Unarines operacijos (pvz not operacija)
def p_unary_operation(p):
    '''
    expression : MINUS expression %prec UMINUS
               | PLUS expression %prec UPLUS
               | NOT expression
    '''
    p[0] = ast.UnaryOperation(p[1], p[2])

#String operacijos (papildoma musu kalbos funkcija)
def p_string_op(p):
    '''
    expression : TOUPPER expression
               | TOLOWER expression
               | LNGTH expression
    '''
    p[0] = ast.ToUpper(p[1], p[2])

#Skliausteliu logika
def p_paren(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2] if isinstance(p[2], ast.BaseExpression) else ast.Primitive(p[2])

#Booleanu aprasymas
def p_boolean(p):
    '''
    boolean : TRUE
            | FALSE
    '''
    p[0] = ast.Primitive(p[1])


def p_assignable(p):
    '''
    assignable : primitive
               | expression
    '''
    p[0] = p[1]

#Kableliais atskirti argumentai (funkcijos kvietimai)
def p_comma_separated_expr(p):
    '''
    arguments : arguments COMMA expression
              | expression
              |
    '''
    if len(p) == 2:
        p[0] = ast.InstructionList([p[1]])
    elif len(p) == 1:
        p[0] = ast.InstructionList()
    else:
        p[1].children.append(p[3])
        p[0] = p[1]



def p_arrays(p):
    '''
    expression : LSQBRACK arguments RSQBRACK
    '''
    p[0] = ast.Array(p[2])


def p_array_access(p):
    '''
    expression : identifier LSQBRACK expression RSQBRACK
    '''
    p[0] = ast.ArrayAccess(p[1], p[3])


def p_array_access_assign(p):
    '''
    statement : identifier LSQBRACK expression RSQBRACK EQUALS expression STMT_END
    '''
    p[0] = ast.ArrayAssign(p[1], p[3], p[6])


def p_assign(p):
    '''
    expression : identifier EQUALS assignable STMT_END
    '''
    p[0] = ast.Assignment(p[1], p[3])


def p_ifstatement(p):
    '''
    if_statement : IF expression LBRACK statement_list RBRACK
    '''
    p[0] = ast.If(p[2], p[4])


def p_ifstatement_else(p):
    '''
    if_statement : IF expression LBRACK statement_list RBRACK ELSE LBRACK statement_list RBRACK
    '''
    p[0] = ast.If(p[2], p[4], p[8])


def p_ifstatement_else_if(p):
    '''
    if_statement : IF expression LBRACK statement_list RBRACK ELSE if_statement
    '''
    p[0] = ast.If(p[2], p[4], p[7])

def p_print_statement(p):
    '''
    statement : PRINT arguments STMT_END
    '''
    p[0] = ast.PrintStatement(p[2])


def p_compound_operations(p):
    '''
    statement : identifier PLUS_EQ expression STMT_END
               | identifier MINUS_EQ expression STMT_END
    '''
    p[0] = ast.CompoundOperation(p[1], p[3], p[2])


def p_increment_decrement_identifiers(p):
    '''
    expression : identifier DOUBLE_PLUS
               | identifier DOUBLE_MINUS
    '''
    if p[2] == '++':
        p[0] = ast.BinaryOperation(p[1], ast.Primitive(1), '+')
    else:
        p[0] = ast.BinaryOperation(p[1], ast.Primitive(1), '-')


def p_expression(p):
    '''
    expression : primitive
               | STRING
               | identifier
    '''
    p[0] = p[1]


def p_for_loop(p):
    '''
    statement : FOR identifier IN expression ARROW_LTR expression LBRACK statement_list RBRACK
              | FOR identifier IN expression ARROW_RTL expression LBRACK statement_list RBRACK
    '''
    p[0] = ast.For(p[2], p[4], p[6], p[5] == '->', p[8])


def p_for_loop_in(p):
    '''
    statement : FOR identifier IN expression LBRACK statement_list RBRACK
    '''
    p[0] = ast.ForIn(p[2], p[4], p[6])


def p_function_declaration(p):
    '''
    statement : FUNCTION identifier LPAREN arguments RPAREN LBRACK statement_list RBRACK
              | FUNCTION identifier LBRACK statement_list RBRACK
    '''
    p[2].is_function = True

    if len(p) == 9:
        p[0] = ast.Assignment(p[2], ast.Function(p[4], p[7]))
    else:
        p[0] = ast.Assignment(p[2], ast.Function(ast.InstructionList(), p[4]))


def p_return(p):
    '''
    statement : RETURN expression STMT_END
    '''
    p[0] = ast.ReturnStatement(p[2])


def p_function_call(p):
    '''
    expression : identifier LPAREN arguments RPAREN
    statement : identifier LPAREN arguments RPAREN STMT_END

    '''
    p[1].is_function = True
    p[0] = ast.FunctionCall(p[1], p[3])


def p_error(p):
    if p is not None:
        raise ParserSyntaxError("Syntax error at line %d, illegal token '%s' found" % (p.lineno, p.value))

    raise ParserSyntaxError("Unexpected end of input")


def get_parser():
    return yacc.yacc()