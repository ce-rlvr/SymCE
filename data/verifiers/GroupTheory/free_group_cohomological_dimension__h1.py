import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    The conjecture claims that the cohomological dimension of F over Z is exactly 1.
    By Stallings' theorem, a group has cohomological dimension 1 iff it is a non-trivial free group.
    """
    try:
        is_free_non_trivial = False
        
        # Check if it is explicitly presented as a non-trivial free group
        if hasattr(witness, 'relators') and hasattr(witness, 'generators'):
            if len(witness.relators) == 0 and len(witness.generators) > 0:
                is_free_non_trivial = True
                
        # If it is a finite group, its cohomological dimension is 0 (if trivial) or infinite.
        if not is_free_non_trivial and hasattr(witness, 'order'):
            try:
                if witness.order() < float('inf'):
                    is_free_non_trivial = False
            except Exception:
                pass
                
        neg_q = not is_free_non_trivial
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The cohomological dimension of F over Z is not exactly 1"
]

N_HYP = 0
NEG_Q_INDEX = 0