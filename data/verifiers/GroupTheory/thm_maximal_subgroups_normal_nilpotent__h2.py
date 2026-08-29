import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Witness is expected to be a tuple (G, M) where G is a group and M is a subgroup.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, M = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: M is a maximal subgroup of G
    try:
        h2 = False
        if isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup):
            # Check if M is a subgroup of G
            is_sub = all(g in G for g in M.generators)
            if is_sub and M.order() < G.order():
                is_maximal = True
                g_order = G.order()
                # For M to be maximal, any element g in G \ M must generate G when added to M
                for g in G.generate_dimino():
                    if g not in M:
                        H = PermutationGroup(list(M.generators) + [g])
                        if H.order() < g_order:
                            is_maximal = False
                            break
                h2 = is_maximal
    except Exception:
        h2 = False

    # ¬Q: M is not a normal subgroup of G
    try:
        neg_q = False
        if isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup):
            is_sub = all(g in G for g in M.generators)
            if is_sub:
                is_normal = True
                # Check if g * m * g^-1 is in M for all generators g of G and m of M
                for g in G.generators:
                    for m in M.generators:
                        conj = g * m * (~g)
                        if conj not in M:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: M is a maximal subgroup of G",
    "¬Q: M is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2