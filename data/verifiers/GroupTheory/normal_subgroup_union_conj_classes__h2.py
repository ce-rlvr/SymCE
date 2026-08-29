import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False]

    # H_1: G is a group (and N is a subset of G)
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            elements = set(G.elements)
            if not isinstance(N, (list, set, tuple)):
                h1 = False
            else:
                for n in N:
                    if n not in elements:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # ¬Q: N is a normal subgroup of G iff N is a union of conjugacy classes of G (must fail)
    try:
        elements = set(G.elements)
        N_set = set(N)
        
        # Check if N is a subgroup
        is_subgroup = True
        if not N_set:
            is_subgroup = False
        else:
            id_elem = list(elements)[0]**0
            if id_elem not in N_set:
                is_subgroup = False
            else:
                for a in N_set:
                    if ~a not in N_set:
                        is_subgroup = False
                        break
                    for b in N_set:
                        if a * b not in N_set:
                            is_subgroup = False
                            break
                            
        # Check if N is a normal subgroup
        is_normal_subgroup = is_subgroup
        if is_subgroup:
            for n in N_set:
                for g in elements:
                    if g * n * ~g not in N_set:
                        is_normal_subgroup = False
                        break
                if not is_normal_subgroup:
                    break
                    
        # Check if N is a union of conjugacy classes
        is_union_of_conjugacy_classes = True
        for n in N_set:
            for g in elements:
                if g * n * ~g not in N_set:
                    is_union_of_conjugacy_classes = False
                    break
            if not is_union_of_conjugacy_classes:
                break
                
        # The conjecture claims: is_normal_subgroup == is_union_of_conjugacy_classes
        # We want the negation of this claim.
        neg_q = (is_normal_subgroup != is_union_of_conjugacy_classes)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: N is a normal subgroup of G is not equivalent to N being a union of conjugacy classes of G"
]

N_HYP = 1
NEG_Q_INDEX = 1