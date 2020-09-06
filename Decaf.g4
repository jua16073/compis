// Grammar of Decaf
// Reserved Keywords:

grammar Decaf;

fragment
DIGIT: [0-9];

fragment
LETTER: [a-zA-Z_];

NUM: DIGIT (DIGIT)* ;


ID: LETTER (LETTER|DIGIT)* ;
CHAR:'\'' LETTER '\'';
SPACES : [ \t\r\n\f]+  ->channel(HIDDEN);
LineComment:   '//' ~[\r\n]*-> skip;

//BLANK: [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

program: 'class' 'Program' '{' (declaration)* '}' EOF;

declaration: structDeclaration | varDeclaration | methodDeclaration;

varDeclaration: varType ID ';' #normalVar | varType ID '[' NUM ']' ';' #arrayVar;

structDeclaration: 'struct' ID '{' (varDeclaration)* '}';

varType: 'int' | 'char' | 'boolean' | 'struct' ID | structDeclaration | 'void';

methodDeclaration: methodType ID '(' (parameter | parameter (',' parameter)*)?  ')' block ;

methodType: 'int' | 'char' | 'boolean' | 'void';

parameter: parameterType ID | parameterType ID '[' ']';

parameterType: 'int' | 'char' | 'boolean';

block: '{' (varDeclaration)* (statement)* '}';

statement: 'if' '(' expression ')' block ('else' block)? #ifScope
        | 'while' '(' expression ')' block #whileScope
        | 'return' (expression)? ';' #stmnt_return
        | methodCall ';' #stmnt_methodCall
        | block #stmnt_block
        | location '=' expression #stmnt_equal
        | (expression)? ';' #stmnt_expression; 

location: (ID | ID '[' expression ']' ) ('.' location)?;

expression: location #expr_location | methodCall #expr_methodCall | literal #expr_literal
        | expression p_arith_op expression #expr_arith_op
        | expression op expression #expr_op
        | '-' expression #expr_minus
        | '!' expression #expr_not
        | '(' expression ')' #expr_par; 

methodCall: ID '(' (arg | arg (',' arg)*)?    ')';

arg: expression;

op: arith_op | rel_op | eq_op | cond_op;

arith_op: '+' | '-' | '%';
p_arith_op: '*' | '/';

rel_op: '<' | '>' | '<=' | '>=';

eq_op: '==' | '!=';

cond_op: '&&' | '||';

literal: int_literal | char_literal | bool_literal;
int_literal: NUM;
char_literal: CHAR; 
bool_literal: 'true' | 'false';
