import sympy
from sympy.polys.domains import ZZ, QQ
from sympy import Symbol

# Top-level setup: named object bindings
x = Symbol('x')
y = Symbol('y')

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, K, S) or a dictionary with these keys,
    checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            S = witness.get('S')
        else:
            R, K, S = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a principal ideal domain
    try:
        if hasattr(R, 'is_PID'):
            h1 = bool(R.is_PID)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        if hasattr(R, 'get_field'):
            h2 = bool(K == R.get_field())
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: S is not a principal ideal domain
    try:
        if hasattr(S, 'is_PID'):
            neg_q = not bool(S.is_PID)
        else:
            # If S doesn't have the is_PID property, it's not a valid ring object in this context
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: K is the field of fractions of R",
    "¬Q: S is not a principal ideal domain"
]

N_HYP = 2
NEG_Q_INDEX = 2