# Generated from Decaf.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DecafParser import DecafParser
else:
    from DecafParser import DecafParser

# This class defines a complete generic visitor for a parse tree produced by DecafParser.

class DecafVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by DecafParser#program.
    def visitProgram(self, ctx:DecafParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#declaration.
    def visitDeclaration(self, ctx:DecafParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#varDeclaration.
    def visitVarDeclaration(self, ctx:DecafParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#structDeclaration.
    def visitStructDeclaration(self, ctx:DecafParser.StructDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#varType.
    def visitVarType(self, ctx:DecafParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:DecafParser.MethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#methodType.
    def visitMethodType(self, ctx:DecafParser.MethodTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#parameter.
    def visitParameter(self, ctx:DecafParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#parameterType.
    def visitParameterType(self, ctx:DecafParser.ParameterTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#block.
    def visitBlock(self, ctx:DecafParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#statement.
    def visitStatement(self, ctx:DecafParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#location.
    def visitLocation(self, ctx:DecafParser.LocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expression.
    def visitExpression(self, ctx:DecafParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#methodCall.
    def visitMethodCall(self, ctx:DecafParser.MethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#arg.
    def visitArg(self, ctx:DecafParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#op.
    def visitOp(self, ctx:DecafParser.OpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#arith_op.
    def visitArith_op(self, ctx:DecafParser.Arith_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#rel_op.
    def visitRel_op(self, ctx:DecafParser.Rel_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#eq_op.
    def visitEq_op(self, ctx:DecafParser.Eq_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#cond_op.
    def visitCond_op(self, ctx:DecafParser.Cond_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#literal.
    def visitLiteral(self, ctx:DecafParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#int_literal.
    def visitInt_literal(self, ctx:DecafParser.Int_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#char_literal.
    def visitChar_literal(self, ctx:DecafParser.Char_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#bool_literal.
    def visitBool_literal(self, ctx:DecafParser.Bool_literalContext):
        return self.visitChildren(ctx)



del DecafParser