import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        G, N_iterable = witness
        N_list = list(N_iterable)
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: For every i in I, N_i is a normal subgroup of G
    try:
        h2 = True
        for N in N_list:
            if not isinstance(N, PermutationGroup):
                h2 = False
                break
            if not N.is_subgroup(G):
                h2 = False
                break
            if not N.is_normal(G):
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: The intersection of all N_i for i in I is NOT a normal subgroup of G
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            if not N_list:
                # The intersection of an empty family of subgroups of G is G itself
                intersection = G
            else:
                # Compute the intersection of all elements in the subgroups
                common_elements = set(N_list[0].generate())
                for N in N_list[1:]:
                    common_elements = common_elements.intersection(set(N.generate()))
                
                # Create the intersection group from the common elements
                intersection = PermutationGroup(list(common_elements))
            
            is_sub = intersection.is_subgroup(G)
            is_norm = intersection.is_normal(G)
            
            # The conclusion FAILS if the intersection is not a normal subgroup
            neg_q = not (is_sub and is_norm)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: For every i in I, N_i is a normal subgroup of G",
    "¬Q: The intersection of all N_i for i in I is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2