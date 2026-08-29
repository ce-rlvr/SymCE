import sympy
from sympy import QQ, GF, Rational, Integer, Symbol, Poly

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            K, a, b = witness
        elif len(witness) == 2:
            K = QQ
            a, b = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H1: K is a field of characteristic not equal to 2
    try:
        h1 = bool(K.is_Field and K.characteristic != 2)
    except Exception:
        h1 = False

    # H2: a and b are elements of K
    try:
        h2 = bool(a in K and b in K)
        if h2:
            a_K = K.convert(a)
            b_K = K.convert(b)
    except Exception:
        h2 = False

    # H3: a^2 - 4b is not a square in K
    try:
        if h2:
            four = K.convert(4)
            val3 = a_K**2 - four*b_K
            poly3 = Poly([K.one, K.zero, -val3], x, domain=K)
            h3 = bool(len(poly3.ground_roots()) == 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: b(a^2 - 4b) is not a square in K
    try:
        if h2:
            four = K.convert(4)
            val4 = b_K * (a_K**2 - four*b_K)
            poly4 = Poly([K.one, K.zero, -val4], x, domain=K)
            h4 = bool(len(poly4.ground_roots()) == 0)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: x^4 + a*x^2 + b is reducible over K
    try:
        if h2:
            polyQ = Poly([K.one, K.zero, a_K, K.zero, b_K], x, domain=K)
            neg_q = (polyQ.is_irreducible is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2",
    "H_2: a and b are elements of K",
    "H_3: a^2 - 4b is not a square in K",
    "H_4: b(a^2 - 4b) is not a square in K",
    "¬Q: x^4 + a x^2 + b is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4