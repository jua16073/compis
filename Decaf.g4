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

structDeclaration: 'struct' ID '{' (varDeclaration)* '}' ';';

varType: 'int' | 'char' | 'boolean' | 'struct' ID | structDeclaration | 'void';

methodDeclaration: methodType ID '(' (parameter | parameter (',' parameter)*)?  ')' block ;

methodType: 'int' | 'char' | 'boolean' | 'void';

parameter: parameterType ID | parameterType ID '[' ']';

parameterType: 'int' | 'char' | 'boolean';

block: '{' (varDeclaration)* (statement)* '}';

statement: 'if' '(' expression ')' block1 = block ('else' block2 = block)? #ifScope
        | 'while' '(' expression ')' block #whileScope
        | 'return' (expression)? ';' #stmnt_return
        | methodCall ';' #stmnt_methodCall
        | block #stmnt_block
        | left = location '=' right = expression #stmnt_equal
        | (expression)? ';' #stmnt_expression; 

location: (ID | ID '[' expression ']' ) ('.' location)?;

expression: methodCall #expr_methodCall | location #expr_location  | literal #expr_literal
        | '(' expression ')' #expr_par
        | '-' expression #expr_minus
        | '!' expression #expr_not
        | left = expression p_arith_op right = expression #expr_arith_op
        | left = expression arith_op right = expression #expr_op
        | left = expression rel_op right = expression #expr_rel_op
        | left = expression eq_op right = expression #expr_eq_op
        | left = expression cond_op right = expression #expr_cond_op;
        

methodCall: ID '(' (arg | arg (',' arg)*)?    ')';

arg: expression;

//op: arith_op | rel_op | eq_op | cond_op;

arith_op: '+' | '-' ;

p_arith_op: '*' | '/' | '%';

rel_op: '<' | '>' | '<=' | '>=';

eq_op: '==' | '!=';

cond_op: '&&' | '||';

literal: int_literal | char_literal | bool_literal;
int_literal: NUM;
char_literal: CHAR; 
bool_literal: 'true' | 'false';
