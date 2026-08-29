import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: G is not locally cyclic
    # For finite groups, being locally cyclic is equivalent to being cyclic.
    try:
        if not h1:
            neg_q = False
        else:
            n = witness.order()
            is_cyclic_attr = getattr(witness, 'is_cyclic', None)
            
            if isinstance(is_cyclic_attr, bool):
                is_cyclic = is_cyclic_attr
            elif n <= 2000:
                is_cyclic = False
                for g in witness.elements:
                    if g.order() == n:
                        is_cyclic = True
                        break
            else:
                # Fail-safe for excessively large groups without the property
                is_cyclic = True
                
            neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: G is not locally cyclic"
]

N_HYP = 1
NEG_Q_INDEX = 1