from DecafVisitor import DecafVisitor

DEFAULT_TYPES = {
    'int': 4,
    'boolean': 1,
    'char': 1,
}

class Inter(DecafVisitor):

    def __init__(self, scopes):
        DecafVisitor.__init__(self)
        self.tree = None
        self.og_registers = ["r0", "r1","r2", "r3", "r4", "r5", "r6", "r7"]
        self.registers = self.og_registers[::-1]
        self.line = ""
        self.label = 0
        self.scope_ids = 0
        self.scope_actual = ["global"]
        self.scopes = scopes
        self.cumulative = 0

    def visitProgram(self, ctx):
        self.visitChildren(ctx)
        return 0

    def visitMethodDeclaration(self, ctx):
        name = ctx.ID().getText()
        self.scope_ids +=1
        self.scope_actual.append(name)
        start = name +": \n"
        actual = self.scopes[self.scope_actual[-1]]
        start += "func begin " + str(actual.get_size())  + "\n"
        self.line += start
        self.visitChildren(ctx)
        end = "func end \n"
        self.line += end
        self.scope_actual.pop()
        return 0
    
    def visitStmnt_return(self,ctx):
        if ctx.expression:
            register = self.visit(ctx.expression())
            self.line += "Return " + str(register) + "\n"
            if register in self.og_registers:
                self.registers.append(register)
        return 0

    def visitMethodCall(self, ctx):
        method = ctx.ID().getText()
        if ctx.arg() :
            for arg in ctx.arg():
                param = self.visit(arg)
                self.line += "push param " + param + "\n"
                if param in self.og_registers:
                    self.registers.append(param)
        register = self.registers.pop()
        self.line += register + " = _LCall " + method + "\n"
        if register in self.og_registers:
            self.registers.append(register)
        #self.visitChildren(ctx)
        return 0

    def visitExpr_par(self, ctx):
        return self.visit(ctx.expression())

    def visitWhileScope(self, ctx):
        self.scope_ids += 1
        self.scope_actual.append("while" + str(self.scope_ids))
        start_label = "L" + str(self.label)
        while_line = start_label + ":\n"
        self.label += 1
        self.line += while_line
        register = self.visit(ctx.expression())
        end_label = "L" + str(self.label)
        self.label += 1
        while_cont1 = "IfZ " + register + " Goto " + end_label +" \n"
        if register in self.og_registers:
            self.registers.append(register)
        self.line += while_cont1
        self.visit(ctx.block())
        while_end = "Goto " + start_label + " \n"
        while_end += end_label + ":\n"
        self.line += while_end
        self.scope_actual.pop()
        return 0

    def visitIfScope(self, ctx):
        self.scope_ids += 1
        name = "if" + str(self.scope_ids)
        self.scope_actual.append(name)
        register = self.visit(ctx.expression())
        salto = "L" + str(self.label)
        self.label += 1
        if_line = "IfZ " + register + " Goto " + salto + "\n"
        if register in self.og_registers:
            self.registers.append(register)
        self.line += if_line
        self.visit(ctx.block1)
        if ctx.block2:
            end_line = salto + ": \n"
            end = "L" + str(self.label)
            self.line += "Goto " + end + "\n"
            self.line += end_line
            self.visit(ctx.block2)
            self.line += end + ":\n"
            self.label += 1
        else:
            end_line = salto + ": \n"
            self.line += end_line
        self.scope_actual.pop()
        return 0

    def visitExpr_arith_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        register = self.registers.pop()
        operation = register + "=" + str(left) + ctx.p_arith_op().getText() + str(right)
        if right in self.og_registers:
            self.registers.append(right)
        if left in self.og_registers:
            self.registers.append(left)
        self.line += operation + "\n"
        return register

    def visitExpr_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        register = self.registers.pop()
        operation = register + "=" + str(left) + ctx.arith_op().getText() + str(right)
        if right in self.og_registers:
            self.registers.append(right)
        if left in self.og_registers:
            self.registers.append(left)
        self.line += operation + "\n"
        return register

    def visitExpr_rel_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        register = self.registers.pop()
        operation = register + "=" + left + ctx.rel_op().getText() + right
        if right in self.og_registers:
            self.registers.append(right)
        if left in self.og_registers:
            self.registers.append(left)
        self.line += operation + "\n"
        return register
    
    def visitExpr_eq_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        register = self.registers.pop()
        operation = register + "=" + left + ctx.eq_op().getText() + right
        if right in self.og_registers:
            self.registers.append(right)
        if left in self.og_registers:
            self.registers.append(left)
        self.line += operation + "\n"
        return register

    def visitExpr_cond_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        register = self.registers.pop()
        operation = register + "=" + left + ctx.cond_op().getText() + right
        if right in self.og_registers:
            self.registers.append(right)
        if left in self.og_registers:
            self.registers.append(left)
        self.line += operation + "\n"
        return register

    def visitExpr_literal(self, ctx):
        return self.visitChildren(ctx)

    def visitStmnt_equal(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        equal = str(left) + " = " + str(right) + "\n"
        if right in self.og_registers:
            self.registers.append(right)
        self.line += equal
        return left
    
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
        if boolean == 'true':
            boolean = "1"
        else:
            boolean = "0"
        return ("boolean", boolean)
    
    def visitLocation(self, ctx, parent = None):
        name = ctx.ID().getText()
        offset = 0

        for scope in self.scope_actual[::-1]:
            sActual = self.scopes[scope]
            if symbol := sActual.get_symbol(name):
                break
        
        for symbol in sActual.symbols:
            if symbol.name == name:
                break
            else:
                if symbol.type in DEFAULT_TYPES:
                    offset += DEFAULT_TYPES[symbol.type]
                else:
                    offset += sActual.get_instance_size(symbol.type.replace('struct', "")) * symbol.reps

        if ctx.expression() != None:
            resp = self.visit(ctx.expression())
            try:
                if symbol.type in DEFAULT_TYPES:
                    offset += DEFAULT_TYPES[symbol.type] * int(ctx.expression().getText())
                else:
                    sym_type = symbol.type.replace("struct", "")
                    offset += sActual.get_instance_size(sym_type) * int(ctx.expression().getText())
            except:
                register = self.registers.pop()
                if symbol.type in DEFAULT_TYPES:
                    self.line += register + " = " + resp + " * " + str(DEFAULT_TYPES[symbol.type]) + "\n"
                else:
                    sym_type = symbol.type.replace("struct", "")
                    self.line += register + " = " + resp + " * " + str(sActual.get_instance_size(sym_type)) + "\n"
                offset = register


        sName = sActual.name[0] + str(sActual.id)
        value  = sName + "[" + str(offset) + "]"
        return value
