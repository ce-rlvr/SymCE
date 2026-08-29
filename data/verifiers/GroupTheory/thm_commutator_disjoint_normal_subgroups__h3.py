import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False, False]
        G, H, K = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: H is a normal subgroup of G
    try:
        h2 = False
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = True
            for h in H.generators:
                if not G.contains(h):
                    is_sub = False
                    break
            
            if is_sub:
                is_norm = True
                for g in G.generators:
                    g_inv = g**-1
                    for h in H.generators:
                        if not H.contains(g_inv * h * g):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2 = is_norm
    except Exception:
        h2 = False

    # H3: K is a normal subgroup of G
    try:
        h3 = False
        if isinstance(K, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = True
            for k in K.generators:
                if not G.contains(k):
                    is_sub = False
                    break
            
            if is_sub:
                is_norm = True
                for g in G.generators:
                    g_inv = g**-1
                    for k in K.generators:
                        if not K.contains(g_inv * k * g):
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h3 = is_norm
    except Exception:
        h3 = False

    # NegQ: The mutual commutator subgroup of H and K is not the trivial subgroup
    try:
        neg_q = False
        if isinstance(H, PermutationGroup) and isinstance(K, PermutationGroup):
            gens_commute = True
            for h in H.generators:
                for k in K.generators:
                    if (h * k) != (k * h):
                        gens_commute = False
                        break
                if not gens_commute:
                    break
            neg_q = not gens_commute
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a normal subgroup of G",
    "H_3: K is a normal subgroup of G",
    "¬Q: The mutual commutator subgroup of H and K is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3