import sympy
from sympy import Poly, roots
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        p = Poly(witness, x)
        h1 = p.domain.is_QQ or p.domain.is_ZZ
    except Exception:
        h1 = False

    try:
        p = Poly(witness, x)
        h2 = p.degree() >= 1
    except Exception:
        h2 = False

    try:
        p = Poly(witness, x)
        rts = roots(witness, x, multiple=False)
        
        if len(rts) < p.degree():
            neg_q = False
        else:
            unique_rts = list(rts.keys())
            irr_rts = [r for r in unique_rts if not r.is_rational]
            
            if not irr_rts:
                deg = 1
            else:
                minpoly = primitive_element(irr_rts, x)
                deg = Poly(minpoly, x).degree()
                
            neg_q = (deg != 8)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is the field of rational numbers Q",
    "H_2: E is the splitting field of f(x) over Q",
    "not Q: The degree of the extension over Q is not 8"
]

N_HYP = 2
NEG_Q_INDEX = 2