import sympy as sp
from sympy.abc import x
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

CONDITION_LABELS = [
    "H_1: The extension K/F is finite",
    "H_2: The extension K/F is Galois",
    "not Q: The order of the Galois group Gal(K/F) is not equal to the degree of K over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_finite', False))
            h2 = bool(witness.get('is_galois', False))
            neg_q = witness.get('galois_group_order') != witness.get('degree')
            return [h1, h2, neg_q]
        except Exception:
            pass

    try:
        h1 = bool(getattr(witness, 'is_finite', False))
        h2 = bool(getattr(witness, 'is_galois', False))
        gal_order = getattr(witness, 'galois_group_order', None)
        degree = getattr(witness, 'degree', None)
        if gal_order is not None and degree is not None:
            neg_q = (gal_order != degree)
            return [h1, h2, neg_q]
    except Exception:
        pass

    if isinstance(witness, tuple) and len(witness) == 4:
        try:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            neg_q = witness[2] != witness[3]
            return [h1, h2, neg_q]
        except Exception:
            pass

    try:
        f = sp.Poly(witness)
        if f.degree() > 0:
            h1 = bool(f.is_irreducible)
            deg = f.degree()
            if f.domain == sp.QQ and deg <= 6:
                from sympy.polys.galoisalg import galois_group
                G, _ = galois_group(f)
                gal_order = G.order()
                h2 = (gal_order == deg)
                neg_q = (gal_order != deg)
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]