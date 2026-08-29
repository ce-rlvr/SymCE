import sympy
from sympy.combinatorics import PermutationGroup
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

def is_subgroup(sub, supergroup):
    try:
        if not isinstance(sub, PermutationGroup) or not isinstance(supergroup, PermutationGroup):
            return False
        for gen in sub.generators:
            if gen not in supergroup:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if is_subgroup(N, G):
            h2 = True
            for g in G.generators:
                g_inv = ~g
                for n in N.generators:
                    if (g * n * g_inv) not in N:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = is_subgroup(H, G)
    except Exception:
        h3 = False

    # neg_Q: H is not a subgroup of N
    try:
        if not isinstance(H, PermutationGroup) or not isinstance(N, PermutationGroup):
            neg_q = True
        else:
            neg_q = not is_subgroup(H, N)
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "¬Q: H is not a subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3