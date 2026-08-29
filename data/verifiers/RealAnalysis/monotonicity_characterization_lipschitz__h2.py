import sympy
import z3
import math
import itertools
import functools

x = sympy.Symbol('x', real=True)

def sympy_to_z3(expr, z3_var, sympy_var):
    if isinstance(expr, (int, float)):
        return expr
    if expr == sympy_var:
        return z3_var
    if hasattr(expr, 'is_Number') and expr.is_Number:
        return float(expr)
    if hasattr(expr, 'is_Add') and expr.is_Add:
        return sum(sympy_to_z3(arg, z3_var, sympy_var) for arg in expr.args)
    if hasattr(expr, 'is_Mul') and expr.is_Mul:
        res = 1
        for arg in expr.args:
            res *= sympy_to_z3(arg, z3_var, sympy_var)
        return res
    if hasattr(expr, 'is_Pow') and expr.is_Pow:
        base = sympy_to_z3(expr.args[0], z3_var, sympy_var)
        exp = sympy_to_z3(expr.args[1], z3_var, sympy_var)
        return base ** exp
    if hasattr(expr, 'func') and expr.func.__name__ == 'Abs':
        arg = sympy_to_z3(expr.args[0], z3_var, sympy_var)
        if isinstance(arg, (int, float)):
            return abs(arg)
        return z3.If(arg >= 0, arg, -arg)
    raise ValueError(f"Unsupported sympy expression: {expr}")

def eval_f(f, val):
    if callable(f):
        return f(val)
    elif hasattr(f, 'free_symbols'):
        symbols = list(f.free_symbols)
        if len(symbols) > 1:
            raise ValueError("Too many free symbols")
        sym = symbols[0] if symbols else sympy.Symbol('x')
        return sympy_to_z3(f, val, sym)
    else:
        return float(f)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False]
        f, L, a, b = witness
    except Exception:
        return [False, False, False]
        
    try:
        a_val = float(a)
        b_val = float(b)
        L_val = float(L)
        h1_ok = a_val < b_val
        _ = eval_f(f, a_val)
    except Exception:
        h1_ok = False

    try:
        zx, zy = z3.Reals('x y')
        h2_solver = z3.Solver()
        h2_solver.set("timeout", 2000)
        
        premise = z3.And(zx >= a_val, zx < zy, zy <= b_val)
        hx = L_val * zx - eval_f(f, zx)
        hy = L_val * zy - eval_f(f, zy)
        conclusion = hx <= hy
        
        h2_solver.add(premise)
        h2_solver.add(z3.Not(conclusion))
        res = h2_solver.check()
        h2_ok = (res == z3.unsat)
    except Exception:
        h2_ok = False

    try:
        zx, zy = z3.Reals('x y')
        q_solver = z3.Solver()
        q_solver.set("timeout", 2000)
        
        premise = z3.And(zx >= a_val, zx <= b_val, zy >= a_val, zy <= b_val)
        
        def z3_Abs(val):
            if isinstance(val, (int, float)):
                return abs(val)
            return z3.If(val >= 0, val, -val)
            
        fx = eval_f(f, zx)
        fy = eval_f(f, zy)
        lip_cond = z3_Abs(fx - fy) <= L_val * z3_Abs(zx - zy)
        
        q_solver.add(premise)
        q_solver.add(z3.Not(lip_cond))
        res = q_solver.check()
        neg_q_ok = (res == z3.sat)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the closed interval a to b",
    "H_2: The function h(x) = Lx - f(x) is monotonically non-decreasing on a to b",
    "¬Q: The function f is not L-Lipschitz continuous on the interval a to b"
]

N_HYP = 2
NEG_Q_INDEX = 2