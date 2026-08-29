import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
        if isinstance(N, list):
            N = PermutationGroup(N)
    except Exception:
        return [False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1 = True
        for n in N.generators:
            if not G.contains(n):
                h1 = False
                break
        if h1:
            gens = list(G.generators)
            gens += [~g for g in gens]
            for g in gens:
                for n in N.generators:
                    if not N.contains(g * n * ~g):
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: The order of N is a prime number p
    try:
        h2 = bool(isprime(N.order()))
    except Exception:
        h2 = False

    # neg_Q: N is not contained in the center of G
    try:
        neg_q = False
        for n in N.generators:
            for g in G.generators:
                if n * g != g * n:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The order of N is a prime number p",
    "¬Q: N is not contained in the center of G"
]

N_HYP = 2
NEG_Q_INDEX = 2