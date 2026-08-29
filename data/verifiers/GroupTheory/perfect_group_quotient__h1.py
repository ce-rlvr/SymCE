import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1 = True
        for n in N.generators:
            if n not in G:
                h1 = False
                break
        
        if h1:
            for g in G.generators:
                g_inv = ~g
                for n in N.generators:
                    if (g * n * g_inv) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: G is a perfect group
    try:
        h2 = G.derived_subgroup().order() == G.order()
    except Exception:
        h2 = False

    # ¬Q: G/N is not a perfect group
    try:
        G_prime = G.derived_subgroup()
        G_prime_N = PermutationGroup(G_prime.generators + N.generators)
        neg_q = G_prime_N.order() != G.order()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: G is a perfect group",
    "¬Q: G/N is not a perfect group"
]

N_HYP = 2
NEG_Q_INDEX = 2