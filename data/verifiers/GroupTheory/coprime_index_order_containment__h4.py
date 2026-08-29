import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup

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
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G)
        if h2:
            # Check normality: g * n * g^-1 in N for all generators n of N and g of G
            for n in N.generators:
                for g in G.generators:
                    if (g * n * ~g) not in N:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h3 = False

    # ¬Q: H is not a subgroup of N
    try:
        neg_q = isinstance(H, PermutationGroup) and isinstance(N, PermutationGroup) and not H.is_subgroup(N)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "¬Q: H is not a subgroup of N"
]

N_HYP = 3
NEG_Q_INDEX = 3