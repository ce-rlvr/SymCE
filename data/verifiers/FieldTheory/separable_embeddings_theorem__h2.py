import sympy
from sympy import Poly
from sympy.abc import x, y, z, t
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2,2)
O3 = sympy.zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            P = witness.get('poly', witness)
        elif isinstance(witness, (tuple, list)):
            P = witness[0]
        else:
            P = witness

        if isinstance(P, Poly):
            poly = P
        else:
            poly = Poly(P)
            
        deg = poly.degree()

        h1_ok = False
        if deg >= 1:
            is_irred = poly.is_irreducible
            dP = poly.diff()
            if dP.is_zero:
                is_sep = False
            else:
                g = poly.gcd(dP)
                is_sep = (g.degree() == 0)
            h1_ok = bool(is_irred and is_sep)

        q_ok = False
        if deg >= 1:
            dP = poly.diff()
            if dP.is_zero:
                has_deg_roots = False
            else:
                g = poly.gcd(dP)
                has_deg_roots = (g.degree() == 0)
            q_ok = bool(has_deg_roots)

        neg_q = not q_ok

        return [h1_ok, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: L over K is a finite separable field extension",
    "neg_Q: The number of distinct K-homomorphisms from L into the algebraic closure is not equal to the degree"
]

N_HYP = 1
NEG_Q_INDEX = 1