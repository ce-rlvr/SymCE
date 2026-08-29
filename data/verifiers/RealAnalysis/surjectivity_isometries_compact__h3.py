import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')

def conditions(witness) -> list[bool]:
    try:
        X, f = witness
    except Exception:
        return [False, False, False]

    # H_1: X is a compact metric space
    h1_ok = False
    try:
        if isinstance(X, (list, tuple, set)):
            h1_ok = True
        elif isinstance(X, sympy.FiniteSet):
            h1_ok = True
        elif isinstance(X, sympy.Interval):
            h1_ok = (not X.left_open) and (not X.right_open) and X.start.is_finite and X.end.is_finite
        elif isinstance(X, sympy.Union):
            def is_compact(S):
                if isinstance(S, sympy.FiniteSet): 
                    return True
                if isinstance(S, sympy.Interval):
                    return (not S.left_open) and (not S.right_open) and S.start.is_finite and S.end.is_finite
                return False
            h1_ok = all(is_compact(arg) for arg in X.args)
    except Exception:
        h1_ok = False

    # H_2: f: X -> X is a mapping
    h2_ok = False
    try:
        if isinstance(X, (list, tuple, set, sympy.FiniteSet)):
            h2_ok = True
            for elem in X:
                if isinstance(f, dict):
                    fx = f[elem]
                elif callable(f):
                    fx = f(elem)
                else:
                    f_expr = sympy.sympify(f)
                    syms = list(f_expr.free_symbols)
                    fx = f_expr.subs(syms[0], elem) if syms else f_expr
                if fx not in X:
                    h2_ok = False
                    break
        elif isinstance(X, sympy.Interval):
            f_expr = f(sympy.Symbol('x')) if callable(f) else f
            f_expr = sympy.sympify(f_expr)
            syms = list(f_expr.free_symbols)
            x_sym = syms[0] if syms else sympy.Symbol('x')
            min_val = sympy.calculus.util.minimum(f_expr, x_sym, X)
            max_val = sympy.calculus.util.maximum(f_expr, x_sym, X)
            h2_ok = bool((min_val >= X.start) and (max_val <= X.end))
    except Exception:
        h2_ok = False

    # neg_Q: f is not surjective
    neg_q_ok = False
    try:
        if isinstance(X, (list, tuple, set)):
            image = set()
            for elem in X:
                if isinstance(f, dict):
                    fx = f[elem]
                elif callable(f):
                    fx = f(elem)
                else:
                    f_expr = sympy.sympify(f)
                    syms = list(f_expr.free_symbols)
                    fx = f_expr.subs(syms[0], elem) if syms else f_expr
                image.add(fx)
            neg_q_ok = len(image) < len(set(X))
        elif isinstance(X, sympy.FiniteSet):
            image = set()
            for elem in X:
                if isinstance(f, dict):
                    fx = f[elem]
                elif callable(f):
                    fx = f(elem)
                else:
                    f_expr = sympy.sympify(f)
                    syms = list(f_expr.free_symbols)
                    fx = f_expr.subs(syms[0], elem) if syms else f_expr
                image.add(fx)
            neg_q_ok = len(image) < len(X)
        elif isinstance(X, sympy.Interval):
            f_expr = f(sympy.Symbol('x')) if callable(f) else f
            f_expr = sympy.sympify(f_expr)
            syms = list(f_expr.free_symbols)
            x_sym = syms[0] if syms else sympy.Symbol('x')
            min_val = sympy.calculus.util.minimum(f_expr, x_sym, X)
            max_val = sympy.calculus.util.maximum(f_expr, x_sym, X)
            neg_q_ok = bool((min_val > X.start) or (max_val < X.end))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: f: X -> X is a mapping",
    "¬Q: The mapping f is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2