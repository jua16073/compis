
class Tables:
    def __init__ (self):
        self.symbs = []
        self.types = []
        self.scopes = []
        

class Simbolo:
    def __init__(self, id, name, type, scope):
        self.id = id
        self.name = name
        self.type = type
        self.scope = scope
        self.offset = type.size

class Tipo:
    def __init__ (self, id, name, size, scope):
        self.id = id
        self.name = name
        self.size = size
        self.scope = scope

class Scope:
    def __init__(self, id, name, parent, back, params):
        self.id = id
        self.name = name
        self.parent = parent
        self.back = back
        self.params = params

