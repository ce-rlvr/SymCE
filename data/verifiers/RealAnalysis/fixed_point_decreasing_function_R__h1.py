import sympy
import z3

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x', real=True)
Piecewise = sympy.Piecewise
Abs = sympy.Abs
Max = sympy.Max
Min = sympy.Min

def sympy_to_z3(expr, var_map):
    """Recursively converts a sympy expression to a z3 expression."""
    if isinstance(expr, sympy.Symbol):
        if expr.name in var_map:
            return var_map[expr.name]
        return z3.Real(expr.name)
    elif isinstance(expr, int):
        return z3.RealVal(expr)
    elif isinstance(expr, float):
        frac = sympy.Rational(expr)
        return z3.RealVal(f"{frac.p}/{frac.q}")
    elif isinstance(expr, sympy.Float):
        frac = sympy.Rational(expr)
        return z3.RealVal(f"{frac.p}/{frac.q}")
    elif isinstance(expr, sympy.Rational):
        return z3.RealVal(f"{expr.p}/{expr.q}")
    elif isinstance(expr, sympy.Integer):
        return z3.RealVal(str(expr))
    elif isinstance(expr, sympy.Number):
        if expr in (sympy.oo, -sympy.oo):
            raise ValueError("Infinity not supported in z3 translation")
        return z3.RealVal(str(expr))
    elif isinstance(expr, sympy.Add):
        args = [sympy_to_z3(arg, var_map) for arg in expr.args]
        return sum(args[1:], args[0])
    elif isinstance(expr, sympy.Mul):
        args = [sympy_to_z3(arg, var_map) for arg in expr.args]
        res = args[0]
        for a in args[1:]:
            res = res * a
        return res
    elif isinstance(expr, sympy.Pow):
        base = sympy_to_z3(expr.args[0], var_map)
        exp_sym = expr.args[1]
        if isinstance(exp_sym, sympy.Integer):
            n = int(exp_sym)
            if n > 0:
                res = base
                for _ in range(n - 1):
                    res = res * base
                return res
            elif n < 0:
                res = base
                for _ in range(abs(n) - 1):
                    res = res * base
                return z3.RealVal(1) / res
            else:
                return z3.RealVal(1)
        exp = sympy_to_z3(exp_sym, var_map)
        return base ** exp
    elif isinstance(expr, sympy.Abs):
        arg = sympy_to_z3(expr.args[0], var_map)
        return z3.If(arg >= 0, arg, -arg)
    elif isinstance(expr, sympy.Max):
        args = [sympy_to_z3(arg, var_map) for arg in expr.args]
        res = args[0]
        for a in args[1:]:
            res = z3.If(res >= a, res, a)
        return res
    elif isinstance(expr, sympy.Min):
        args = [sympy_to_z3(arg, var_map) for arg in expr.args]
        res = args[0]
        for a in args[1:]:
            res = z3.If(res <= a, res, a)
        return res
    elif isinstance(expr, sympy.sign):
        arg = sympy_to_z3(expr.args[0], var_map)
        return z3.If(arg > 0, z3.RealVal(1), z3.If(arg < 0, z3.RealVal(-1), z3.RealVal(0)))
    elif isinstance(expr, sympy.Piecewise):
        res = None
        for e, c in reversed(expr.args):
            z3_e = sympy_to_z3(e, var_map)
            if c == sympy.true or str(c) == "True":
                res = z3_e
            else:
                z3_c = sympy_to_z3(c, var_map)
                if res is None:
                    res = z3_e
                else:
                    res = z3.If(z3_c, z3_e, res)
        if res is None:
            res = z3.RealVal(0)
        return res
    elif isinstance(expr, sympy.Relational):
        lhs = sympy_to_z3(expr.lhs, var_map)
        rhs = sympy_to_z3(expr.rhs, var_map)
        if isinstance(expr, sympy.StrictLessThan): return lhs < rhs
        if isinstance(expr, sympy.LessThan): return lhs <= rhs
        if isinstance(expr, sympy.StrictGreaterThan): return lhs > rhs
        if isinstance(expr, sympy.GreaterThan): return lhs >= rhs
        if isinstance(expr, sympy.Eq): return lhs == rhs
        if isinstance(expr, sympy.Ne): return lhs != rhs
    elif isinstance(expr, sympy.And):
        return z3.And(*[sympy_to_z3(arg, var_map) for arg in expr.args])
    elif isinstance(expr, sympy.Or):
        return z3.Or(*[sympy_to_z3(arg, var_map) for arg in expr.args])
    elif isinstance(expr, sympy.Not):
        return z3.Not(sympy_to_z3(expr.args[0], var_map))
    elif expr == sympy.true:
        return True
    elif expr == sympy.false:
        return False
    else:
        raise ValueError(f"Unsupported sympy expression: {type(expr)} {expr}")

def check_unsat(formula, timeout=1500):
    s = z3.Solver()
    s.set("timeout", timeout)
    s.add(formula)
    return s.check() == z3.unsat

def check_sat(formula, timeout=1500):
    s = z3.Solver()
    s.set("timeout", timeout)
    s.add(formula)
    return s.check() == z3.sat

def conditions(witness) -> list[bool]:
    res = [False, False]
    
    try:
        x_z3 = z3.Real('x')
        z3_expr = None
        
        if callable(witness):
            try:
                sym_expr = witness(x)
                if isinstance(sym_expr, (int, float)):
                    z3_expr = z3.RealVal(sym_expr)
                else:
                    z3_expr = sympy_to_z3(sym_expr, {'x': x_z3})
            except Exception:
                z3_expr_raw = witness(x_z3)
                if isinstance(z3_expr_raw, (int, float)):
                    z3_expr = z3.RealVal(z3_expr_raw)
                else:
                    z3_expr = z3_expr_raw
        elif isinstance(witness, sympy.Expr):
            z3_expr = sympy_to_z3(witness, {'x': x_z3})
        elif z3.is_expr(witness):
            z3_expr = witness
        elif isinstance(witness, (int, float)):
            z3_expr = z3.RealVal(witness)
            
        if z3_expr is None:
            return res
    except Exception:
        return res

    # H1: The function f is strictly decreasing on R
    try:
        a = z3.Real('a')
        b = z3.Real('b')
        f_a = z3.substitute(z3_expr, (x_z3, a))
        f_b = z3.substitute(z3_expr, (x_z3, b))
        
        # Strictly decreasing: a < b => f(a) > f(b)
        # Valid if negation (a < b AND f(a) <= f(b)) is unsat
        res[0] = bool(check_unsat(z3.And(a < b, f_a <= f_b)))
    except Exception:
        pass

    # neg_Q: It is NOT the case that there exists a unique real number c such that f(c) = c
    # This means there are either 0 fixed points, or >= 2 fixed points.
    try:
        c = z3.Real('c')
        d = z3.Real('d')
        f_c = z3.substitute(z3_expr, (x_z3, c))
        f_d = z3.substitute(z3_expr, (x_z3, d))
        
        zero_fixed_points = check_unsat(f_c == c)
        multiple_fixed_points = check_sat(z3.And(c != d, f_c == c, f_d == d))
        
        res[1] = bool(zero_fixed_points or multiple_fixed_points)
    except Exception:
        pass

    return res

CONDITION_LABELS = [
    "H_1: The function f is strictly decreasing on R",
    "¬Q: f does not have a unique fixed point"
]

N_HYP = 1
NEG_Q_INDEX = 1