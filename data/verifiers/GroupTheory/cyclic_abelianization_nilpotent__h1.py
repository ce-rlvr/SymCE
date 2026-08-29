import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G = witness
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            G_prime = G.derived_subgroup()
            target_order = G.order()
            h1 = False
            for g in G.elements:
                gens = list(G_prime.generators) + [g]
                H = PermutationGroup(gens)
                if H.order() == target_order:
                    h1 = True
                    break
    except Exception:
        h1 = False

    try:
        G = witness
        if not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            is_cyclic = False
            g_order = G.order()
            for g in G.elements:
                if g.order() == g_order:
                    is_cyclic = True
                    break
            neg_q = not is_cyclic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The quotient group G/G' is a cyclic group",
    "¬Q: G is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1