from antlr4 import *
from DecafLexer import DecafLexer
from DecafListener import DecafListener
from DecafParser import DecafParser
from antlr4.tree.Trees import Trees
import sys

class DecafPrintListener(DecafListener):
    def enterProgram(self, ctx):
        print("Decaf: %s" % ctx.ID())

def main():
    lexer = DecafLexer(StdinStream())
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()
    print(Trees.toStringTree(tree, None, parser))
    printer = DecafPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

if __name__ == '__main__':
    main()
