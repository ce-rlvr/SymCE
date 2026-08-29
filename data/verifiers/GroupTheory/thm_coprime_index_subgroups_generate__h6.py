import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def get_order(grp):
    try:
        o = grp.order()
    except TypeError:
        o = grp.order
    return int(o)

def check_subgroup(sub, supergroup):
    if not isinstance(sub, PermutationGroup):
        return False
    if not isinstance(supergroup, PermutationGroup):
        return False
    for g in sub.generators:
        if g not in supergroup:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False] * 6

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = check_subgroup(H, G)
    except Exception:
        h2 = False

    # H_3: K is a subgroup of G
    try:
        h3 = check_subgroup(K, G)
    except Exception:
        h3 = False

    # H_4: The index of H in G is finite
    try:
        h4 = h1 and h2 and (get_order(G) % get_order(H) == 0)
    except Exception:
        h4 = False

    # H_5: The index of K in G is finite
    try:
        h5 = h1 and h3 and (get_order(G) % get_order(K) == 0)
    except Exception:
        h5 = False

    # ¬Q: G != HK
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            try:
                H_elems = list(H.elements)
            except Exception:
                H_elems = list(H.generate())
            try:
                K_elems = list(K.elements)
            except Exception:
                K_elems = list(K.generate())
                
            HK_set = set(h * k for h in H_elems for k in K_elems)
            neg_q = len(HK_set) < get_order(G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "H_4: The index of H in G is finite",
    "H_5: The index of K in G is finite",
    "¬Q: G != HK"
]

N_HYP = 5
NEG_Q_INDEX = 5