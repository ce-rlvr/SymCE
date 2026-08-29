import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "¬Q: I^m I^n != I^{m+n}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False]
        R, I, m, n = witness
    except Exception:
        return [False, False, False]

    # H1: R is a ring
    try:
        h1 = False
        if hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
        elif hasattr(R, 'is_ring') and R.is_ring:
            h1 = True
        elif hasattr(R, 'zero'):
            h1 = True
        h1 = bool(h1)
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    try:
        h2 = False
        if type(I).__name__ in ('PolyIdeal', 'Ideal'):
            h2 = True
        elif hasattr(I, 'is_Ideal') and I.is_Ideal:
            h2 = True
        elif hasattr(I, 'ring'):
            h2 = True
        elif hasattr(I, 'gens'):
            h2 = True
        h2 = bool(h2)
    except Exception:
        h2 = False

    # neg_Q: I^m I^n != I^{m+n}
    try:
        def is_numeric_int(x):
            if isinstance(x, int):
                return True
            if isinstance(x, sympy.Integer):
                return True
            if isinstance(x, float) and x.is_integer():
                return True
            return False

        if not is_numeric_int(m) or not is_numeric_int(n):
            return [h1, h2, False]

        left = (I**m) * (I**n)
        right = I**(m+n)
        neg_q = bool(left != right)
    except Exception:
        # If negative powers or other invalid operations are attempted, 
        # the identity is undefined and therefore fails to hold.
        neg_q = True

    return [h1, h2, neg_q]