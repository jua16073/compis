import sistema_de_tipos as tables
from DecafVisitor import DecafVisitor

DEFAULT_TYPES = {
    'int': 4,
    'boolean': 1,
    'char': 1,
}

class MyDecafVisitor(DecafVisitor):

    def __init__(self):
        DecafVisitor.__init__(self)
        self.scope_ids = 0
        self.symbols_ids = 0
        self.offset = 0
        self.instantiable_ids = 0
        self.ERRORS = []
        global_scope = tables.Scope()
        self.scopes = [global_scope]
        self.total_scopes = {global_scope.name: global_scope,}

    def visitProgram(self, ctx):
        self.ERRORS = []
        self.visitChildren(ctx)

        if self.scopes[-1].get_instance("main") == None:
            new_error = tables.Error("main method not defined", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return 0

    def visitMethodDeclaration(self, ctx):
        method_name = ctx.ID().getText()
        method_type = ctx.methodType().getText()
        self.scope_ids += 1
        new_scope = tables.Scope(self.scope_ids, method_name, self.scopes[-1], method_type)
        self.scopes.append(new_scope)
        params = ctx.parameter()
        p = []
        param_names = []
        for param in params:
            param_type = param.parameterType().getText()
            param_name = param.ID().getText()
            if param_name not in param_names:
                param_names.append(param_name)
                new_param = tables.Symbols(param_type, param_name, 1)
                p.append(new_param)
                self.symbols_ids += 1
                size = 0
                if param_type in DEFAULT_TYPES:
                    size = DEFAULT_TYPES[param_type]
                else:
                    search = param_type.replace("struct", "")
                    for scope in self.scopes[::-1]:
                        found = scope.get_instance(search)
                        if found:
                            if found.type == "struct":
                                size = found.size
                                break
                    else:
                        new_error = tables.Error("type " + search + " not found", ctx.start.line, ctx.start.column)
                        self.ERRORS.append(new_error)
                self.scopes[-1].add_symbol(param_type, param_name, 1, self.symbols_ids)
                self.offset += size
            else:
                new_error = tables.Error("parameter already defined", ctx.start.line, ctx.start.column)
                self.ERRORS.append(new_error)
        nani = (ctx.block().statement())
        the_return = None
        for part in nani:
            if 'return' in part.getText():
                break
        else:
            if method_type != "void":
                new_error = tables.Error("return does not match method type", ctx.start.line, ctx.start.column)
                self.ERRORS.append(new_error)
        
        if self.scopes[-2].get_instance(method_name):
            new_error = tables.Error("method already defined in scope", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        else:
            self.scopes[-2].add_instantiable(self.instantiable_ids, method_name, method_type, the_return,p)
        self.visitChildren(ctx)
        end_scope = self.scopes.pop()
        self.total_scopes[new_scope.name] = end_scope
        return 0

    def visitIfScope(self,ctx):
        val = self.visit(ctx.expression())
        self.scope_ids += 1
        if val != "boolean":
            new_error = tables.Error("expected boolean got " + val, ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        new_scope = tables.Scope(self.scope_ids, "if" + str(self.scope_ids), self.scopes[-1])
        self.scopes.append(new_scope)
        self.visitChildren(ctx)
        end = self.scopes.pop()
        self.total_scopes[new_scope.name] = end
        return None

    def visitWhileScope(self,ctx):
        val = self.visit(ctx.expression())
        self.scope_ids += 1
        if val != "boolean":
            new_error = tables.Error("expected boolean got " + val, ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        new_scope = tables.Scope(self.scope_ids, "while" + str(self.scope_ids), self.scopes[-1])
        self.scopes.append(new_scope)
        self.visitChildren(ctx)
        end = self.scopes.pop()
        self.total_scopes[new_scope.name] = end
        return None
    
    def visitStmnt_return(self, ctx):
        if ctx.expression() != None:
            val = self.visit(ctx.expression())
            for scope in self.scopes[::-1]:
                if scope.type != None:
                    if val != scope.type:
                        new_error = tables.Error("return " + ctx.expression().getText() + " does not match method type " + scope.type, ctx.start.line, ctx.start.column)
                        self.ERRORS.append(new_error)
                        break
        else:
            for scope in self.scopes[::-1]:
                if scope.type != None:
                    if "void" != scope.type:
                        new_error = tables.Error("empty return  does not match method type " + scope.type, ctx.start.line, ctx.start.column)
                        self.ERRORS.append(new_error)
                        break
        return None


    def visitBlock(self, ctx):
        self.visitChildren(ctx)
        return None

    def visitLocation(self,ctx, parent = None):
        name  = ctx.ID().getText()
        if ctx.expression() != None:
            val = self.visit(ctx.expression())
            if val != "int":
                new_error = tables.Error("expected int got " + ctx.expresion()+ " of type "+ val, ctx.start.line, ctx.start.column)
                self.ERRORS.append(new_error)
        if parent != None:
            for scope in self.scopes[::-1]:
                symbol = scope.get_subattribute(parent, name)
                if symbol != None:
                    if ctx.location() != None:
                        val  = self.visitLocation(ctx.location(), symbol.type.replace('struct', ''))
                        return val
                    return symbol.type
            else:
                new_error = tables.Error(name + " not found in " + parent, ctx.start.line, ctx.start.column)
                self.ERRORS.append(new_error)
        if ctx.location() == None:
            for scope in self.scopes[::-1]:
                symbol = scope.get_symbol(name)
                if symbol != None:
                    symbol_type = symbol.type
                    return symbol_type
                    
            else:
                new_error = tables.Error(name + " not found", ctx.start.line, ctx.start.column)
                self.ERRORS.append(new_error)
        else:
            for scope in self.scopes[::-1]:
                symbol = scope.get_symbol(name)
                if symbol != None:
                    symbol_type = symbol.type
                    if "struct" in symbol_type:
                        val = self.visitLocation(ctx.location(), symbol_type.replace('struct', ''))
                        return val
                    else:
                        new_error = tables.Error(name + " has no subattributes", ctx.start.line, ctx.start.column)
                        self.ERRORS.append(new_error)
        return None


    def visitStructDeclaration(self, ctx):
        #self.visitChildren(ctx)
        name = ctx.ID().getText()
        type = "struct"
        att = ctx.varDeclaration()
        sub_params = []
        size = 0
        sub_attributes_names = []
        for s in att:
            var_type = s.varType().getText()
            var_name = s.ID().getText()
            if var_name not in sub_attributes_names:
                sub_attributes_names.append(var_name)
                sub = tables.Symbols(var_type, var_name, id)
                sub_params.append(sub)
                if var_type in DEFAULT_TYPES:
                    size += DEFAULT_TYPES[var_type]
                else:
                    search = var_type.replace("struct", "")
                    for scope in self.scopes[::-1]:
                        found = scope.get_instance(search)
                        if found:
                            if found.type == "struct":
                                size += found.size
                                break
                    else:
                        new_error = tables.Error("type " + search + " not found", ctx.start.line, ctx.start.column)
                        self.ERRORS.append(new_error)
            else:
                new_error = tables.Error("type " + var_name + " already defined in scope", ctx.start.line, ctx.start.column)
                self.ERRORS.append(new_error)
                
        self.scopes[-1].add_instantiable(self.instantiable_ids, name, 'struct', None, sub_params, size)
        self.instantiable_ids += 1
        return (type, name)

    def visitNormalVar(self, ctx):
        type_var = ctx.varType().getText()
        name = ctx.ID().getText()
        self.symbols_ids += 1
        if self.scopes[-1].get_symbol(name):
            new_error = tables.Error('"' + name + '" already defined in scope', ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        else:
            # symbol = tables.Symbols(type_var, name, self.symbols_ids, self.offset)
            # self.scopes[-1].symbols.append(symbol)
            self.scopes[-1].add_symbol(type_var, name, 1, self.symbols_ids, self.offset)
        if type_var in DEFAULT_TYPES:
            self.offset += DEFAULT_TYPES[type_var]
        else:
            search = type_var.replace("struct", "")
            for scope in self.scopes[::-1]:
                found = scope.get_instance(search)
                if found:
                    if found.type == "struct":
                        self.offset += found.size
                        break
            else:
                new_error = tables.Error("type " + search + " not found", ctx.start.line, ctx.start.column)
                self.ERRORS.append(new_error)
        self.visitChildren(ctx)
        return (type_var, name)

    def visitArrayVar(self, ctx):
        type_var = ctx.varType().getText()
        name = ctx.ID().getText()
        num = ctx.NUM().getText()
        if int(num) <= 0:
            new_error = tables.Error("array has to be size > 0", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        else:
            self.symbols_ids += 1
            # symbol = tables.Symbols(type_var, symbols_ids, name, self.offset)
            # self.scopes[-1].symbols.append(symbol)
            self.scopes[-1].add_symbol(type_var, name, num, self.symbols_ids, self.offset)
            if type_var in DEFAULT_TYPES:
                self.offset += (DEFAULT_TYPES[type_var] * int(num))
            else:
                search = type_var.replace("struct", "")
                for scope in self.scopes[::-1]:
                    found = scope.get_instance(search)
                    if found:
                        if found.type == "struct":
                            self.offset += found.size * int(num)
                            break
                else:
                    new_error = tables.Error("type " + search + " not found", ctx.start.line, ctx.start.column)
                    self.ERRORS.append(new_error)
        self.visitChildren(ctx)
        return 0

    def visitMethodCall(self,ctx):
        name = ctx.ID().getText()
        args = ctx.arg()
        self.visitChildren(ctx)
        for scope in self.scopes[::-1]:
            method = scope.get_instance(name)
            if method != None:
                if len(args) == len(method.params):
                    actual = 0
                    for arg in args:
                        val = self.visit(arg)
                        if val != None and val == method.params[actual].type:
                            break
                        elif val != None:
                            new_error = tables.Error("type of "+ val +" " + arg.getText() + " does not match with parameter "+ method.params[actual].type+ " "+ method.params[actual].name, ctx.start.line, ctx.start.column)
                            self.ERRORS.append(new_error)
                        actual += 1
                return method.type
        return None

    def visitStmnt_equal(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if left == None:
            new_error = tables.Error(ctx.left.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        elif right == None:
            new_error = tables.Error(ctx.right.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        elif left != right:
            new_error = tables.Error(ctx.left.getText() + " expected " + left +" found " + ctx.right.getText() + " of type " + right + " instead", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return None

    def visitExpr_not(self, ctx):
        val = self.visit(ctx.expression())
        if val == "boolean":
            return val
        else:
            new_error = tables.Error("expected boolean got " + val, ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
    
    def visitExpr_par(self,ctx):
        val = self.visit(ctx.expression())
        return val

    def visitExpr_minus(self, ctx):
        val = self.visit(ctx.expression())
        return val
    
    def visitExpr_arith_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if right == "int" and left == "int":
            return "int"
        elif left == None:
            new_error = tables.Error(ctx.left.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        elif right == None:
            new_error = tables.Error(ctx.right.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        else:
            new_error = tables.Error("expected int and int got " + left + " and " + right, ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return None

    def visitExpr_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if right == "int" and left == "int":
            return "int"
        elif left == None:
            new_error = tables.Error(ctx.left.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        elif right == None:
            new_error = tables.Error(ctx.right.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        else:
            new_error = tables.Error("expected int and int got " + left + " and " + right, ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return None
    
    def visitExpr_rel_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if right == "int" and left == "int":
            return "boolean"
        elif left == None:
            new_error = tables.Error(ctx.left.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        elif right == None:
            new_error = tables.Error(ctx.right.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        else:
            new_error = tables.Error("expected int and int got " + left + " and " + right, ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return None
    
    def visitExpr_eq_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if left == right:
            return "boolean"
        elif left == None:
            new_error = tables.Error(ctx.left.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        elif right == None:
            new_error = tables.Error(ctx.right.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        else:
            new_error = tables.Error("expected same types got " + left + " and " + right, ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return None
    
    def visitExpr_cond_op(self, ctx):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        if left == "boolean" and right == "boolean":
            return "boolean"
        elif left == None:
            new_error = tables.Error(ctx.left.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        elif right == None:
            new_error = tables.Error(ctx.right.getText() +  " is None", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        else:
            new_error = tables.Error("expected boolean types got " + left + " and " + right, ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return None


    def visitLiteral(self, ctx):
        val = self.visitChildren(ctx)
        return val[0]
    
    def visitInt_literal(self, ctx):
        num = ctx.NUM()
        if num == None:
            new_error = tables.Error("expected num", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return ("int", int(num.getText()))
    
    def visitChar_literal(self, ctx):
        char = ctx.CHAR()
        if char == None:
            new_error = tables.Error("expected char", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return ("char", char.getText())
    
    def visitBool_literal(self, ctx):
        boolean = ctx.getText()
        if boolean != 'true' and boolean != 'false':
            new_error = tables.Error("expected true or false", ctx.start.line, ctx.start.column)
            self.ERRORS.append(new_error)
        return ("boolean", boolean)