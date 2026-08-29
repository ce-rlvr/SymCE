import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def pointwise_stabilizer(G, S):
    stab = set()
    try:
        elements = list(G.elements)
    except Exception:
        elements = list(G.generate())
        
    for g in elements:
        fixes_all = True
        for s in S:
            if isinstance(s, int) and s >= 0:
                if s < g.size:
                    if g(s) != s:
                        fixes_all = False
                        break
                else:
                    # Permutations act trivially on points >= g.size
                    pass
            else:
                fixes_all = False
                break
        if fixes_all:
            stab.add(g)
    return stab

def conditions(witness):
    try:
        if len(witness) == 4:
            G, X, A, B = witness
        elif len(witness) == 3:
            G, A, B = witness
            if isinstance(G, PermutationGroup):
                X = set(range(G.degree))
            else:
                X = set()
        else:
            return [False, False, False]
            
        A = set(A)
        B = set(B)
        X = set(X)
    except Exception:
        return [False, False, False]

    # H_1: G is a group acting on a set X
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(X, set)
        if h1:
            for x in X:
                if not isinstance(x, int) or x < 0:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: A and B are subsets of X
    try:
        h2 = A.issubset(X) and B.issubset(X)
    except Exception:
        h2 = False

    # ¬Q: The pointwise stabilizer G_{(A \cup B)} is not equal to G_{(A)} \cap G_{(B)}
    try:
        stab_A = pointwise_stabilizer(G, A)
        stab_B = pointwise_stabilizer(G, B)
        stab_A_cup_B = pointwise_stabilizer(G, A.union(B))
        
        q = (stab_A_cup_B == stab_A.intersection(stab_B))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: A and B are subsets of X",
    "¬Q: The pointwise stabilizer G_{(A \\cup B)} is not equal to G_{(A)} \\cap G_{(B)}"
]

N_HYP = 2
NEG_Q_INDEX = 2