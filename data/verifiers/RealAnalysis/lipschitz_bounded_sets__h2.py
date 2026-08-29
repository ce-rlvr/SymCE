import sympy
from sympy import Symbol, S, oo, Interval, Union
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup for witness expressions
x = Symbol('x', real=True)
Reals = S.Reals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (f, A) where:
      - f is a sympy expression representing a function f: R -> R
      - A is a sympy Set representing a subset of R
    """
    try:
        if len(witness) != 2:
            return [False, False]
        f, A = witness
    except Exception:
        return [False, False]
    
    # H_1: f is Lipschitz continuous on Reals
    h1 = False
    try:
        if A.is_subset(S.Reals):
            df = f.diff(x)
            # A function is Lipschitz if its derivative is bounded.
            if df.is_constant() and df.is_real and (df.is_finite != False):
                h1 = True
            else:
                frange = function_range(df, x, S.Reals)
                if frange.inf > -oo and frange.sup < oo:
                    h1 = True
    except Exception:
        pass

    # ¬Q: The image set f(A) is unbounded
    neg_q = False
    try:
        frange_A = function_range(f, x, A)
        if frange_A.inf == -oo or frange_A.sup == oo:
            neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is Lipschitz continuous",
    "¬Q: f(A) is unbounded"
]

N_HYP = 1
NEG_Q_INDEX = 1