import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
Z1 = {0}
trivial_ring = {0}

def conditions(witness) -> list[bool]:
    R, n = None, None
    
    if isinstance(witness, dict):
        n = witness.get('n')
        R = witness.get('R', witness.get('r'))
    elif isinstance(witness, tuple) and len(witness) == 2:
        a, b = witness
        a_is_int = isinstance(a, (int, Integer))
        b_is_int = isinstance(b, (int, Integer))
        
        if a_is_int and a >= 2 and not (b_is_int and b >= 2):
            n, R = a, b
        elif b_is_int and b >= 2 and not (a_is_int and a >= 2):
            n, R = b, a
        else:
            R, n = a, b
    else:
        if isinstance(witness, (int, Integer)) and witness >= 2:
            n = witness
            R = 0  # Implicitly the trivial ring
        else:
            R = witness
            n = 2  # Implicitly n=2

    # H1: n is an integer such that n >= 2
    try:
        h1 = isinstance(n, (int, Integer)) and n >= 2
    except Exception:
        h1 = False

    # neg_Q: M_n(R) does NOT contain non-zero zero divisors
    # This is true iff R is the trivial ring.
    try:
        neg_q = False
        try:
            if R == 0 or R == 1:
                neg_q = True
        except Exception:
            pass
        
        if isinstance(R, str) and R in ['Z1', 'Z_1', 'Z/1Z', 'trivial', 'zero']:
            neg_q = True
        elif isinstance(R, (list, set, tuple)) and len(R) == 1:
            neg_q = True
        elif hasattr(R, 'is_trivial') and R.is_trivial:
            neg_q = True
        elif hasattr(R, 'order'):
            if callable(R.order) and R.order() == 1:
                neg_q = True
            elif not callable(R.order) and R.order == 1:
                neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "¬Q: The matrix ring M_n(R) does not contain non-zero zero divisors"
]

N_HYP = 1
NEG_Q_INDEX = 1