import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: Assume that the order of G is strictly less than 60.
    try:
        if callable(getattr(witness, 'order', None)):
            ord_G = witness.order()
        elif hasattr(witness, 'order'):
            ord_G = witness.order
        else:
            raise AttributeError("Witness has no order attribute or method")
        h1 = bool(ord_G < 60)
    except Exception:
        h1 = False

    # ¬Q: G is not a solvable group.
    try:
        # In SymPy, solvable groups have the `is_solvable` property evaluate to True.
        # If the object lacks this property or it evaluates to False, it is not a solvable group.
        if hasattr(witness, 'is_solvable'):
            is_solv = bool(witness.is_solvable)
        else:
            is_solv = False
    except Exception:
        is_solv = False

    neg_q = not is_solv

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: order of G is strictly less than 60",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1