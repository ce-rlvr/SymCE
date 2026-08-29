import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
from sympy.abc import x, y, z
from sympy import Poly, roots

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        F, S = witness
    except Exception:
        return [False, False]
        
    # H1: F is a field
    try:
        h1 = False
        if F == sympy.QQ:
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
    except Exception:
        h1 = False
        
    # neg_Q: conclusion fails
    try:
        neg_q = False
        if F == sympy.QQ:
            all_roots_rational = True
            for p in S:
                poly = Poly(p, x)
                rts = roots(poly)
                if sum(rts.values()) != poly.degree():
                    all_roots_rational = False
                    break
                for r in rts.keys():
                    if not getattr(r, 'is_rational', False):
                        all_roots_rational = False
                        break
            
            if all_roots_rational:
                for p in S:
                    poly = Poly(p, x)
                    for c in poly.coeffs():
                        if not getattr(c, 'is_rational', False):
                            neg_q = True
                            break
                    if neg_q:
                        break
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "not Q: conclusion fails"
]

N_HYP = 1
NEG_Q_INDEX = 1