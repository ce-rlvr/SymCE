import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        # The conjecture claims the group admits the presentation of the Higman group.
        # The Higman group is an infinite group with 4 generators and 4 relators of length 5.
        is_higman = False
        
        if hasattr(witness, 'generators') and hasattr(witness, 'relators'):
            if len(witness.generators) == 4 and len(witness.relators) == 4:
                try:
                    # Check if all relators have length 5 (e.g., a*b*a**-1*b**-2)
                    if all(len(r) == 5 for r in witness.relators):
                        is_higman = True
                except Exception:
                    pass
        
        # Finite groups (like PermutationGroups) cannot be the Higman group
        if isinstance(witness, PermutationGroup):
            is_higman = False
            
        # The conclusion fails if the witness is NOT the Higman group
        neg_q = not is_higman
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G does not admit the presentation of the Higman group"
]

N_HYP = 0
NEG_Q_INDEX = 0