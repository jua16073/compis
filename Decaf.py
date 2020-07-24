from antlr4 import *
import antlr4
from DecafLexer import DecafLexer
from DecafListener import DecafListener
from DecafParser import DecafParser
from antlr4.tree.Trees import Trees
import sys

class DecafPrintListener(DecafListener):
    pass
    # def enterProgram(self, ctx):
    #     print("Decaf: %s" % ctx.ID())

def main():
    program = open('help.txt', 'r+')
    text = program.read()
    program.close()
    text = antlr4.InputStream(text)
    lexer = DecafLexer(text)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()
    printer = DecafPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    print(Trees.toStringTree(tree, None, parser))

if __name__ == '__main__':
    main()
