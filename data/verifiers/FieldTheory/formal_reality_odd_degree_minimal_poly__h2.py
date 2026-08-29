import sympy
from sympy import Poly, Matrix, QQ, RR, ZZ, eye, zeros, minimal_polynomial
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, Matrix):
            P = minimal_polynomial(witness, x)
            P = Poly(P, domain='QQ')
        elif isinstance(witness, Poly):
            P = witness
        else:
            P = Poly(witness)
            if P.domain == ZZ:
                P = Poly(witness, domain='QQ')
    except Exception:
        return [False, False, False]

    # H_1: F is a formally real field
    try:
        domain = P.domain
        is_field = getattr(domain, 'is_Field', False) or domain in [QQ, RR]
        
        if domain == QQ or domain == RR:
            is_formally_real = True
        elif getattr(domain, 'is_RealField', False):
            is_formally_real = True
        elif getattr(domain, 'is_AlgebraicField', False):
            is_formally_real = getattr(domain.ext, 'is_real', True)
        else:
            is_formally_real = False
            
        h1 = bool(is_field and is_formally_real)
    except Exception:
        h1 = False

    # H_2: The minimal polynomial of alpha over F has an odd degree
    try:
        h2 = bool(P.degree() % 2 == 1)
    except Exception:
        h2 = False

    # ¬Q: F(alpha) is not a formally real field
    # F(alpha) is isomorphic to F[x]/(P). It is a formally real field iff
    # P is irreducible and F is formally real.
    # Since H_1 checks if F is formally real, the conclusion fails iff P is NOT irreducible.
    try:
        irr = P.is_irreducible
        if irr is None:
            neg_q = False
        else:
            neg_q = not irr
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a formally real field",
    "H_2: The minimal polynomial of alpha over F has an odd degree",
    "¬Q: F(alpha) is not a formally real field"
]

N_HYP = 2
NEG_Q_INDEX = 2