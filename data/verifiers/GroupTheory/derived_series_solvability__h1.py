import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    try:
        # P: G is a solvable group
        P = bool(witness.is_solvable)
        
        # Q: there exists an integer n >= 0 such that G^(n) is the trivial subgroup
        # By the theorem "Solvability via Derived Series", G^(n) denotes the n-th derived subgroup.
        # witness.derived_series() computes the derived series until it stabilizes.
        # It reaches the trivial subgroup if and only if the last element is trivial.
        ds = witness.derived_series()
        Q = bool(ds[-1].is_trivial)
        
        # The conclusion is the equivalence P <==> Q
        conclusion = (P == Q)
        
        # neg_Q is True when the conclusion fails at the witness
        neg_Q = not conclusion
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The equivalence between G being solvable and its derived series terminating at the trivial subgroup fails"
]

N_HYP = 0
NEG_Q_INDEX = 0