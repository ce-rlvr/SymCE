import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, S = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group, S is a subgroup
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(S, PermutationGroup) and all(s in G for s in S.generators)
    except Exception:
        h1 = False

    # H2: G/S is solvable
    try:
        if not h1:
            h2 = False
        else:
            is_normal = True
            for g in G.generators:
                ginv = ~g
                for s in S.generators:
                    if (g * s * ginv) not in S:
                        is_normal = False
                        break
                if not is_normal:
                    break
            
            if not is_normal:
                h2 = False
            else:
                curr = G
                while True:
                    nxt = curr.derived_subgroup()
                    if nxt.order() == curr.order():
                        res = curr
                        break
                    curr = nxt
                
                h2 = all(r in S for r in res.generators)
    except Exception:
        h2 = False

    # neg_Q: S is NOT the solvable residual of G
    try:
        if not h1:
            neg_q = False
        else:
            curr = G
            while True:
                nxt = curr.derived_subgroup()
                if nxt.order() == curr.order():
                    res = curr
                    break
                curr = nxt
            
            is_residual = (res.order() == S.order()) and all(r in S for r in res.generators)
            neg_q = not is_residual
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group and S is a subgroup of G",
    "H_2: The quotient group G/S is solvable",
    "¬Q: S is not the solvable residual of G"
]

N_HYP = 2
NEG_Q_INDEX = 2