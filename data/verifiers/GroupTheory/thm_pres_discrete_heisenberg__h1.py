import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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

def conditions(witness):
    try:
        neg_Q = False
        # The discrete Heisenberg group is infinite.
        # Any finite group (like those in sympy.combinatorics) cannot be isomorphic to it.
        if isinstance(witness, PermutationGroup):
            neg_Q = True
        elif hasattr(witness, 'order'):
            try:
                if witness.order() < float('inf'):
                    neg_Q = True
            except Exception:
                pass
        return [bool(neg_Q)]
    except Exception:
        return [False]

CONDITION_LABELS = ["¬Q: H does not admit the presentation of the discrete Heisenberg group"]

N_HYP = 0
NEG_Q_INDEX = 0