import sympy as sp
from sympy import S, oo
import itertools
from sympy.calculus.util import continuous_domain

# Expected witness format:
# A tuple: (vars, exprs, K_bounds)
# where:
#   vars is a list of sympy Symbols (e.g., [x])
#   exprs is a list of sympy expressions (e.g., [sp.Piecewise((1, x > 0), (0, True))])
#   K_bounds is a list of (min, max) tuples (e.g., [(0, 1)])
# A 1D counterexample is recommended.

x, y, z = sp.symbols('x y z')

CONDITION_LABELS = [
    "H_1: K is a compact subset of R^m",
    "H_2: f: R^n -> K is a function",
    "¬Q: f is not continuous on R^n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        vars, exprs, K_bounds = witness
        if not isinstance(vars, (list, tuple)):
            vars = [vars]
        if not isinstance(exprs, (list, tuple)):
            exprs = [exprs]
        if not isinstance(K_bounds, (list, tuple)):
            K_bounds = [K_bounds]
    except Exception:
        return [False, False, False]
        
    # H_1: K is a compact subset of R^m
    try:
        h1 = True
        if len(K_bounds) != len(exprs):
            h1 = False
        for b in K_bounds:
            if not (isinstance(b, (list, tuple)) and len(b) == 2):
                h1 = False
                break
            lower, upper = b
            if not (lower <= upper and lower > -oo and upper < oo):
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: f: R^n -> K is a function
    try:
        h2 = True
        test_vals = [-10.5, -1.1, -0.001, 0.0, 0.001, 1.1, 10.5, 3.14159, -2.71828]
        for pt_vals in itertools.product(test_vals, repeat=len(vars)):
            pt = dict(zip(vars, pt_vals))
            for expr, b in zip(exprs, K_bounds):
                val = expr.subs(pt).evalf()
                try:
                    val_c = complex(val)
                    if abs(val_c.imag) > 1e-9:
                        h2 = False
                        break
                    val_r = val_c.real
                    if not (b[0] - 1e-5 <= val_r <= b[1] + 1e-5):
                        h2 = False
                        break
                except Exception:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: f is not continuous on R^n
    neg_q = False
    try:
        for expr in exprs:
            for v in vars:
                dom = continuous_domain(expr, v, S.Reals)
                if dom != S.Reals:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        pass

    if not neg_q:
        try:
            # Heuristic fallback: check for jumps near test points
            test_vals = [-10.5, -1.1, -0.001, 0.0, 0.001, 1.1, 10.5, 3.14159, -2.71828]
            for pt_vals in itertools.product(test_vals, repeat=len(vars)):
                pt = dict(zip(vars, pt_vals))
                for expr in exprs:
                    try:
                        val_center = complex(expr.subs(pt).evalf())
                        for v in vars:
                            for sign in [-1, 1]:
                                pt_offset = pt.copy()
                                pt_offset[v] += sign * 1e-9
                                val_offset = complex(expr.subs(pt_offset).evalf())
                                if abs(val_center - val_offset) > 1e-2:
                                    neg_q = True
                                    break
                            if neg_q:
                                break
                    except Exception:
                        pass
                    if neg_q:
                        break
                if neg_q:
                    break
        except Exception:
            pass

    return [h1, h2, neg_q]