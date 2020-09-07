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


    # Visit a parse tree produced by DecafParser#normalVar.
    def visitNormalVar(self, ctx:DecafParser.NormalVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#arrayVar.
    def visitArrayVar(self, ctx:DecafParser.ArrayVarContext):
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


    # Visit a parse tree produced by DecafParser#ifScope.
    def visitIfScope(self, ctx:DecafParser.IfScopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#whileScope.
    def visitWhileScope(self, ctx:DecafParser.WhileScopeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#stmnt_return.
    def visitStmnt_return(self, ctx:DecafParser.Stmnt_returnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#stmnt_methodCall.
    def visitStmnt_methodCall(self, ctx:DecafParser.Stmnt_methodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#stmnt_block.
    def visitStmnt_block(self, ctx:DecafParser.Stmnt_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#stmnt_equal.
    def visitStmnt_equal(self, ctx:DecafParser.Stmnt_equalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#stmnt_expression.
    def visitStmnt_expression(self, ctx:DecafParser.Stmnt_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#location.
    def visitLocation(self, ctx:DecafParser.LocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_cond_op.
    def visitExpr_cond_op(self, ctx:DecafParser.Expr_cond_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_location.
    def visitExpr_location(self, ctx:DecafParser.Expr_locationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_literal.
    def visitExpr_literal(self, ctx:DecafParser.Expr_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_op.
    def visitExpr_op(self, ctx:DecafParser.Expr_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_eq_op.
    def visitExpr_eq_op(self, ctx:DecafParser.Expr_eq_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_minus.
    def visitExpr_minus(self, ctx:DecafParser.Expr_minusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_par.
    def visitExpr_par(self, ctx:DecafParser.Expr_parContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_arith_op.
    def visitExpr_arith_op(self, ctx:DecafParser.Expr_arith_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_rel_op.
    def visitExpr_rel_op(self, ctx:DecafParser.Expr_rel_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_methodCall.
    def visitExpr_methodCall(self, ctx:DecafParser.Expr_methodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#expr_not.
    def visitExpr_not(self, ctx:DecafParser.Expr_notContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#methodCall.
    def visitMethodCall(self, ctx:DecafParser.MethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#arg.
    def visitArg(self, ctx:DecafParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#arith_op.
    def visitArith_op(self, ctx:DecafParser.Arith_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DecafParser#p_arith_op.
    def visitP_arith_op(self, ctx:DecafParser.P_arith_opContext):
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