import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            N = witness.get('N')
        else:
            if len(witness) != 3:
                return [False, False, False, False]
            G, H, N = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1 and h2:
            oG = G.order()
            oH = H.order()
            if oG % oH == 0:
                h3 = True
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1 and h2 and h3:
            q = False
            if isinstance(N, PermutationGroup):
                n = G.order() // H.order()
                is_normal = N.is_subgroup(G) and N.is_normal(G)
                if is_normal:
                    oN = N.order()
                    if G.order() % oN == 0:
                        index_N = G.order() // oN
                        divides = (math.factorial(n) % index_N == 0)
                        q = divides
            neg_q = not q
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: The index of H in G is a finite integer n",
    "¬Q: N is not a normal subgroup of G or the index of N in G does not divide n!"
]

N_HYP = 3
NEG_Q_INDEX = 3