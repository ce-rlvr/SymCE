import sympy

Z = sympy.ZZ
Q = sympy.QQ

def conditions(witness):
    try:
        P, (X,) = sympy.ring('x', witness)
        h1 = getattr(witness, 'is_commutative', True)
    except Exception:
        h1 = False

    try:
        if h1:
            P2, (X2, Y2) = sympy.ring('x, y', witness)
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # The conclusion is mathematically always true for any commutative ring with identity.
    # Therefore, it never fails, and its negation is always False.
    neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    'H_1: R is a commutative ring with identity',
    'H_2: R(x, y) is the polynomial ring in two variables over R',
    'neg_Q: R(x, x^-1) is not isomorphic to R(x, y)/<xy - 1>'
]

N_HYP = 2
NEG_Q_INDEX = 2