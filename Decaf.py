from antlr4 import *
import antlr4
from DecafLexer import DecafLexer
from DecafListener import DecafListener
from DecafParser import DecafParser
from antlr4.tree.Trees import Trees
from DecafVisitor import DecafVisitor
import tablas as Visitor
import sistema_de_tipos as tables
import sys
import intermidate

#program = open('help.txt', 'r+')
#program = open('final.txt', "r+")
program = open('nani.txt', 'r+')
#program = open("test_files/ackerman.decaf", 'r+')
# program = open("test_files/fib.decaf", 'r+')
program = open("test_files/toB.decaf", 'r+')
#program = open("final_boss.txt", "r+")
text = program.read()
program.close()
text = antlr4.InputStream(text)
lexer = DecafLexer(text)
stream = CommonTokenStream(lexer)
parser = DecafParser(stream)
tree = parser.program()
printer = DecafListener()
walker = ParseTreeWalker()
walker.walk(printer, tree)
#print(Trees.toStringTree(tree, None, parser))
nani = Visitor.MyDecafVisitor()
nani.visit(tree)
for error in nani.ERRORS:
    print(error.problem, " in line ", error.line)
#print(nani.total_scopes)
#print(Visitor.ERRORS)
nani = intermidate.Inter(nani.total_scopes)
nani.visit(tree)
print("#############################")
print(nani.line)
#print(nani.registers)
    

