import sympy
from sympy import Poly, Symbol, isprime, GF, QQ, ZZ
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let K be a field of prime characteristic p. Let a be an element of K.
    Then x^p - a is irreducible over K."
    """
    try:
        # Witness can be (K, p, a) or just (p, a) where K is implicitly GF(p)
        if isinstance(witness, tuple):
            if len(witness) == 3:
                K, p, a = witness
            elif len(witness) == 2:
                p, a = witness
                K = GF(p)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: K is a field of prime characteristic p
    try:
        h1 = bool(getattr(K, 'is_Field', False) and isprime(p) and getattr(K, 'characteristic', None) == p)
    except Exception:
        h1 = False

    # H_2: a is an element of K
    try:
        a_val = K(a)
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: x^p - a is NOT irreducible over K (i.e., it is reducible)
    try:
        if h1 and h2:
            x_sym = Symbol('x')
            a_sym = K.to_sympy(a_val)
            poly = Poly(x_sym**p - a_sym, x_sym, domain=K)
            neg_q = not poly.is_irreducible
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of prime characteristic p",
    "H_2: a is an element of K",
    "¬Q: x^p - a is reducible over K"
]

N_HYP = 2
NEG_Q_INDEX = 2