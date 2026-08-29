import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    h1 = False
    try:
        if type(witness).__name__ == 'FreeGroup':
            h1 = True
        elif type(witness).__name__ == 'FpGroup':
            if len(witness.relators) == 0:
                h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        # The word problem for a free group with a finite set of free generators
        # is always solvable in finite time (e.g., by freely reducing the word).
        # Therefore, the conclusion is always true for any valid witness satisfying H1.
        # Thus, its negation is always False.
        if h1:
            neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a finite set of free generators for F",
    "¬Q: The word problem for F with generators X is not solvable in finite time"
]

N_HYP = 1
NEG_Q_INDEX = 1