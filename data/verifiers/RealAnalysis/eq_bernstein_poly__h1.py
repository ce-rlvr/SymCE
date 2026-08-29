import sympy as sp
from sympy.calculus.util import continuous_domain
import math
import itertools
import functools

# Top-level setup
x = sp.Symbol('x', real=True)

def get_expr_and_var(witness):
    if isinstance(witness, (int, float)):
        witness = sp.sympify(witness)
    if isinstance(witness, sp.Expr):
        free = witness.free_symbols
        if len(free) == 1:
            return witness, list(free)[0]
        elif len(free) == 0:
            return witness, x
    elif callable(witness):
        try:
            expr = witness(x)
            if isinstance(expr, sp.Expr):
                return expr, x
        except Exception:
            pass
    return None, None

def is_valid_limit(L):
    if L is None:
        return False
    if hasattr(L, 'has') and L.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
        return False
    if type(L).__name__ == 'AccumBounds':
        return False
    return True

def conditions(witness) -> list[bool]:
    # H_1: B_n(f)(x) is the n-th Bernstein polynomial for f.
    h1_ok = False
    try:
        expr, var = get_expr_and_var(witness)
        if expr is not None:
            v0 = float(expr.subs(var, 0.0).evalf())
            v1 = float(expr.subs(var, 0.5).evalf())
            v2 = float(expr.subs(var, 1.0).evalf())
            if not (math.isinf(v0) or math.isnan(v0) or math.isinf(v1) or math.isnan(v1) or math.isinf(v2) or math.isnan(v2)):
                h1_ok = True
        elif callable(witness):
            v0 = float(witness(0.0))
            v1 = float(witness(0.5))
            v2 = float(witness(1.0))
            if not (math.isinf(v0) or math.isnan(v0) or math.isinf(v1) or math.isnan(v1) or math.isinf(v2) or math.isnan(v2)):
                h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The sequence of Bernstein polynomials {B_n(f)} is not uniformly equicontinuous on [0, 1]
    neg_q_ok = False
    try:
        expr, var = get_expr_and_var(witness)
        evaluated_with_sympy = False
        
        if expr is not None:
            try:
                dom = continuous_domain(expr, var, sp.Interval(0, 1))
                if dom == sp.Interval(0, 1):
                    neg_q_ok = False
                    evaluated_with_sympy = True
                else:
                    discontinuities = sp.Interval(0, 1) - dom
                    if not isinstance(discontinuities, sp.FiniteSet):
                        neg_q_ok = True
                        evaluated_with_sympy = True
                    else:
                        is_unif_equi = True
                        for c in discontinuities:
                            if c == 0:
                                L_right = sp.limit(expr, var, 0, dir='+')
                                val = expr.subs(var, 0)
                                if not is_valid_limit(L_right) or L_right != val:
                                    is_unif_equi = False
                                    break
                            elif c == 1:
                                L_left = sp.limit(expr, var, 1, dir='-')
                                val = expr.subs(var, 1)
                                if not is_valid_limit(L_left) or L_left != val:
                                    is_unif_equi = False
                                    break
                            else:
                                L_left = sp.limit(expr, var, c, dir='-')
                                L_right = sp.limit(expr, var, c, dir='+')
                                if not is_valid_limit(L_left) or not is_valid_limit(L_right) or L_left != L_right:
                                    is_unif_equi = False
                                    break
                        neg_q_ok = not is_unif_equi
                        evaluated_with_sympy = True
            except Exception:
                pass
                
        if not evaluated_with_sympy:
            if expr is not None:
                def witness_func(val):
                    return float(expr.subs(var, val).evalf())
            elif callable(witness):
                witness_func = witness
            else:
                witness_func = None
                
            if witness_func is not None:
                is_unif_equi = True
                
                try:
                    f0 = float(witness_func(0.0))
                    f1 = float(witness_func(1e-12))
                    f2 = float(witness_func(1e-10))
                    if abs(f1 - f0) > 0.05 and abs(f2 - f1) < 0.05:
                        is_unif_equi = False
                except Exception:
                    is_unif_equi = False

                if is_unif_equi:
                    try:
                        f_end = float(witness_func(1.0))
                        f1 = float(witness_func(1.0 - 1e-12))
                        f2 = float(witness_func(1.0 - 1e-10))
                        if abs(f1 - f_end) > 0.05 and abs(f2 - f1) < 0.05:
                            is_unif_equi = False
                    except Exception:
                        is_unif_equi = False

                if is_unif_equi:
                    grid = [i / 1000.0 for i in range(1001)]
                    vals = []
                    for v in grid:
                        try:
                            vals.append(float(witness_func(v)))
                        except Exception:
                            is_unif_equi = False
                            break
                    
                    if len(vals) == 1001 and is_unif_equi:
                        for i in range(1000):
                            if abs(vals[i+1] - vals[i]) > 0.1:
                                a = grid[i]
                                b = grid[i+1]
                                fa = vals[i]
                                fb = vals[i+1]
                                for _ in range(50):
                                    mid = (a + b) / 2.0
                                    if mid == a or mid == b:
                                        break
                                    try:
                                        fmid = float(witness_func(mid))
                                        if abs(fmid - fa) > abs(fb - fmid):
                                            b = mid
                                            fb = fmid
                                        else:
                                            a = mid
                                            fa = fmid
                                    except Exception:
                                        is_unif_equi = False
                                        break
                                if not is_unif_equi:
                                    break
                                c = (a + b) / 2.0
                                if 1e-5 < c < 1.0 - 1e-5:
                                    try:
                                        L = float(witness_func(c - 1e-10))
                                        R = float(witness_func(c + 1e-10))
                                        if abs(L - R) > 0.05:
                                            is_unif_equi = False
                                            break
                                    except Exception:
                                        is_unif_equi = False
                                        break
                
                neg_q_ok = not is_unif_equi

    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: B_n(f)(x) is the n-th Bernstein polynomial for f", "¬Q: The sequence of polynomials B_n(f) is not uniformly equicontinuous on the unit interval"]
N_HYP = 1
NEG_Q_INDEX = 1