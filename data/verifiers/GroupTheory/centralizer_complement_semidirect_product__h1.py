import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_subgroup(sub, grp):
    try:
        return all(g in grp for g in sub.generators)
    except Exception:
        return False

def is_normal(sub, grp):
    try:
        if not is_subgroup(sub, grp):
            return False
        for g in grp.generators:
            g_inv = ~g
            for h in sub.generators:
                if g * h * g_inv not in sub:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 3):
            return [False] * 5 + [False]
        G, N, H = witness
    except Exception:
        return [False] * 5 + [False]

    # H1: G, N, H are PermutationGroups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = h1 and is_normal(N, G)
    except Exception:
        h2 = False

    # H3: H is a subgroup of G
    try:
        h3 = h1 and is_subgroup(H, G)
    except Exception:
        h3 = False

    # H4: N and H intersect trivially
    try:
        if h1:
            common = set(N.generate()).intersection(set(H.generate()))
            h4 = len(common) == 1
        else:
            h4 = False
    except Exception:
        h4 = False

    # H5: G is the semidirect product of N and H (|G| = |N| * |H|)
    try:
        if h1:
            h5 = G.order() == N.order() * H.order()
        else:
            h5 = False
    except Exception:
        h5 = False

    # neg_Q: C_G(H) is not equal to the internal direct product C_N(H) x Z(H)
    try:
        if h1:
            def is_centralizer_elem(g, grp_H):
                return all(g * h == h * g for h in grp_H.generators)
                
            CG_H_elems = [g for g in G.generate() if is_centralizer_elem(g, H)]
            CN_H_elems = [n for n in N.generate() if is_centralizer_elem(n, H)]
            ZH_elems = [h for h in H.generate() if is_centralizer_elem(h, H)]
            
            # Since C_N(H) and Z(H) always intersect trivially and commute,
            # their internal direct product has order |C_N(H)| * |Z(H)|.
            # C_G(H) equals this product iff their orders match.
            neg_q = len(CG_H_elems) != len(CN_H_elems) * len(ZH_elems)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G, N, H are PermutationGroups",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: N and H intersect trivially",
    "H_5: G is the semidirect product of N and H (|G| = |N| * |H|)",
    "¬Q: C_G(H) is not equal to the internal direct product C_N(H) x Z(H)"
]

N_HYP = 5
NEG_Q_INDEX = 5