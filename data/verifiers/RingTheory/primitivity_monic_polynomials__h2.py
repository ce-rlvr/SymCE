import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a UFD, then the content c(f) is a unit in R, making f a primitive polynomial."
    (The dropped hypothesis was that f is monic).
    """
    try:
        # Parse the witness into a sympy Poly object
        if isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[0], 'is_UFD'):
                f = Poly(witness[1], domain=witness[0])
            elif hasattr(witness[1], 'is_UFD'):
                f = Poly(witness[0], domain=witness[1])
            else:
                f = Poly(witness[0])
        elif not isinstance(witness, Poly):
            f = Poly(witness)
        else:
            f = witness
    except Exception:
        return [False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        R = f.domain
        is_ufd = getattr(R, 'is_UFD', False)
        if callable(is_ufd):
            is_ufd = is_ufd()
        h1 = bool(is_ufd)
    except Exception:
        h1 = False

    # ¬Q: The content c(f) is NOT a unit in R (f is NOT primitive)
    try:
        prim = getattr(f, 'is_primitive', True)
        if callable(prim):
            prim = prim()
        neg_q = not bool(prim)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: The content c(f) is not a unit in R (f is not primitive)"
]

N_HYP = 1
NEG_Q_INDEX = 1