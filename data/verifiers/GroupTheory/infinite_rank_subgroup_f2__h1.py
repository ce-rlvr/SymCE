import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings that the witness expression may reference.
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Evaluates the remaining hypotheses and the negated conclusion at the given witness.
    
    Conjecture:
      Hypothesis: The rank of F is at least 2.
      Conclusion: F contains a subgroup that is isomorphic to the free group of countably infinite rank.
    """
    # H_1: The rank of F is at least 2
    # For any group, rank >= 2 is equivalent to the group not being cyclic 
    # (since rank is the minimal number of generators, and rank <= 1 iff it is cyclic).
    try:
        if callable(witness.is_cyclic):
            h1_ok = not witness.is_cyclic()
        else:
            h1_ok = not witness.is_cyclic
        h1_ok = bool(h1_ok)
    except Exception:
        h1_ok = False

    # neg_Q: F does NOT contain a subgroup isomorphic to the free group of countably infinite rank
    # If F is a finite group, it cannot contain any infinite subgroup.
    try:
        if isinstance(witness, PermutationGroup):
            # All PermutationGroups in SymPy are finite.
            neg_q_ok = True
        else:
            # Fallback for other potential group objects
            order = witness.order() if callable(witness.order) else witness.order
            neg_q_ok = bool(order < float('inf'))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The rank of F is at least 2",
    "¬Q: F does not contain a subgroup isomorphic to the free group of countably infinite rank"
]

N_HYP = 1
NEG_Q_INDEX = 1