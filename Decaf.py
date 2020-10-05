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

#program = open('help.txt', 'r+')
program = open('final.txt', "r+")
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
print(Visitor.ERRORS)
    

