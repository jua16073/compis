from DecafVisitor import DecafVisitor

class Inter(DecafVisitor):

    def __init__(self):
        DecafVisitor.__init__(self)
        self.tree = None
        self.og_registers = ["r0", "r1","r2", "r3", "r4", "r5", "r6", "r7"]
        self.registers = self.og_registers[::-1]
        self.line = ""

    def visitProgram(self, ctx):
        self.visitChildren(ctx)
        return 

    def visitMethodDeclaration(self, ctx):
        name = ctx.ID().getText()
        start = "func begin " + name + "\n"
        self.line += start
        self.visitChildren(ctx)
        end = "func end \n"
        self.line += end
        return 0

    def visitExpr_op(self, ctx):
        print(ctx.left.getText())
        print(ctx.right.getText())
        print("/////////////////////")
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        register = self.registers.pop()
        operation = register + "=" + left + ctx.arith_op().getText() + right
        if left in self.og_registers:
            self.og_registers.append(left)
        if right in self.og_registers:
            self.og_registers.append(right)

        self.line += operation + "\n"
        self.visitChildren(ctx)
        return register

    def visitExpr_literal(self, ctx):
        return self.visitChildren(ctx)

    def visitLiteral(self, ctx):
        val = self.visitChildren(ctx)
        return val[1]
    
    def visitInt_literal(self, ctx):
        num = ctx.NUM()
        return ("int", (num.getText()))
    
    def visitChar_literal(self, ctx):
        char = ctx.CHAR()
        return ("char", char.getText())
    
    def visitBool_literal(self, ctx):
        boolean = ctx.getText()
        return ("boolean", boolean)

    def visitStmnt_equal(self, ctx):
        self.visitChildren(ctx)
        return 
