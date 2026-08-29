import sympy
from sympy import Symbol, Sum, limit, oo, simplify
import math
import itertools
import functools

# Top-level setup
n = Symbol('n', integer=True, positive=True)
k = Symbol('k', integer=True, nonnegative=True)

def is_eventually_zero(expr, n_var):
    try:
        expr_simp = simplify(expr)
        if expr_simp == 0:
            return True
    except Exception:
        pass
    
    for i in range(100, 105):
        try:
            val = expr.subs(n_var, i)
            val_simp = simplify(val)
            if val_simp != 0:
                return False
        except Exception:
            return False
    return True

def get_radius(expr, n_var):
    if is_eventually_zero(expr, n_var):
        return oo
        
    try:
        ratio = simplify(abs(expr / expr.subs(n_var, n_var + 1)))
        L = limit(ratio, n_var, oo)
        if L.is_number or L == oo:
            return L
    except Exception:
        pass

    try:
        root = simplify(abs(expr)**(-1/n_var))
        L = limit(root, n_var, oo)
        if L.is_number or L == oo:
            return L
    except Exception:
        pass

    return None

def conditions(witness) -> list[bool]:
    # Parse witness: allow either a_n or s_n to be provided
    if isinstance(witness, dict):
        if 's_n' in witness:
            s_n = witness['s_n']
            try:
                a_n = simplify(s_n - s_n.subs(n, n-1))
            except Exception:
                return [False, False, False]
        elif 'a_n' in witness:
            a_n = witness['a_n']
            try:
                s_n = Sum(a_n.subs(n, k), (k, 0, n)).doit()
            except Exception:
                return [False, False, False]
        else:
            return [False, False, False]
    else:
        a_n = witness
        try:
            s_n = Sum(a_n.subs(n, k), (k, 0, n)).doit()
        except Exception:
            return [False, False, False]

    # H1: a_n defines a power series with a computable radius of convergence R
    try:
        R = get_radius(a_n, n)
        h1 = (R is not None)
    except Exception:
        h1 = False

    # H2: s_n is not eventually zero
    try:
        h2 = not is_eventually_zero(s_n, n)
    except Exception:
        h2 = False

    # Negated Conclusion: The radius of convergence of s_n is NOT equal to min(R, 1)
    try:
        R_s = get_radius(s_n, n)
        if R_s is None or R is None:
            neg_q = False
        else:
            expected_R_s = min(R, 1)
            neg_q = (R_s != expected_R_s)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a_n defines a power series with a computable radius of convergence R",
    "H_2: s_n is not eventually zero",
    "¬Q: The radius of convergence of s_n is NOT equal to min(R, 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2