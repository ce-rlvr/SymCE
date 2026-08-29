import math
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_id(g, G=None):
    if G is not None and hasattr(G, 'identity'):
        return g == G.identity
    if hasattr(g, 'is_Identity'):
        return g.is_Identity
    try:
        return g == g**0
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 3:
            n, G, generators = witness
        elif len(witness) == 2:
            n, generators = witness
            G = PermutationGroup(*generators)
        else:
            return [False] * 4 + [False]
    except Exception:
        return [False] * 4 + [False]

    # H1: Let n >= 2 be an integer.
    try:
        h1 = int(n) == n and n >= 2 and len(generators) == n - 1
        if h1:
            n = int(n)
            try:
                H = PermutationGroup(*generators)
                if hasattr(G, 'order') and G.order() != H.order():
                    h1 = False
            except Exception:
                pass
    except Exception:
        h1 = False

    # H2: s_i^2 = 1 for all 1 <= i <= n-1
    try:
        h2 = True
        for g in generators:
            if not is_id(g**2, G):
                h2 = False
                break
    except Exception:
        h2 = False

    # H3: (s_i s_{i+1})^3 = 1 for all 1 <= i <= n-2
    try:
        h3 = True
        for i in range(n - 2):
            prod = generators[i] * generators[i+1]
            if not is_id(prod**3, G):
                h3 = False
                break
    except Exception:
        h3 = False

    # H4: (s_i s_j)^2 = 1 for all i, j such that |i - j| >= 2
    try:
        h4 = True
        for i in range(n - 1):
            for j in range(n - 1):
                if abs(i - j) >= 2:
                    prod = generators[i] * generators[j]
                    if not is_id(prod**2, G):
                        h4 = False
                        break
    except Exception:
        h4 = False

    # neg_Q: G is NOT isomorphic to S_n
    try:
        if hasattr(G, 'order') and G.order() != math.factorial(n):
            neg_q = True
        elif hasattr(G, 'is_isomorphic'):
            neg_q = not G.is_isomorphic(SymmetricGroup(n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: s_i^2 = 1 for all 1 <= i <= n-1",
    "H_3: (s_i s_{i+1})^3 = 1 for all 1 <= i <= n-2",
    "H_4: (s_i s_j)^2 = 1 for all |i - j| >= 2",
    "¬Q: G is not isomorphic to S_n"
]

N_HYP = 4
NEG_Q_INDEX = 4