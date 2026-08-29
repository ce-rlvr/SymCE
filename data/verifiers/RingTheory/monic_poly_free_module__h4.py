import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            n = witness.get('n')
        else:
            f, n = witness
    except Exception:
        return [False, False, False, False]

    try:
        poly_f = Poly(f)
        h1 = True
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f)
        h2 = len(poly_f.gens) <= 1
    except Exception:
        h2 = False

    try:
        poly_f = Poly(f)
        h3 = (poly_f.LC() == 1)
    except Exception:
        h3 = False

    try:
        poly_f = Poly(f)
        if not isinstance(n, (int, sympy.Integer)):
            neg_q = True
        else:
            neg_q = (n != poly_f.degree()) or (n < 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ['H_1: R is a commutative ring', 'H_2: f is a polynomial', 'H_3: f is monic', 'not Q: factor ring is not free module of rank n']
N_HYP = 3
NEG_Q_INDEX = 3