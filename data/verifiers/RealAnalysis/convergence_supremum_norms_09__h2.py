import sympy
from sympy import Abs, oo, limit

# Top-level setup for potential witness expressions
# (No specific named groups or matrices are needed for this real analysis theorem)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary or object providing:
      - S: a SymPy set (e.g., sympy.S.Reals)
      - f_n: a SymPy expression representing the sequence of functions f_n(x)
      - f: a SymPy expression representing the limit function f(x)
      - x: the SymPy symbol used for the spatial variable
      - n: the SymPy symbol used for the sequence index
    """
    # Extract witness components safely
    try:
        if isinstance(witness, dict):
            S = witness['S']
            f_n = witness['f_n']
            f = witness['f']
            x = witness['x']
            n = witness['n']
        else:
            S = witness.S
            f_n = witness.f_n
            f = witness.f
            x = witness.x
            n = witness.n
    except Exception:
        return [False, False, False]

    # H_1: S is a non-empty set
    try:
        h1_ok = bool(S.is_empty == False)
    except Exception:
        h1_ok = False

    # H_2: The sequence {f_n} converges uniformly to f on S
    try:
        diff = Abs(f_n - f)
        sup_diff = sympy.calculus.util.maximum(diff, x, S)
        lim_sup_diff = limit(sup_diff, n, oo)
        h2_ok = bool(lim_sup_diff == 0)
    except Exception:
        h2_ok = False

    # ¬Q: The sequence of real numbers sup |f_n(x)| converges to sup |f(x)| FAILS
    # It fails if the supremum is infinite (so it's not a sequence of real numbers),
    # or if the limit of the supremums does not equal the supremum of the limit.
    try:
        sup_fn = sympy.calculus.util.maximum(Abs(f_n), x, S)
        sup_f = sympy.calculus.util.maximum(Abs(f), x, S)
        
        lim_sup_fn = limit(sup_fn, n, oo)
        
        if lim_sup_fn == oo or sup_f == oo:
            neg_Q_ok = True
        else:
            neg_Q_ok = bool(lim_sup_fn != sup_f)
    except Exception:
        neg_Q_ok = False

    return [h1_ok, h2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: S is a non-empty set",
    "H_2: The sequence {f_n} converges uniformly to f on S",
    "¬Q: The sequence sup |f_n(x)| is not a sequence of real numbers, or does not converge to sup |f(x)|"
]

N_HYP = 2
NEG_Q_INDEX = 2