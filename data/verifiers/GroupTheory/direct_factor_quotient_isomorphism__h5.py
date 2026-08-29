import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_order(grp):
    ord_val = grp.order
    return ord_val() if callable(ord_val) else ord_val

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = H.is_subgroup(G) and H.is_normal(G)
    except Exception:
        h2 = False

    try:
        h3 = K.is_subgroup(G) and K.is_normal(G)
    except Exception:
        h3 = False

    try:
        h4 = False
        if H.is_subgroup(G) and K.is_subgroup(G):
            h_els = set(H.generate())
            k_els = set(K.generate())
            int_order = len(h_els.intersection(k_els))
            h4 = (get_order(H) * get_order(K) // int_order) == get_order(G)
    except Exception:
        h4 = False

    try:
        # G/H is isomorphic to K iff |G|/|H| == |K| (given G=HK).
        # By the Second Isomorphism Theorem, since G=HK, G/H = HK/H is isomorphic to K/(H \cap K).
        # Thus, G/H is isomorphic to K iff |H \cap K| = 1, which is equivalent to |G| = |H| * |K|.
        # Therefore, the conclusion fails (G/H is NOT isomorphic to K) iff |G| != |H| * |K|.
        neg_q = get_order(G) != get_order(H) * get_order(K)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a normal subgroup of G",
    "H_3: K is a normal subgroup of G",
    "H_4: G is the set product HK",
    "¬Q: G/H is not isomorphic to K"
]

N_HYP = 4
NEG_Q_INDEX = 4