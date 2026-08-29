import sympy
import math
import itertools
import functools

# Top-level setup for witness expressions
x = sympy.Symbol('x', real=True)
Piecewise = sympy.Piecewise
Interval = sympy.Interval
solveset = sympy.solveset
S = sympy.S

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: u is a vector in R^n",
    "H_3: v(0) . u > 0",
    "H_4: v(1) . u < 0",
    "¬Q: v(c) . u != 0 for all c in (0, 1)"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        n, u, v = witness
    except Exception:
        return [False] * 5
        
    # H1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False
        
    # H2: u is a vector in R^n
    try:
        if isinstance(u, sympy.Matrix):
            u = list(u)
        if n == 1 and not isinstance(u, (list, tuple)):
            u = [u]
        h2 = isinstance(u, (list, tuple)) and len(u) == n and all(
            isinstance(ui, (int, float, sympy.Basic)) and sympy.sympify(ui).is_real for ui in u
        )
    except Exception:
        h2 = False
        
    # Evaluate v
    try:
        if callable(v):
            v_expr = v(x)
        elif isinstance(v, (list, tuple)) and all(callable(vi) for vi in v):
            v_expr = [vi(x) for vi in v]
        else:
            v_expr = v
            
        if isinstance(v_expr, sympy.Matrix):
            v_expr = list(v_expr)
            
        if n == 1 and not isinstance(v_expr, (list, tuple)):
            v_expr = [v_expr]
            
        if not (isinstance(v_expr, (list, tuple)) and len(v_expr) == n):
            raise ValueError
    except Exception:
        return [h1, h2, False, False, False]
        
    # H3: v(0) . u > 0
    try:
        v0 = [sympy.sympify(vi).subs(x, 0) for vi in v_expr]
        dot0 = sum(vi * ui for vi, ui in zip(v0, u))
        h3 = bool(sympy.sympify(dot0 > 0))
    except Exception:
        h3 = False
        
    # H4: v(1) . u < 0
    try:
        v1 = [sympy.sympify(vi).subs(x, 1) for vi in v_expr]
        dot1 = sum(vi * ui for vi, ui in zip(v1, u))
        h4 = bool(sympy.sympify(dot1 < 0))
    except Exception:
        h4 = False
        
    # Negated Conclusion: No c in (0, 1) such that v(c) . u == 0
    try:
        dot_expr = sum(sympy.sympify(vi) * ui for vi, ui in zip(v_expr, u))
        sols = solveset(dot_expr, x, domain=Interval.open(0, 1))
        
        if sols is S.EmptySet or sols.is_empty == True:
            neg_q = True
        elif sols.is_empty == False:
            neg_q = False
        elif isinstance(sols, sympy.Set) and not isinstance(sols, sympy.ConditionSet):
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]