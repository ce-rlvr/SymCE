import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup

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

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = False
        if hasattr(N, 'is_normal'):
            h1 = bool(N.is_normal(G))
        else:
            if hasattr(N, 'is_subgroup') and N.is_subgroup(G):
                is_normal = True
                for g in G.generators:
                    g_inv = ~g
                    for n in N.generators:
                        if (g * n * g_inv) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h1 = is_normal
    except Exception:
        h1 = False

    try:
        h2 = bool(H.is_subgroup(G))
    except Exception:
        h2 = False

    try:
        h3 = math.gcd(H.order(), G.order() // N.order()) == 1
    except Exception:
        h3 = False

    try:
        if hasattr(H, 'is_subgroup'):
            neg_q = not H.is_subgroup(N)
        else:
            subset = True
            for h in H.generators:
                if h not in N:
                    subset = False
                    break
            neg_q = not subset
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: H is a subgroup of G",
    "H_3: gcd(|H|, G:N) = 1",
    "not Q: H is not a subset of N"
]

N_HYP = 3
NEG_Q_INDEX = 3