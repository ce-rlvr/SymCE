import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        f = x**4 + 8*x + 12
        h1_ok = all(c.is_rational for c in sympy.Poly(f, x).coeffs())
    except Exception:
        h1_ok = False

    try:
        if not hasattr(witness, 'order'):
            neg_q_ok = False
        elif witness.order() != 12:
            neg_q_ok = True
        else:
            is_A4 = False
            try:
                if hasattr(witness, 'is_isomorphic'):
                    is_A4 = witness.is_isomorphic(A4)
                else:
                    is_A4 = witness.derived_subgroup().order() == 4
            except Exception:
                is_A4 = witness.derived_subgroup().order() == 4
            neg_q_ok = not is_A4
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: f(x) = x^4 + 8x + 12 is in Q", "not Q: The Galois group Gal(E/Q) is not isomorphic to A4"]

N_HYP = 1
NEG_Q_INDEX = 1