import sympy as sp
import z3
import math

# Top-level setup
n_sym = sp.Symbol('n', integer=True, positive=True)
x_sym = sp.Symbol('x', real=True)
n = z3.Int('n')
x = z3.Real('x')

Interval = sp.Interval
oo = sp.oo
Union = sp.Union
Intersection = sp.Intersection
EmptySet = sp.S.EmptySet
UniversalSet = sp.S.UniversalSet

def sympy_to_z3(expr):
    if isinstance(expr, (int, float)):
        return z3.RealVal(expr)
    if isinstance(expr, sp.StrictGreaterThan):
        return sympy_to_z3(expr.lhs) > sympy_to_z3(expr.rhs)
    if isinstance(expr, sp.GreaterThan):
        return sympy_to_z3(expr.lhs) >= sympy_to_z3(expr.rhs)
    if isinstance(expr, sp.StrictLessThan):
        return sympy_to_z3(expr.lhs) < sympy_to_z3(expr.rhs)
    if isinstance(expr, sp.LessThan):
        return sympy_to_z3(expr.lhs) <= sympy_to_z3(expr.rhs)
    if isinstance(expr, sp.Eq):
        return sympy_to_z3(expr.lhs) == sympy_to_z3(expr.rhs)
    if isinstance(expr, sp.And):
        return z3.And(*[sympy_to_z3(arg) for arg in expr.args])
    if isinstance(expr, sp.Or):
        return z3.Or(*[sympy_to_z3(arg) for arg in expr.args])
    if isinstance(expr, sp.Not):
        return z3.Not(sympy_to_z3(expr.args[0]))
    if isinstance(expr, sp.Symbol):
        if expr.name == 'n':
            return z3.ToReal(n)
        if expr.name == 'x':
            return x
        return z3.Real(expr.name)
    if isinstance(expr, sp.Rational):
        return z3.RealVal(expr.p) / z3.RealVal(expr.q)
    if isinstance(expr, sp.Float):
        return z3.RealVal(str(expr))
    if isinstance(expr, sp.Number):
        return float(expr)
    if isinstance(expr, sp.Add):
        return sum(sympy_to_z3(arg) for arg in expr.args)
    if isinstance(expr, sp.Mul):
        res = 1
        for arg in expr.args:
            res *= sympy_to_z3(arg)
        return res
    if isinstance(expr, sp.Pow):
        return sympy_to_z3(expr.base) ** sympy_to_z3(expr.exp)
    if expr == sp.S.true:
        return z3.BoolVal(True)
    if expr == sp.S.false:
        return z3.BoolVal(False)
    if isinstance(expr, sp.Abs):
        arg_z3 = sympy_to_z3(expr.args[0])
        return z3.If(arg_z3 >= 0, arg_z3, -arg_z3)
    raise ValueError(f"Unsupported sympy expr: {expr}")

def to_z3(obj):
    if z3.is_expr(obj):
        return obj
    if isinstance(obj, sp.Set):
        if isinstance(obj, sp.Interval):
            conds = []
            if obj.start != sp.S.NegativeInfinity:
                start_z3 = sympy_to_z3(obj.start)
                if obj.left_open:
                    conds.append(x > start_z3)
                else:
                    conds.append(x >= start_z3)
            if obj.end != sp.S.Infinity:
                end_z3 = sympy_to_z3(obj.end)
                if obj.right_open:
                    conds.append(x < end_z3)
                else:
                    conds.append(x <= end_z3)
            if not conds:
                return z3.BoolVal(True)
            if len(conds) == 1:
                return conds[0]
            return z3.And(*conds)
        elif obj == sp.S.EmptySet:
            return z3.BoolVal(False)
        elif obj == sp.S.UniversalSet:
            return z3.BoolVal(True)
        elif isinstance(obj, sp.FiniteSet):
            conds = [x == sympy_to_z3(arg) for arg in obj.args]
            if not conds:
                return z3.BoolVal(False)
            if len(conds) == 1:
                return conds[0]
            return z3.Or(*conds)
        elif isinstance(obj, sp.Union):
            args_z3 = [to_z3(arg) for arg in obj.args]
            if not args_z3:
                return z3.BoolVal(False)
            if len(args_z3) == 1:
                return args_z3[0]
            return z3.Or(*args_z3)
        elif isinstance(obj, sp.Intersection):
            args_z3 = [to_z3(arg) for arg in obj.args]
            if not args_z3:
                return z3.BoolVal(True)
            if len(args_z3) == 1:
                return args_z3[0]
            return z3.And(*args_z3)
        elif isinstance(obj, sp.Complement):
            a = to_z3(obj.args[0])
            b = to_z3(obj.args[1])
            return z3.And(a, z3.Not(b))
        else:
            raise ValueError(f"Unsupported sympy set: {obj}")
    if isinstance(obj, sp.Basic):
        return sympy_to_z3(obj)
    if isinstance(obj, bool):
        return z3.BoolVal(obj)
    raise ValueError(f"Cannot convert {obj} to z3")

def get_z3_witness(witness):
    w_eval = witness
    if callable(witness) and not isinstance(witness, sp.Basic):
        success = False
        for args in [(n_sym,), (n_sym, x_sym), (n,), (n, x)]:
            try:
                w_eval = witness(*args)
                success = True
                break
            except Exception:
                continue
        if not success:
            try:
                w_eval = witness()
            except Exception:
                pass

    if hasattr(w_eval, '__contains__') and not isinstance(w_eval, (sp.Set, sp.Basic, list, tuple, dict, set)):
        try:
            res = w_eval.__contains__(x_sym)
            if res is not NotImplemented:
                w_eval = res
        except Exception:
            try:
                res = w_eval.__contains__(x)
                if res is not NotImplemented:
                    w_eval = res
            except Exception:
                pass

    return to_z3(w_eval)

def conditions(witness) -> list[bool]:
    try:
        z3_expr = get_z3_witness(witness)
    except Exception:
        return [False, False]
    
    try:
        z3_expr_n_plus_1 = z3.substitute(z3_expr, (n, n + 1))
        
        H1_formula = z3.Forall([n, x], z3.Implies(
            z3.And(n >= 1, z3_expr_n_plus_1),
            z3_expr
        ))
        
        s = z3.Solver()
        s.set("timeout", 2000)
        s.add(z3.Not(H1_formula))
        res = s.check()
        H1_ok = (res == z3.unsat)
    except Exception:
        H1_ok = False

    try:
        Q_formula = z3.Exists(x, z3.Forall(n, z3.Implies(n >= 1, z3_expr)))
        
        s2 = z3.Solver()
        s2.set("timeout", 2000)
        s2.add(Q_formula)
        res2 = s2.check()
        neg_Q_ok = (res2 == z3.unsat)
    except Exception:
        neg_Q_ok = False

    return [H1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: For all n in N, K_{n+1} is a subset of K_n",
    "¬Q: The intersection of all K_n is empty"
]
N_HYP = 1
NEG_Q_INDEX = 1