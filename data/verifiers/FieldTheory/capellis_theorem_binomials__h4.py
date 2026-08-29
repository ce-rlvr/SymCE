import sympy
from sympy import Symbol, Poly, QQ, Rational
from sympy.ntheory import factorint

# Top-level setup
# QQ and Rational are exposed for convenience in witness construction.
# The witness can be either a tuple (K, n, a) or (n, a) where K defaults to QQ.

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                K, n, a = witness
            elif len(witness) == 2:
                K = QQ
                n, a = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: K is a field
    try:
        h1 = getattr(K, 'is_Field', False)
        if not h1 and K == QQ:
            h1 = True
    except Exception:
        h1 = False

    # H2: n >= 2 is an integer
    try:
        h2 = isinstance(n, int) and n >= 2
    except Exception:
        h2 = False

    # H3: a in K and a not in K^p for all prime factors p of n
    try:
        h3 = True
        a_K = K(a)
        primes = factorint(n).keys()
        x = Symbol('x')
        for p in primes:
            poly = Poly(x**p - a_K, x, domain=K)
            if len(poly.ground_roots()) > 0:
                h3 = False
                break
    except Exception:
        h3 = False

    # neg_Q: x^n - a is NOT irreducible over K
    try:
        x = Symbol('x')
        poly = Poly(x**n - K(a), x, domain=K)
        # We check explicitly for False to avoid issues if is_irreducible returns None
        neg_q = (poly.is_irreducible is False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n >= 2 is an integer",
    "H_3: a in K and a not in K^p for all prime factors p of n",
    "¬Q: x^n - a is not irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3