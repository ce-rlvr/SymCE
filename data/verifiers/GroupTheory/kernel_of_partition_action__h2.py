import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
    # Unpack witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, P = witness
                X = set().union(*[set(p) for p in P])
                k = len(P)
            elif len(witness) == 3:
                G, X, P = witness
                k = len(P)
            elif len(witness) == 4:
                G, X, P, k = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = True
        elements = G.elements if hasattr(G, 'elements') else G
        X_set = set(X)
        for g in elements:
            for x in X_set:
                if g(x) not in X_set:
                    h1 = False
                    break
            if not h1:
                break
    except Exception:
        h1 = False

    # H_2: G preserves the partition P
    try:
        h2 = True
        elements = G.elements if hasattr(G, 'elements') else G
        P_sets = [set(p) for p in P]
        for g in elements:
            for p in P_sets:
                img = set(g(x) for x in p)
                if img not in P_sets:
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # ¬Q: The kernel of the induced action of G on P is NOT equal to \bigcap_{i=1}^k N_G(P_i)
    try:
        elements = G.elements if hasattr(G, 'elements') else G
        P_sets = [set(p) for p in P]
        
        # Kernel of the induced action of G on P
        ker_P = []
        for g in elements:
            if all(set(g(x) for x in p) == p for p in P_sets):
                ker_P.append(g)
                
        # Intersection of the setwise stabilizers up to k
        inter = []
        for g in elements:
            if all(set(g(x) for x in P_sets[i]) == P_sets[i] for i in range(min(k, len(P_sets)))):
                inter.append(g)
                
        q = (set(ker_P) == set(inter))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: G preserves the partition P",
    "¬Q: The kernel of the induced action of G on P is not equal to the intersection of the setwise stabilizers up to k"
]

N_HYP = 2
NEG_Q_INDEX = 2