import sympy
from sympy import Poly, RootOf, factor_list, degree, real_roots
from sympy.abc import x
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup
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
    """
    Checks if the witness (a polynomial in x over Q representing the field extension K = Q[x]/(P(x)))
    satisfies the hypotheses and falsifies the conclusion of the conjecture.
    """
    try:
        P = Poly(witness, x, domain='QQ')
        factors = factor_list(P)[1]
        is_irred = (len(factors) == 1 and factors[0][1] == 1)
        h1 = bool(is_irred and P.degree() >= 1)
    except Exception:
        h1 = False

    try:
        P = Poly(witness, x, domain='QQ')
        h2 = bool(P.degree() >= 1)
    except Exception:
        h2 = False

    try:
        P = Poly(witness, x, domain='QQ')
        deg = P.degree()
        if deg <= 1:
            neg_q = False
        else:
            real_roots_count = len(real_roots(P))
            if 0 < real_roots_count < deg:
                is_gal = False
            else:
                r = RootOf(P, 0)
                factors = factor_list(P.as_expr(), extension=r)[1]
                is_gal = True
                for fac, mult in factors:
                    if degree(fac, x) > 1:
                        is_gal = False
                        break
            neg_q = not is_gal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field extension of F",
    "H_2: The extension K/F is finite",
    "¬Q: The map E -> Gal(K/E) is not a bijection (K/F is not Galois)"
]

N_HYP = 2
NEG_Q_INDEX = 2