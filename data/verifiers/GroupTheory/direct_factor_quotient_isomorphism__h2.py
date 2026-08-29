import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a group and H, K are subgroups of G
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(H, PermutationGroup) and 
              isinstance(K, PermutationGroup))
        if h1:
            h1 = H.is_subgroup(G) and K.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: K is a normal subgroup of G
    try:
        h2 = bool(h1 and K.is_normal(G))
    except Exception:
        h2 = False

    # H_4: The intersection of H and K contains only the identity element
    try:
        if h1:
            h_elems = set(H.elements)
            k_elems = set(K.elements)
            int_elems = h_elems & k_elems
            h4 = (len(int_elems) == 1)
        else:
            h4 = False
    except Exception:
        h4 = False

    # H_3: G is the set product HK
    try:
        if h1 and h4:
            # For finite groups, if H \cap K = {1}, |HK| = |H| * |K|.
            # Since HK is a subset of G, HK = G iff |G| == |H| * |K|.
            h3 = (G.order() == H.order() * K.order())
        elif h1:
            h3 = (G.order() == (H.order() * K.order()) // len(int_elems))
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The quotient group G/H is not isomorphic to K
    try:
        if not h1:
            neg_q = False
        else:
            # If H is not normal, G/H is not a group, so it cannot be isomorphic to K.
            # If H is normal, the Second Isomorphism Theorem guarantees G/H is isomorphic to K
            # (since G = HK and H \cap K = {1}).
            # Thus, the conclusion fails if and only if H is not normal in G.
            neg_q = not H.is_normal(G)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group and H, K are subgroups of G",
    "H_2: K is a normal subgroup of G",
    "H_3: G is the set product HK",
    "H_4: The intersection of H and K contains only the identity element",
    "¬Q: The quotient group G/H is not isomorphic to K (or G/H is not a group)"
]

N_HYP = 4
NEG_Q_INDEX = 4