 %{
int yylex();
void yyerror(const char *s);
%}
%{
#pragma warning(disable : 4996)
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	#include <ctype.h>
	#include "functions.h"
	
	void storeDataType(char*);
	int isDuplicate(char*, char*);
	void storeIdentifier(char*,char*);
	void DuplicateIdentifierError(char*);
	char* retrieveDataType();
	void clearBuffers();
	int isValidAssignment(char*);
	void AssignmentError(char*);
	char* extractIdentifier(char[]);
	
	char* RemoveQuotesFromString(char* str);
%}

%union {
	int integer;
	float number;
	char* string;
	char* dataType;
	char character;
}
%start program

%token IF ELSE AND OR
%token FOR WHILE VOID RETURN
%token <integer> ASSIGN EQUALS NOTEQUAL LESS LESSOREQUAL GREATER GREATEROREQUAL
%token <integer> LPAREN RPAREN LBRACE RBRACE
%token <integer> DOT COMMA SEMICOLON
%token <integer> ADD MINUS MUL DIV

%token PRINT ID

%token <character>  CHARACTER_VALUE
%token <integer>   INTEGER_VALUE
%token <number> FLOAT_VALUE
%token <string> STRING_VALUE


%token <character> CHAR
%token <string> STRING
%token <number> FLOAT
%token <integer> INT
%token <dataType> DATA_TYPE
%token <string> IDENTIFIER

%%

/* descriptions of expected inputs     corresponding actions (in C) */
//statements
program: statements {;}
  ;
  
// statement
statements : statement {;}  // one statment
  | statements statement {;} // more than one statment
  
// expressions for if and else <<<<<<<<<<<<AND WHILE DABA JAU
if_else: expression comparison expression {;} // return true/false
  | expression comparison expression AND if_else {;}
  | expression comparison expression OR if_else {;}
  ;
// statement
statement: var_declaration | func_declaration | selection_declaration | loop_declaration
  | expression {;} // new expression
  | RETURN expression {;} // return expression
  | print_exp {;}
  ;
// PRINT expression
print_exp:  PRINT STRING SEMICOLON {printf("%s\n", $2);}
  ;

// Kodo blokai (funkcijom, if-ui, ciklam)
block:  LBRACE statements RBRACE {;} // block with statements
  | LBRACE RBRACE {;}  // empty block
  ;
  
// variable declaration
var_declaration: IDENTIFIER DATA_TYPE {printf("Function variable %s declared\n", $2);}       
  |   DATA_TYPE expression {;}
  |   IDENTIFIER ASSIGN expression {printf("%s value was changed \n", $1);}
  ;
  
// if statement
selection_declaration: IF if_else block {printf("If(){}.. declared\n");} // if (..) {..}
  | IF if_else block ELSE block {printf("If(){}Else{}.. declared\n");}
  ;
// ciklu aprasymas

loop_declaration: WHILE if_else block {printf("While Block \n");}
   | FOR LPAREN expression SEMICOLON expression RPAREN block{printf("For Loop Block\n");}
  ;
  

// Funkcijos deklaracija
func_declaration: DATA_TYPE IDENTIFIER LPAREN func_args RPAREN block{printf("Function declared with name: \"%s\"\n", $2);}
  ;
// Funkcijos argumentai
func_args:  /* no function args */ {;}
    | var_declaration {;} /* One argument or its a last argument */
    | func_args COMMA var_declaration {;} // many function arguments

    
expression : values {;}
    | IDENTIFIER {;} 
    | IDENTIFIER ASSIGN expression {printf("Variable %s declared\n", $1);}
    | IDENTIFIER LPAREN method_call_args RPAREN {printf("Function %s called \n", $1);} // method calling
    | expression ADD expression {printf("Using addition ");}
    | expression DIV expression {printf("Using division ");}
    | expression MUL expression {printf("Using multiplication ");}
    | expression MINUS expression {printf("Using subtraction ");}
    
// method arguments
method_call_args: /* no args */ {;}
  | expression {;}  // last argument
  | method_call_args COMMA expression {;}
  ;
  
comparison: EQUALS | NOTEQUAL | LESS | GREATER | LESSOREQUAL | GREATEROREQUAL
    ;
			
/* TYPE_SPECIFIER checks, if given DATA_TYPE is equal to given value type*/
values	: STRING {/*if(!isValidAssignment("string")){ AssignmentError("'string'");}*/;}
				| INT {/*if(!isValidAssignment("int")){ AssignmentError("'int'");}*/;}
				| FLOAT {/*if(!isValidAssignment("float")){ AssignmentError("'float'");}*/;}
				| CHAR {/*if(!isValidAssignment("char")){ AssignmentError("'char'");}*/;}
				;
    
%%
/* C code, might need to move to another file. */
char* RemoveQuotesFromString(char* str)
{
	int len = strlen(str);
    sprintf(str, "%.*s", len-2, str + 1);
	return str;
}

int main()
{
   yyparse();
   return 0;
}