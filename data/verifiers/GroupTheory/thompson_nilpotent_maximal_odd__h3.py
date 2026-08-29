import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup
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
        if isinstance(witness, tuple) and len(witness) == 2:
            G, M = witness
        else:
            G = witness
            M = None
    except Exception:
        G, M = None, None

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G contains a maximal subgroup M
    try:
        h2 = False
        if h1 and isinstance(M, PermutationGroup):
            # Check if M is a subgroup of G
            is_sub = True
            for gen in M.generators:
                if gen not in G:
                    is_sub = False
                    break
            
            # Check if M is maximal in G
            if is_sub and M.order() < G.order():
                h2 = True
                for g in G.generate():
                    if g not in M:
                        # For any element g in G \ M, the group <M, g> must be G
                        H = PermutationGroup(list(M.generators) + [g])
                        if H.order() != G.order():
                            h2 = False
                            break
    except Exception:
        h2 = False

    # H_3: The order of M is an odd integer
    try:
        h3 = False
        if isinstance(M, PermutationGroup):
            h3 = (M.order() % 2 == 1)
    except Exception:
        h3 = False

    # neg_Q: G is not a solvable group
    try:
        neg_q = False
        if h1:
            neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G contains a maximal subgroup M",
    "H_3: The order of M is an odd integer",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3