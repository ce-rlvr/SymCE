import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        if not isinstance(N, PermutationGroup):
            h2 = False
        elif not N.is_subgroup(G):
            h2 = False
        else:
            is_N_normal = True
            for g in G.generators:
                for n in N.generators:
                    if (g * n * ~g) not in N:
                        is_N_normal = False
                        break
                if not is_N_normal:
                    break
            h2 = is_N_normal
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G such that G is the internal semidirect product of N and H
    try:
        if not isinstance(H, PermutationGroup):
            h3 = False
        elif not H.is_subgroup(G):
            h3 = False
        else:
            # Check if N intersect H is trivial
            intersection_size = sum(1 for h in H.elements if h in N)
            # For internal semidirect product, we need N intersect H = {e} and |N| * |H| = |G|
            if intersection_size == 1 and N.order() * H.order() == G.order():
                h3 = True
            else:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: H is NOT a normal subgroup of G, OR G is NOT the internal direct product of N and H
    # Given H_3, G is the internal direct product iff H is a normal subgroup of G.
    # Thus, the conclusion fails iff H is NOT a normal subgroup of G.
    try:
        if not isinstance(H, PermutationGroup) or not H.is_subgroup(G):
            neg_q = True
        else:
            is_H_normal = True
            for g in G.generators:
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        is_H_normal = False
                        break
                if not is_H_normal:
                    break
            neg_q = not is_H_normal
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G such that G is the internal semidirect product of N and H",
    "¬Q: H is not a normal subgroup of G (or G is not the internal direct product of N and H)"
]

N_HYP = 3
NEG_Q_INDEX = 3