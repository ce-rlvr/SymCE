import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def get_order(group):
    val = group.order
    if callable(val):
        return val()
    return val

def get_elements(group):
    try:
        return list(group.generate_dimino())
    except Exception:
        return list(group.elements)

def check_solvable(group):
    val = group.is_solvable
    if callable(val):
        return val()
    return val

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: H and K are subgroups of G
    try:
        h1 = bool(H.is_subgroup(G) and K.is_subgroup(G))
    except Exception:
        h1 = False
        
    # H2: G is the internal direct product of H and K
    try:
        if not (H.is_normal(G) and K.is_normal(G)):
            h2 = False
        elif get_order(H) * get_order(K) != get_order(G):
            h2 = False
        else:
            try:
                int_K = H.intersect(K)
                intersection_trivial = (get_order(int_K) == 1)
            except Exception:
                intersection_trivial = True
                for g in get_elements(H):
                    if not g.is_Identity and K.contains(g):
                        intersection_trivial = False
                        break
            h2 = bool(intersection_trivial)
    except Exception:
        h2 = False
        
    # H3: H is a solvable group
    try:
        h3 = bool(check_solvable(H))
    except Exception:
        h3 = False
        
    # neg_Q: H is NOT the trivial subgroup OR K is NOT equal to G
    try:
        neg_q = not (get_order(H) == 1 and get_order(K) == get_order(G))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: H and K are subgroups of G",
    "H_2: G is the internal direct product of H and K",
    "H_3: H is a solvable group",
    "¬Q: H is not the trivial subgroup or K is not equal to G"
]

N_HYP = 3
NEG_Q_INDEX = 3