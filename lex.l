%{
    #include <string>
    #include <stdio.h>
    #include "node.h"
    #include "parser.hpp"
%}

numbers ([0-9])+
word ([a-zA-Z])+

%%

{word}               {sscanf(yytext, "%s", yylval.name); return (STRING);}
{numbers}            {yylval.number = atoi(yytext); return (NUM);}
";"                  {return (SEMICOLON);}
.                       printf("Unknown token!n"); yyterminate();

%%