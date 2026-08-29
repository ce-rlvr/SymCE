import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = False
        if h1_ok and isinstance(N, PermutationGroup):
            is_subgroup = True
            for g in N.generators:
                if not G.contains(g):
                    is_subgroup = False
                    break
            if is_subgroup:
                h2_ok = (G.order() % N.order() == 0)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = False
        if h1_ok and h2_ok:
            m = G.order() // N.order()
            for g in G.generate():
                g_m = g**m
                if not N.contains(g_m):
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The index of N in G is a finite integer m",
    "¬Q: There exists g in G such that g^m is not in N"
]

N_HYP = 2
NEG_Q_INDEX = 2