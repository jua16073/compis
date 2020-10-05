from DecafVisitor import DecafVisitor

class inter(DecafVisitor):

    def __init__(self):
        DecafVisitor.__init__(self)
        self.tree = None

    def visitExpr_arith_op(self):
        pass