DEFAULT_TYPES = ['int', 'boolean', 'char']

class Scope:
    def __init__(self, id = 0, type = "void",  name = "global", parent = None, params = None):
        self.id = id
        self.type = type
        self.name = name
        self.new_types = []
        self.symbols = []
        self.parent = parent

class Types:
    def __init__ (self, id = 0, name = None):
        self.id = id
        self.name = name
        self.size = 0
        self.inside = []

class Symbols:
    def __init__ (self, type, id = 0, name = None, offset = 0):
        self.id = id
        self.name = name
        self.type = type
        self.offset = offset




