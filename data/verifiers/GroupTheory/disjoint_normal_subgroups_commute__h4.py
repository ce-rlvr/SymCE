import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, N, M = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup):
            is_sub = all(n in G for n in N.generators)
            if is_sub:
                is_norm = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2 = is_norm
    except Exception:
        h2 = False

    # H_3: M is a normal subgroup of G
    try:
        h3 = False
        if isinstance(M, PermutationGroup):
            is_sub = all(m in G for m in M.generators)
            if is_sub:
                is_norm = True
                for g in G.generators:
                    for m in M.generators:
                        if (g * m * ~g) not in M:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h3 = is_norm
    except Exception:
        h3 = False

    # ¬Q: There exists n in N and m in M such that nm != mn
    # (It is sufficient to check the generators of N and M)
    try:
        neg_q = False
        if isinstance(N, PermutationGroup) and isinstance(M, PermutationGroup):
            for n in N.generators:
                for m in M.generators:
                    if n * m != m * n:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: M is a normal subgroup of G",
    "¬Q: There exists n in N and m in M such that nm != mn"
]

N_HYP = 3
NEG_Q_INDEX = 3