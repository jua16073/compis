DEFAULT_TYPES = ['int', 'boolean', 'char']

class Scope:
    def __init__(self, id = 0,  name = "global", parent = None, type = None):
        self.id = id
        self.type = type
        self.name = name
        self.instantiables = []
        self.symbols = []
        self.parent = parent
    
    def get_instance(self, name):
        for instance in self.instantiables:
            if instance.name == name:
                return instance
    
    def add_instantiable(self, id, name, type, ret = None, subs = [], size = 0):
        instan = Instantiable(id, name, type, ret, subs, size)
        self.instantiables.append(instan)
    
    def get_symbol(self, name):
        for symbol in self.symbols:
            if symbol.name == name:
                return symbol

    def add_symbol(self, type, name, id = 0, offset = 0):
        symbol = Symbols(type, name, id, offset)
        self.symbols.append(symbol)
    
    def get_subattribute(self, instance_name, sub_name):
        for instance in self.instantiables:
            if instance.name == instance_name:
                for sub in instance.sub_attributes:
                    if sub.name == sub_name:
                        return sub
        return None
    


class Instantiable:
    def __init__ (self, id = 0, name = None, type = None, ret = None, subs = [], size = 0 ):
        self.id = id
        self.name = name
        if type == "struct":
            self.type = type
            self.size = size
            self.sub_attributes = subs
        else:
            self.type = type
            self.ret = ret
            self.params = subs

class Symbols:
    def __init__ (self, type, name,  id = 0, offset = 0):
        self.id = id
        self.name = name
        self.type = type
        self.offset = offset

class Error:
    def __init__ (self, problem, line, columns):
        self.problem = problem
        self.line = line
        self.column = columns




