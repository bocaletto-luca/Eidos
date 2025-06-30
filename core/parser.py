# core/parser.py

import os
from lark import Lark, Transformer, v_args
from core.ast import (
    Func, Print, VarDecl, If, While, Return,
    Number, String, Var, BinOp, Call
)

BASE_DIR     = os.path.dirname(__file__)
GRAMMAR_FILE = os.path.join(BASE_DIR, "grammar.lark")
with open(GRAMMAR_FILE, "r") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr", propagate_positions=True)

@v_args(inline=True)
class ASTBuilder(Transformer):
    def start(self, *funcs):
        return list(funcs)

    def func_decl(self, name, *args):
        """
        args può essere:
          - ( [param_list], stmt1, stmt2, ... )
          - ( stmt1, stmt2, ... ) se non ci sono parametri
        """
        if args and isinstance(args[0], list):
            params = args[0]
            stmts  = args[1:]
        else:
            params = []
            stmts  = args
        return Func(name.value, params, list(stmts))

    def param_list(self, first, *rest):
        return [first.value] + [r.value for r in rest]

    def var_decl(self, name, expr):
        return VarDecl(name.value, expr)

    def print_stmt(self, expr):
        return Print(expr)

    def if_stmt(self, cond, *stmts):
        return If(cond, list(stmts))

    def while_stmt(self, cond, *stmts):
        return While(cond, list(stmts))

    def return_stmt(self, expr):
        return Return(expr)

    def expr_stmt(self, expr):
        return expr

    def call(self, name, args=None):
        return Call(name.value, args or [])

    def arg_list(self, first, *rest):
        return [first] + list(rest)

    # Binary ops
    def add(self, a, b): return BinOp(a, "+", b)
    def sub(self, a, b): return BinOp(a, "-", b)
    def mul(self, a, b): return BinOp(a, "*", b)
    def div(self, a, b): return BinOp(a, "/", b)
    def eq(self, a, b):  return BinOp(a, "==", b)
    def ne(self, a, b):  return BinOp(a, "!=", b)
    def gt(self, a, b):  return BinOp(a, ">", b)
    def lt(self, a, b):  return BinOp(a, "<", b)
    def ge(self, a, b):  return BinOp(a, ">=", b)
    def le(self, a, b):  return BinOp(a, "<=", b)

    # Leafs
    def number(self, tk): return Number(tk.value)
    def string(self, tk): return String(tk.value)
    def var(self, tk):    return Var(tk.value)

def parse(source_text: str):
    tree = parser.parse(source_text)
    return ASTBuilder().transform(tree)
