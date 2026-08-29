import sympy
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    try:
        # Check if the witness is a valid group object
        if not hasattr(witness, 'order') or not hasattr(witness, 'is_nilpotent'):
            return [False]
            
        # A finite group is torsion-free if and only if its order is 1 (the trivial group).
        # Any non-trivial finite group contains elements of finite order > 1 (torsion).
        is_torsion_free = (witness.order() == 1)
        is_nilpotent = bool(witness.is_nilpotent)
        
        # The conclusion states that G embeds into a torsion-free nilpotent group.
        # This is possible if and only if G itself is torsion-free and nilpotent.
        # Thus, the conclusion fails (neg_Q is True) if G is NOT torsion-free OR NOT nilpotent.
        neg_q = not (is_torsion_free and is_nilpotent)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: G is not torsion-free or not nilpotent (cannot embed into a torsion-free nilpotent group)"
]

N_HYP = 0
NEG_Q_INDEX = 0