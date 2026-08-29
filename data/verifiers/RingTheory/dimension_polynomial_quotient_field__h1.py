import sympy
from sympy import Symbol, Poly

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness)
        h1 = len(f.gens) == 1
    except Exception:
        h1 = False

    try:
        h2 = h1 and f.degree() >= 1
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            # The conclusion states that the quotient ring is an n-dimensional vector space over F.
            # This requires F to be a field. If F is a field, the quotient is always an 
            # n-dimensional vector space. If F is not a field, it cannot be a vector space over F.
            # Therefore, the conclusion fails if and only if the domain F is not a field.
            neg_q = not f.domain.is_Field
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f is a polynomial",
    "H_2: The degree of f is n, where n >= 1",
    "¬Q: The quotient ring is not an n-dimensional vector space"
]

N_HYP = 2
NEG_Q_INDEX = 2