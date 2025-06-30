from core.ast import (
    Func, Print, VarDecl, If, While, Return, Call,
    Number, String, Var, BinOp
)

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self, ast_funcs):
        self.funcs     = {f.name: f for f in ast_funcs}
        # stack di ambienti (dizionari): [global_env, frame1, frame2, ...]
        self.env_stack = [{}]

    def run(self):
        if "main" not in self.funcs:
            raise RuntimeError("main() non trovata")
        self._call_func("main", [])

    def _call_func(self, name, args):
        if name not in self.funcs:
            raise RuntimeError(f"Funzione non definita: {name}")
        func = self.funcs[name]
        if len(args) != len(func.params):
            raise RuntimeError(f"Parametri errati chiamata {name}: attesi "
                                f"{len(func.params)}, passati {len(args)}")
        # nuovo frame
        frame = {}
        for pname, pval in zip(func.params, args):
            frame[pname] = pval
        self.env_stack.append(frame)
        try:
            self._exec_block(func.body)
            return None
        except ReturnException as ret:
            return ret.value
        finally:
            self.env_stack.pop()

    def _exec_block(self, stmts):
        for stmt in stmts:
            if isinstance(stmt, VarDecl):
                val = self._eval_expr(stmt.expr)
                self.env_stack[-1][stmt.name] = val

            elif isinstance(stmt, Print):
                print(self._eval_expr(stmt.expr))

            elif isinstance(stmt, If):
                if self._eval_expr(stmt.cond) != 0:
                    self._exec_block(stmt.then_body)

            elif isinstance(stmt, While):
                while self._eval_expr(stmt.cond) != 0:
                    self._exec_block(stmt.body)

            elif isinstance(stmt, Return):
                val = self._eval_expr(stmt.expr)
                raise ReturnException(val)

            elif isinstance(stmt, (Call, BinOp, Number, String, Var)):
                # chiamata o expr standalone
                self._eval_expr(stmt)

            else:
                raise RuntimeError(f"Statement non gestito: {stmt}")

    def _eval_expr(self, node):
        if isinstance(node, Number):
            return node.value
        if isinstance(node, String):
            return node.value
        if isinstance(node, Var):
            # cerca dalla cima dello stack
            for env in reversed(self.env_stack):
                if node.name in env:
                    return env[node.name]
            raise NameError(f"Variabile non definita: {node.name}")
        if isinstance(node, BinOp):
            l = self._eval_expr(node.left)
            r = self._eval_expr(node.right)
            op = node.op
            if op == "+":   return l + r
            if op == "-":   return l - r
            if op == "*":   return l * r
            if op == "/":   return l // r
            if op == "==":  return 1 if l == r else 0
            if op == "!=":  return 1 if l != r else 0
            if op == ">":   return 1 if l > r  else 0
            if op == "<":   return 1 if l < r  else 0
            if op == ">=":  return 1 if l >= r else 0
            if op == "<=":  return 1 if l <= r else 0
        if isinstance(node, Call):
            # eval args, poi chiama
            args = [self._eval_expr(a) for a in node.args]
            return self._call_func(node.name, args)

        raise RuntimeError(f"Expr non gestita: {node}")

def execute(ast_funcs):
    Interpreter(ast_funcs).run()
