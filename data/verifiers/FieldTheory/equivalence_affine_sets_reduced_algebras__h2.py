import sympy
from sympy import CC, QQ, ZZ, Symbol

x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: A is a reduced ring",
    "¬Q: A is not isomorphic as a K-algebra to the coordinate ring of V"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        K, A = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (K == CC)
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if A in (ZZ, QQ, CC):
            h2 = True
        elif hasattr(A, 'is_Field') and A.is_Field:
            h2 = True
        elif A.__class__.__name__ in ('FracField', 'PolyRing', 'FractionField', 'PolynomialRing'):
            h2 = True
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        if A in (ZZ, QQ):
            neg_q = True
        elif A.__class__.__name__ in ('FracField', 'FractionField'):
            if A != K:
                neg_q = True
        elif hasattr(A, 'is_Field') and A.is_Field:
            if A != K:
                neg_q = True
        elif A.__class__.__name__ in ('PolyRing', 'PolynomialRing'):
            if getattr(A, 'domain', None) != K:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]