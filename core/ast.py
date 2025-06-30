# core/ast.py

class Func:
    def __init__(self, name, params, body):
        self.name   = name
        self.params = params      # list of param-names
        self.body   = body        # list of statements

class Print:
    def __init__(self, expr):
        self.expr = expr

class VarDecl:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class If:
    def __init__(self, cond, then_body):
        self.cond      = cond
        self.then_body = then_body

class While:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class Return:
    def __init__(self, expr):
        self.expr = expr

class Number:
    def __init__(self, value):
        self.value = int(value)

class String:
    def __init__(self, value):
        self.value = value[1:-1]

class Var:
    def __init__(self, name):
        self.name = name

class BinOp:
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op
        self.right = right

class Call:
    def __init__(self, name, args):
        self.name = name
        self.args = args  # list of expr
