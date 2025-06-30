from core.ast import (
    Func, VarDecl, Print, Number, String,
    Var, BinOp, If, While, Return, Call
)

class TypeError(Exception):
    pass

class TypeChecker:
    def __init__(self, ast_funcs):
        self.funcs = {f.name: f for f in ast_funcs}
        # ambiente temporaneo per params e locals
        self.env = {}

    def check(self):
        # tutte le funzioni
        for func in self.funcs.values():
            # new env per ogni funzione
            self.env = {}
            # parametri → int
            for p in func.params:
                self.env[p] = "int"
            # verifica body
            self._check_block(func.body)
        if "main" not in self.funcs:
            raise TypeError("main() non trovata")

    def _check_block(self, stmts):
        for stmt in stmts:
            if isinstance(stmt, VarDecl):
                t = self._infer_type(stmt.expr)
                self.env[stmt.name] = t

            elif isinstance(stmt, Print):
                self._infer_type(stmt.expr)

            elif isinstance(stmt, If):
                ct = self._infer_type(stmt.cond)
                if ct != "int":
                    raise TypeError(f"Condizione if non intera ma {ct}")
                self._check_block(stmt.then_body)

            elif isinstance(stmt, While):
                ct = self._infer_type(stmt.cond)
                if ct != "int":
                    raise TypeError(f"Condizione while non intera ma {ct}")
                self._check_block(stmt.body)

            elif isinstance(stmt, Return):
                self._infer_type(stmt.expr)

            elif isinstance(stmt, (BinOp, Number, String, Var, Call)):
                self._infer_type(stmt)

            else:
                raise TypeError(f"Statement non gestito dal checker: {stmt}")

    def _infer_type(self, node):
        if isinstance(node, Number):
            return "int"
        if isinstance(node, String):
            return "string"
        if isinstance(node, Var):
            if node.name not in self.env:
                raise TypeError(f"Variabile non definita: {node.name}")
            return self.env[node.name]
        if isinstance(node, BinOp):
            lt = self._infer_type(node.left)
            rt = self._infer_type(node.right)
            if node.op in {"+","-","*","/"}:
                if lt == "int" and rt == "int":
                    return "int"
                raise TypeError(f"Operazione '{node.op}' non supportata tra {lt} e {rt}")
            if node.op in {"==","!=","<",">","<=",">="}:
                if lt == "int" and rt == "int":
                    return "int"
                raise TypeError(f"Comparazione '{node.op}' non supportata tra {lt} e {rt}")
        if isinstance(node, Call):
            if node.name not in self.funcs:
                raise TypeError(f"Funzione non definita: {node.name}")
            f = self.funcs[node.name]
            if len(node.args) != len(f.params):
                raise TypeError(f"{node.name} param mismatch")
            # tutti gli arg devono essere int
            for arg in node.args:
                at = self._infer_type(arg)
                if at != "int":
                    raise TypeError(f"Argomento non intero in chiamata {node.name}")
            return "int"
        raise TypeError(f"Expr non gestita: {node}")

def type_check(ast_funcs):
    TypeChecker(ast_funcs).check()
