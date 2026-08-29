import sympy as sp
from sympy.abc import x
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness) -> list[bool]:
    if isinstance(witness, tuple) and len(witness) == 2:
        f, K_poly = witness
    else:
        f = witness
        K_poly = witness

    try:
        h1 = bool(sp.simplify(f - (x**5 + 20*x + 16)) == 0)
    except Exception:
        h1 = False

    try:
        poly = sp.Poly(K_poly, x)
        if poly.degree() != 5:
            neg_q = True
        else:
            disc = poly.discriminant()
            if not sp.sqrt(disc).is_integer:
                neg_q = True
            else:
                has_order_3 = False
                for p in sp.primerange(2, 100):
                    if disc % p == 0:
                        continue
                    try:
                        factors = sp.factor_list(poly, modulus=p)[1]
                        degrees = sorted([fac[0].degree() for fac in factors])
                        if degrees == [1, 1, 3]:
                            has_order_3 = True
                            break
                    except Exception:
                        pass
                neg_q = not has_order_3
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = ['H_1: f is x^5 + 20x + 16', 'neg_Q: Gal is NOT isomorphic to A_5']
N_HYP = 1
NEG_Q_INDEX = 1