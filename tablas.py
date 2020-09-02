import sistema_de_tipos as tables
from DecafVisitor import DecafVisitor

DEFAULT_TYPES = {
    'int': 4,
    'boolean': 1,
    'char': 1,
}

global_scope =  tables.Scope()
scopes = [global_scope]

scope_ids = 0
symbols_ids = 0
offset = 0
types_ids = 0

class MyDecafVisitor(DecafVisitor):

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    def visitMethodDeclaration(self, ctx):
        print("method")
        print(ctx.ID().getText())
        print(ctx.methodType().getText())
        global scope_ids
        scope_ids += 1
        new_scope = tables.Scope(scope_ids, ctx.ID().getText(), parent= scopes[scope_ids-1])
        scopes.append(new_scope)
        self.visitChildren(ctx)
        return "yay"

    def visitStructDeclaration(self, ctx):
        print("--struct declaration--")
        name = ctx.ID().getText()
        print(name)
        print("----------------------")
        return self.visitChildren(ctx)

    def visitNormalVar(self, ctx):
        print("Var declaration")
        type_var = ctx.varType().getText()
        name = ctx.ID().getText()
        print(type_var)
        print(name)
        global symbols_ids
        global offset
        symbols_ids += 1
        symbol = tables.Symbols(type_var, symbols_ids, name, offset)
        scopes[-1].symbols.append(symbol)
        if type_var in DEFAULT_TYPES:
            offset += DEFAULT_TYPES[type_var]
        return self.visitChildren(ctx)

    def visitArrayVar(self, ctx):
        type_var = ctx.varType().getText()
        name = ctx.ID().getText()
        num = ctx.NUM().getText()
        print(type_var, " ", name, " ", num)
        global symbols_ids
        global offset
        symbols_ids += 1
        symbol = tables.Symbols(type_var, symbols_ids, name, offset)
        scopes[-1].symbols.append(symbol)
        if type_var in DEFAULT_TYPES:
            offset += (DEFAULT_TYPES[type_var] * int(num))
        return self.visitChildren(ctx)

    

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