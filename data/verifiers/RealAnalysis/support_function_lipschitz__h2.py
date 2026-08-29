import sympy
from sympy import FiniteSet, Interval, ProductSet, Reals, Symbol, oo
from sympy.abc import x, y, z

# Top-level setup
R = Reals

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        if isinstance(witness, (list, tuple, set)):
            w = FiniteSet(*witness)
        else:
            w = witness
            
        if isinstance(w, sympy.Set):
            h1 = (w.is_empty is False) and (w.is_bounded is True)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (list, tuple, set)):
            w = FiniteSet(*witness)
        else:
            w = witness
            
        if isinstance(w, sympy.Set):
            # The support function h_K(x) = sup_{y \in K} <x, y> is globally Lipschitz 
            # continuous on R^n if and only if K is bounded.
            # Therefore, the conclusion fails (h_K is NOT globally Lipschitz) iff K is unbounded.
            neg_q = (w.is_bounded is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a non-empty, bounded subset of R^n",
    "¬Q: The support function h_K is not globally Lipschitz continuous on R^n"
]

N_HYP = 1
NEG_Q_INDEX = 1