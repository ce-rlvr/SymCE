import sympy
from sympy import (
    Symbol, Interval, FiniteSet, Union, Intersection, Piecewise, Eq,
    oo, S, sin, cos, exp, log, floor, ceiling
)
from sympy.calculus.util import maximum, minimum
from sympy.solvers import solveset

# Top-level setup for witness expressions
x = Symbol('x', real=True)
Reals = S.Reals

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should provide a compact metric space X and a function f.
    It can be a tuple (X, f) or (X, d, f), a dictionary, or an object with attributes X and f.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                X, f = witness
            elif len(witness) == 3:
                X, d, f = witness
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            X = witness['X']
            f = witness['f']
        else:
            X = witness.X
            f = witness.f
    except Exception:
        return [False, False, False]
        
    # H_1: (X, d) is a non-empty metric space.
    # We verify this by checking if X is a non-empty subset of the Reals (which inherits the standard metric).
    try:
        h1 = bool(X.is_subset(Reals) and not X.is_empty)
    except Exception:
        h1 = False
        
    # H_2: X is compact.
    # By Heine-Borel, a subset of Reals is compact iff it is closed and bounded.
    try:
        is_bounded = X.is_bounded
        is_closed = X.is_closed
        if is_closed is None:
            is_closed = (X.closure == X)
        h2 = bool(is_bounded and is_closed)
    except Exception:
        h2 = False
        
    # ¬Q: The conclusion FAILS at the witness.
    # Conclusion: There exist a, b in X such that f(a) <= f(x) <= f(b) for all x in X.
    # Negation: f does NOT attain its global supremum OR does NOT attain its global infimum on X.
    try:
        if callable(f):
            f_expr = f(x)
            sym = x
        else:
            f_expr = f
            free_syms = f_expr.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
            elif len(free_syms) == 0:
                sym = x
            else:
                sym = x
                
        sup = maximum(f_expr, sym, X)
        inf = minimum(f_expr, sym, X)
        
        max_not_attained = False
        if sup == oo:
            max_not_attained = True
        else:
            max_sols = solveset(f_expr - sup, sym, domain=X)
            if max_sols.is_empty == True:
                max_not_attained = True
                
        min_not_attained = False
        if inf == -oo:
            min_not_attained = True
        else:
            min_sols = solveset(f_expr - inf, sym, domain=X)
            if min_sols.is_empty == True:
                min_not_attained = True
                
        neg_q = bool(max_not_attained or min_not_attained)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a non-empty metric space",
    "H_2: X is compact",
    "¬Q: f does not attain its global minimum or global maximum on X"
]

N_HYP = 2
NEG_Q_INDEX = 2