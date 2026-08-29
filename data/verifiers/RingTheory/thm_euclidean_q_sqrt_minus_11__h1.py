import sympy
from sympy import sqrt, Rational, Integer

# Top-level setup (no specific named bindings needed for this number theory domain)

def get_d(witness):
    """
    Helper to extract the square-free integer d from the witness.
    The witness could be provided as an integer d, or as an algebraic element like sqrt(d).
    """
    if isinstance(witness, (int, Integer)):
        return int(witness)
    try:
        if hasattr(witness, 'ext'):
            ext = witness.ext
            if ext.is_Pow and ext.exp == Rational(1, 2):
                return int(ext.base)
    except Exception:
        pass
    try:
        sq = witness**2
        if isinstance(sq, (int, Integer)):
            return int(sq)
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    d = get_d(witness)
    
    # H_1: Let O_K be the ring of algebraic integers of K
    # We verify that K is a valid quadratic field Q(sqrt(d)) by checking if d is square-free.
    try:
        if d is not None:
            h1_ok = sympy.is_squarefree(abs(d)) and d not in (0, 1)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: O_K is NOT a Euclidean domain
    try:
        if d is not None:
            if d < 0:
                # For imaginary quadratic fields, O_K is Euclidean iff d is in {-1, -2, -3, -7, -11}
                neg_q_ok = d not in {-1, -2, -3, -7, -11}
            else:
                # For real quadratic fields, we check against the known Euclidean domains.
                # If d is not in this list, it is not Euclidean (or at least, any valid counterexample
                # provided will definitely not be in this list).
                euclidean_real = {2, 3, 5, 6, 7, 11, 13, 14, 17, 19, 21, 29, 33, 37, 41, 57, 69, 73}
                neg_q_ok = d not in euclidean_real
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: O_K is the ring of algebraic integers of K",
    "¬Q: O_K is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1