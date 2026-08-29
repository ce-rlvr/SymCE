import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x', real=True)
Interval = sympy.Interval
Union = sympy.Union
FiniteSet = sympy.FiniteSet
oo = sympy.oo

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (X, f) where:
      - X is a sympy.Set representing the domain.
      - f is a sympy.Expr representing the function f(x).
    """
    try:
        X, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        free_syms = f.free_symbols
        if len(free_syms) > 1:
            return [False, False, False]
        elif len(free_syms) == 1:
            sym = list(free_syms)[0]
        else:
            sym = x
    except Exception:
        return [False, False, False]

    # H_1: f is continuous on X
    try:
        if not X.is_subset(sympy.S.Reals):
            h1 = False
        else:
            cdomain = sympy.continuous_domain(f, sym, sympy.S.Reals)
            is_sub = X.is_subset(cdomain)
            h1 = False if is_sub is None else bool(is_sub)
    except Exception:
        h1 = False

    # H_2: f(x) != 0 for all x in X
    try:
        zeros = sympy.solveset(f, sym, domain=sympy.S.Reals)
        is_emp = zeros.intersect(X).is_empty
        h2 = False if is_emp is None else bool(is_emp)
    except Exception:
        h2 = False

    # ¬Q: f(X) is neither a subset of (0, ∞) nor (-∞, 0)
    # This means f takes both strictly positive and strictly negative values on X.
    try:
        rng = sympy.function_range(f, sym, X)
        pos_int = rng.intersect(sympy.Interval(0, sympy.oo, left_open=True, right_open=True))
        neg_int = rng.intersect(sympy.Interval(-sympy.oo, 0, left_open=True, right_open=True))
        
        pos_empty = pos_int.is_empty
        neg_empty = neg_int.is_empty
        
        if pos_empty is None or neg_empty is None:
            neg_q = False
        else:
            has_pos = not pos_empty
            has_neg = not neg_empty
            neg_q = bool(has_pos and has_neg)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on X",
    "H_2: f(x) != 0 for all x in X",
    "¬Q: f(X) is neither a subset of (0, ∞) nor (-∞, 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2