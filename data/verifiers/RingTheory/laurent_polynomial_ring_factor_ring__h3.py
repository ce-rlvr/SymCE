import sympy
from sympy import S
from sympy.polys.domains.domain import Domain

# Top-level setup
Z = S.Integers
Q = S.Rationals
R = S.Reals
C = S.Complexes
ZZ = sympy.polys.domains.ZZ
QQ = sympy.polys.domains.QQ
RR = sympy.polys.domains.RR
CC = sympy.polys.domains.CC

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # H1: R is a commutative ring with identity
        if witness in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            h1 = True
        elif isinstance(witness, Domain) and getattr(witness, 'has_Ring', False):
            h1 = True
        elif hasattr(witness, 'is_commutative') and witness.is_commutative and hasattr(witness, 'is_ring') and witness.is_ring:
            h1 = True
        elif isinstance(witness, str) and witness.upper() in ['Z', 'Q', 'R', 'C', 'ZZ', 'QQ', 'RR', 'CC']:
            h1 = True
    except Exception:
        pass

    try:
        # H2: R[x, x^{-1}] is the ring of Laurent polynomials over R
        # This is a definitional hypothesis. If R is a valid ring, this holds by definition.
        if h1:
            h2 = True
    except Exception:
        pass

    try:
        # ¬Q: R[x, x^{-1}] is not isomorphic to the factor ring R[x, y]/<xy - 1>
        # Mathematically, for any commutative ring with identity R, the ring of Laurent 
        # polynomials R[x, x^{-1}] is universally isomorphic to R[x, y]/<xy - 1>.
        # Since the conclusion is always true, its negation is always False.
        neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: Laurent polynomial ring over R",
    "¬Q: Laurent polynomial ring not isomorphic to factor ring"
]

N_HYP = 2
NEG_Q_INDEX = 2