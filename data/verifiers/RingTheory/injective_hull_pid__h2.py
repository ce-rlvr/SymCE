import sympy
from sympy import ZZ, QQ, Symbol

# Top-level setup for the witness context
x = Symbol('x')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (R, K) where R is a ring and K is a module/ring.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, K = witness
        else:
            R = witness
            K = None
    except Exception:
        return [False, False]

    # H_1: R is a principal ideal domain
    try:
        # In SymPy, domains have the `is_PID` property
        h1 = bool(getattr(R, 'is_PID', False))
    except Exception:
        h1 = False

    # ¬Q: K is not the injective hull of R
    try:
        # For an integral domain, the injective hull as an R-module is its field of fractions.
        if hasattr(R, 'get_field'):
            inj_hull = R.get_field()
        elif hasattr(R, 'frac_field'):
            inj_hull = R.frac_field()
        else:
            inj_hull = None
            
        if inj_hull is not None and K is not None:
            neg_q = (K != inj_hull)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: K is not the injective hull of R"
]

N_HYP = 1
NEG_Q_INDEX = 1