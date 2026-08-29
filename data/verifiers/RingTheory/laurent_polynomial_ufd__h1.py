import sympy
from sympy import Symbol
from sympy.polys.domains import ZZ, QQ, EX

x = Symbol('x')

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a ring R (e.g., a SymPy domain) over which x is an indeterminate.
    """
    if isinstance(witness, tuple):
        R = witness[0]
    else:
        R = witness

    try:
        # H_1: x is an indeterminate over R
        # We verify this by checking if R is a valid ring structure in SymPy.
        h1_ok = hasattr(R, 'is_UFD')
    except Exception:
        h1_ok = False

    try:
        # not Q: The ring of Laurent polynomials is NOT a Unique Factorization Domain.
        # The Laurent polynomial ring over R is a UFD if and only if R is a UFD.
        # Therefore, the conclusion fails (is NOT a UFD) exactly when R is NOT a UFD.
        if hasattr(R, 'is_UFD'):
            neg_q_ok = (R.is_UFD is False)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is an indeterminate over R",
    "not Q: The ring of Laurent polynomials is not a Unique Factorization Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1