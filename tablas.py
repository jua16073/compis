import sistema_de_tipos as tables
from DecafVisitor import DecafVisitor

DEFAULT_TYPES = {
    'int': 4,
    'boolean': 1,
    'char': 1,
}

global_scope =  tables.Scope()
scopes = [global_scope]
ERRORS = []

scope_ids = 0
symbols_ids = 0
offset = 0
instantiable_ids = 0

class MyDecafVisitor(DecafVisitor):

    def visitProgram(self, ctx):
        self.visitChildren(ctx)

        if scopes[-1].get_instance("main") == None:
            new_error = tables.Error("main method not defined", ctx.start.line, ctx.start.column)
            ERRORS.append(new_error)

        for error in ERRORS:
            print(error.problem, " in line ", error.line)
        return 0

    def visitMethodDeclaration(self, ctx):
        method_name = ctx.ID().getText()
        method_type = ctx.methodType().getText()
        global scope_ids, instantiable_ids, symbols_ids, offset
        scope_ids += 1
        new_scope = tables.Scope(scope_ids, method_name, parent= scopes[-1].id)
        scopes.append(new_scope)
        params = ctx.parameter()
        p = []
        param_names = []
        for param in params:
            param_type = param.parameterType().getText()
            param_name = param.ID().getText()
            if param_name not in param_names:
                param_names.append(param_name)
                new_param = tables.Symbols(param_type, param_name)
                p.append(new_param)
                symbols_ids += 1
                size = 0
                if param_type in DEFAULT_TYPES:
                    size += DEFAULT_TYPES[param_type]
                else:
                    search = param_type.replace("struct", "")
                    for scope in scopes[::-1]:
                        found = scope.get_instance(search)
                        if found:
                            if found.type == "struct":
                                size += found.size
                                break
                    else:
                        new_error = tables.Error("type " + search + " not found", ctx.start.line, ctx.start.column)
                        ERRORS.append(new_error)
                scopes[-1].add_symbol(param_type, param_name, symbols_ids)
                #offset += size
            else:
                new_error = tables.Error("parameter already defined", ctx.start.line, ctx.start.column)
                ERRORS.append(new_error)
        self.visitChildren(ctx)
        nani = (ctx.block().statement())
        the_return = None
        for part in nani:
            if 'return' in part.getText():
                if part.expression() != None:
                    the_return = part.expression().getText()
                    for scope in scopes[::-1]:
                        tipo_return = scope.get_symbol(the_return)                        
                        if tipo_return != None:
                            if tipo_return.type == method_type:
                                break
                            else:
                                new_error = tables.Error(the_return + " type and method type are not the same", ctx.start.line, ctx.start.column)
                                ERRORS.append(new_error)
                                break
                    else:
                        new_error = tables.Error(the_return + " not found in valid scopes", ctx.start.line, ctx.start.column)
                        ERRORS.append(new_error)
                else:
                    if method_type != "void":
                        new_error = tables.Error("return does not match method type", ctx.start.line, ctx.start.column)
                        ERRORS.append(new_error)
        scopes.pop()
        if scopes[-1].get_instance(method_name):
            new_error = tables.Error("method already defined in scope", ctx.start.line, ctx.start.column)
            ERRORS.append(new_error)
        else:
            scopes[-1].add_instantiable(instantiable_ids, method_name, method_type, the_return,p)
        return 0

    def visitBlock(self, ctx):
        self.visitChildren(ctx)
        return 0

    def visitLocation(self,ctx, parent = None):
        name  = ctx.ID().getText()
        if parent != None:
            for scope in scopes[::-1]:
                symbol = scope.get_subattribute(parent, name)
                if symbol != None:
                    if ctx.location() != None:
                        val  = self.visitLocation(ctx.location(), symbol.name.replace('struct', ''))
                        return val
                    return symbol.type
            else:
                new_error = tables.Error(name + " not found in " + parent, ctx.start.line, ctx.start.column)
                ERRORS.append(new_error)
        if ctx.location() == None:
            for scope in scopes[::-1]:
                symbol = scope.get_symbol(name)
                if symbol != None:
                    symbol_type = symbol.type
                    return symbol_type
                    
            else:
                new_error = tables.Error(name + " not found", ctx.start.line, ctx.start.column)
                ERRORS.append(new_error)
        else:
            for scope in scopes[::-1]:
                symbol = scope.get_symbol(name)
                if symbol != None:
                    symbol_type = symbol.type
                    if "struct" in symbol_type:
                        val = self.visitLocation(ctx.location(), symbol_type.replace('struct', ''))
                        return val
                    else:
                        new_error = tables.Error(name + " has no subattributes", ctx.start.line, ctx.start.column)
                        ERRORS.append(new_error)
        return None


    def visitStructDeclaration(self, ctx):
        #self.visitChildren(ctx)
        name = ctx.ID().getText()
        type = "struct"
        att = ctx.varDeclaration()
        sub_params = []
        global instantiable_ids
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
                    for scope in scopes[::-1]:
                        found = scope.get_instance(search)
                        if found:
                            if found.type == "struct":
                                size += found.size
                                break
                    else:
                        new_error = tables.Error("type " + search + " not found", ctx.start.line, ctx.start.column)
                        ERRORS.append(new_error)
            else:
                new_error = tables.Error("type " + var_name + " already defined in scope", ctx.start.line, ctx.start.column)
                ERRORS.append(new_error)
                
        scopes[-1].add_instantiable(instantiable_ids, name, 'struct', None, sub_params, size)
        instantiable_ids += 1
        return (type, name)

    def visitNormalVar(self, ctx):
        type_var = ctx.varType().getText()
        name = ctx.ID().getText()
        global symbols_ids
        global offset
        symbols_ids += 1
        if scopes[-1].get_symbol(name):
            new_error = tables.Error('"' + name + '" already defined in scope', ctx.start.line, ctx.start.column)
            ERRORS.append(new_error)
        else:
            # symbol = tables.Symbols(type_var, name, symbols_ids, offset)
            # scopes[-1].symbols.append(symbol)
            scopes[-1].add_symbol(type_var, name, symbols_ids, offset)
        if type_var in DEFAULT_TYPES:
            offset += DEFAULT_TYPES[type_var]
        else:
            search = type_var.replace("struct", "")
            for scope in scopes[::-1]:
                found = scope.get_instance(search)
                if found:
                    if found.type == "struct":
                        offset += found.size
                        break
            else:
                new_error = tables.Error("type " + search + " not found", ctx.start.line, ctx.start.column)
                ERRORS.append(new_error)
        self.visitChildren(ctx)
        return (type_var, name)

    def visitArrayVar(self, ctx):
        type_var = ctx.varType().getText()
        name = ctx.ID().getText()
        num = ctx.NUM().getText()
        global symbols_ids
        global offset
        if int(num) <= 0:
            new_error = tables.Error("array has to be size > 0", ctx.start.line, ctx.start.column)
            ERRORS.append(new_error)
        else:
            symbols_ids += 1
            # symbol = tables.Symbols(type_var, symbols_ids, name, offset)
            # scopes[-1].symbols.append(symbol)
            scopes[-1].add_symbol(type_var, name, symbols_ids, offset)
            if type_var in DEFAULT_TYPES:
                offset += (DEFAULT_TYPES[type_var] * int(num))
            else:
                search = type_var.replace("struct", "")
                for scope in scopes[::-1]:
                    found = scope.get_instance(search)
                    if found:
                        if found.type == "struct":
                            offset += found.size * int(num)
                            break
                else:
                    new_error = tables.Error("type " + search + " not found", ctx.start.line, ctx.start.column)
                    ERRORS.append(new_error)
        self.visitChildren(ctx)
        return 0

    def visitMethodCall(self,ctx):
        name = ctx.ID().getText()
        args = ctx.arg()
        self.visitChildren(ctx)
        for scope in scopes[::-1]:
            method = scope.get_instance(name)
            if method != None:
                if len(args) == len(method.params):
                    actual = 0
                    for arg in args:
                        for sub_scope in scopes[::-1]:
                            arg_type = sub_scope.get_symbol(arg.getText())
                            if arg_type != None and arg_type.type == method.params[actual].type:
                                break
                            elif arg_type != None:
                                new_error = tables.Error("type of "+ arg_type.type +" " + arg.getText() + " does not match with parameter "+ method.params[actual].type+ " "+ method.params[actual].name, ctx.start.line, ctx.start.column)
                                ERRORS.append(new_error)
                            elif arg_type == None:
                                pass
                        else:
                            new_error = tables.Error("symbol " + arg.getText() + " was not found", ctx.start.line, ctx.start.column)
                            ERRORS.append(new_error)
                        actual += 1
                return method.type
        return 0
                

    def visitLiteral(self, ctx):
        val = self.visitChildren(ctx)
        return val[0]
    
    def visitInt_literal(self, ctx):
        num = ctx.NUM()
        if num == None:
            new_error = tables.Error("expected num", ctx.start.line, ctx.start.column)
            ERRORS.append(new_error)
        return ("int", int(num.getText()))
    
    def visitChar_literal(self, ctx):
        char = ctx.CHAR()
        if char == None:
            new_error = tables.Error("expected char", ctx.start.line, ctx.start.column)
            ERRORS.append(new_error)
        return ("char", char.getText())
    
    def visitBool_literal(self, ctx):
        boolean = ctx.getText()
        if boolean != 'true' and boolean != 'false':
            new_error = tables.Error("expected true or false", ctx.start.line, ctx.start.column)
            ERRORS.append(new_error)
        return ("boolean", boolean)