import sympy
from sympy import symbols, Poly

x, y = symbols('x y')

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, f = witness
        else:
            R = sympy.ZZ
            f = witness
    except Exception:
        return [False, False, False]

    h1 = False
    try:
        if R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
        elif hasattr(R, 'is_Ring') and getattr(R, 'is_Ring', False):
            h1 = True
        elif hasattr(R, 'is_commutative') and getattr(R, 'is_commutative', False):
            h1 = True
        elif isinstance(R, set):
            h1 = True
    except Exception:
        h1 = False

    h2 = False
    try:
        p = Poly(f, x)
        if set(p.free_symbols).issubset({x}):
            h2 = True
    except Exception:
        h2 = False

    # The factor ring R[x, y]/<y - f(x)> is always isomorphic to R[x] 
    # via the evaluation homomorphism y -> f(x).
    # Therefore, the conclusion is always true, and its negation is always False.
    neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f is a polynomial in the single variable x",
    "not Q: The factor ring is NOT isomorphic to the polynomial ring"
]

N_HYP = 2
NEG_Q_INDEX = 2