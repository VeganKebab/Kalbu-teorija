%{
    #include <string>
    #include <stdio.h>
    #include "node.h"
    #include "parser.hpp"
%}

numbers ([0-9])+
word ([a-zA-Z])+

%%

{word}                 {sscanf(yytext, "%s", yylval.name); return (STRING);}
{numbers}              {yylval.number = atoi(yytext); return (NUM);}
" "                    {return (SPACE);}
.                       printf("Unknown token!n"); yyterminate();
"="                     return TOKEN(TEQUAL);
"=="                    return TOKEN(TCEQ);
"!="                    return TOKEN(TCNE);
"<"                     return TOKEN(TCLT);
"<="                    return TOKEN(TCLE);
">"                     return TOKEN(TCGT);
">="                    return TOKEN(TCGE);
"("                     return TOKEN(TLPAREN);
")"                     return TOKEN(TRPAREN);
"{"                     return TOKEN(TLBRACE);
"}"                     return TOKEN(TRBRACE);
"."                     return TOKEN(TDOT);
","                     return TOKEN(TCOMMA);
"+"                     return TOKEN(TPLUS);
"-"                     return TOKEN(TMINUS);
"*"                     return TOKEN(TMUL);
"/"                     return TOKEN(TDIV);

%%