import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup(Permutation(0))

def conditions(witness):
    try:
        G, M = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: M is a normal subgroup of G
    try:
        if isinstance(M, PermutationGroup):
            h2 = True
            for m in M.generators:
                if m not in G:
                    h2 = False
                    break
            if h2:
                for g in G.generators:
                    g_inv = ~g
                    for m in M.generators:
                        if (g * m * g_inv) not in M:
                            h2 = False
                            break
                    if not h2:
                        break
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: M is a solvable group
    try:
        h3 = bool(M.is_solvable)
    except Exception:
        h3 = False
        
    # neg_Q: G is not a solvable group
    try:
        neg_q = not bool(G.is_solvable)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: M is a normal subgroup of G",
    "H_3: M is a solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3