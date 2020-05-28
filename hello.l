%{
	#include <stdio.h> 
	#include <string.h>
  #include <stdlib.h>
	#include "hello.tab.h"
	

	
  void InvalidToken();
%}

whitespace      [ \t\r\v\f]
linefeed        \n

%%

"num" 				{ yylval.dataType = strdup(yytext); return DATA_TYPE;	}
"float"	 			{ yylval.dataType = strdup(yytext); return DATA_TYPE;	}
"wd"	 		{ yylval.dataType = strdup(yytext); return DATA_TYPE;	}
"char"				{ yylval.dataType = strdup(yytext); return DATA_TYPE;	}
"if"        return IF;
"else"      return ELSE;
"and"       return AND;
"or"        return OR;
"while"     return WHILE;
"for"       return FOR;
"void"      return VOID;
"return"    return RETURN;
"print"			return PRINT;
"id"		return ID;

[\'][a-zA-Z0-9][\']         {yylval.character = yytext[1];   return CHAR;}
[-+]?[0-9]+                 {yylval.integer = atoi(yytext);  return INT;}
[-+]?[0-9]*\.?[0-9]+        {yylval.number = atof(yytext); 	 return FLOAT;}
[a-zA-Z][_a-zA-Z0-9]*       {yylval.dataType = strdup(yytext); return IDENTIFIER;}
\"(\\.|[^"])*\"             {yylval.string = strdup(yytext); return STRING;}

"="						          return ASSIGN;
"=="				          	return EQUALS;
"!="			          		return NOTEQUAL;
"<"				          		return LESS;
"<="	          				return LESSOREQUAL;
">"				          		return GREATER;
">="					          return GREATEROREQUAL;
"("	          					return LPAREN;
")"					          	return RPAREN;
"{"         						return LBRACE;
"}"					          	return RBRACE;
"."         						return DOT;
","				          		return COMMA;
";"                     return SEMICOLON;
"+"				          		return ADD;
"-"		          				return MINUS;
"*"		          				return MUL;
"/"				          		return DIV;
\/\/.*						;


{linefeed}                  {yylineno++;}
{whitespace}                ;
.							{InvalidToken();}
%%

int yywrap(void){
    return 1;
}

 void yyerror (char const *s) {
   fprintf (stderr, "%s\n", s);
 }

void InvalidToken(){
    printf("ERROR ON LINE %d : Invalid Token %s\n", yylineno, yytext);
    exit(0);
}
