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
        global scope_ids, instantiable_ids
        scope_ids += 1
        new_scope = tables.Scope(scope_ids, method_name, parent= scopes[-1].id)
        scopes.append(new_scope)
        self.visitChildren(ctx)
        scopes.pop()
        nani = (ctx.block().statement())
        the_return = None
        for part in nani:
            if 'return' in part.getText():
                the_return = part.expression().getText()
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
            else:
                new_error = tables.Error("parameter already defined", ctx.start.line, ctx.start.column)
                ERRORS.append(new_error)

        if scopes[-1].get_instance(method_name):
            new_error = tables.Error("method already defined in scope", ctx.start.line, ctx.start.column)
            ERRORS.append(new_error)
        else:
            scopes[-1].add_instantiable(instantiable_ids, method_name, method_type, the_return,p)
        return 0

    def visitBlock(self, ctx):
        self.visitChildren(ctx)
        return 0

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
            symbol = tables.Symbols(type_var, name, symbols_ids, offset)
            scopes[-1].symbols.append(symbol)
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
            symbol = tables.Symbols(type_var, symbols_ids, name, offset)
            scopes[-1].symbols.append(symbol)
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
        self.visitChildren(ctx)
                

    def visitLiteral(self, ctx):
        val = self.visitChildren(ctx)
        return val
    
    def visitInt_literal(self, ctx):
        num = ctx.NUM().getText()
        return ("int", int(num))
    
    def visitChar_literal(self, ctx):
        char = ctx.CHAR().getText()
        print("char ", char)
        return ("char", char)
    
    def visitBool_literal(self, ctx):
        boolean = ctx.getText()
        return ("boolean", boolean)