%option noyywrap
%option yylineno

%{
#include <string>
#include <sstream>
#include "expression.h"
#include "function.h"
#include "statement.h"
#include "parse.tab.h"

using std::string;
using std::istringstream;

extern void yyerror(const char*, char);
%}

ident [_a-zA-Z][_0-9a-zA-Z]*
int   [0-9]+
float [0-9]*\.[0-9]+

%%

"#"[^\r\n]* { /* comments */    }
[ \t\n]     { /* whitespace */  }
"+"         { return yytext[0]; }
"-"         { return yytext[0]; }
"*"         { return yytext[0]; }
"/"         { return yytext[0]; }
"%"         { return yytext[0]; }
"^"         { return yytext[0]; }
"("         { return yytext[0]; }
")"         { return yytext[0]; }
"="         { return yytext[0]; }
":"         { return yytext[0]; }
","         { return yytext[0]; }
"<"         { return yytext[0]; }
">"         { return yytext[0]; }
"+="        { return PLUSEQ;    }
"-="        { return MINUSEQ;   }
"*="        { return MULTEQ;    }
"/="        { return DIVEQ;     }
"%="        { return MODEQ;     }
"^="        { return POWEQ;     }
"++"        { return INC;       }
"--"        { return DEC;       }
"<="        { return LE;        }
">="        { return GE;        }
"=="        { return EQ;        }
"!="        { return NE;        }
"if"        { return IF;        }
"else"      { return ELSE;      }
"def"       { return DEF;       }
"while"     { return WHILE;     }
"print"     { return PRINT;     }
"end"       { return END;       }
"return"    { return RETURN;    }

{ident}  { yylval.ident = new char[strlen(yytext)+1];
           strcpy(yylval.ident, yytext);
           return IDENT;
         }

{float}  { istringstream(string(yytext)) >> yylval.floatVal;
           return FLOATNUM;
         }

{int}    { istringstream(string(yytext)) >> yylval.intVal;
           return INTNUM;
         }

.        { yyerror("undefined token", yytext[0]); yyterminate(); }
%%