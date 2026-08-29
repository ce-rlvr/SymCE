import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    # H1: The action of G on X is transitive.
    try:
        G, X, B = witness
        X_set = set(X)
        if not X_set:
            h1 = False
        else:
            elements = list(G.generate()) if hasattr(G, 'generate') else list(G)
            invariant = True
            for g in elements:
                for x in X_set:
                    if g(x) not in X_set:
                        invariant = False
                        break
                if not invariant:
                    break
            if not invariant:
                h1 = False
            else:
                x0 = next(iter(X_set))
                orbit = {g(x0) for g in elements}
                h1 = (orbit == X_set)
    except Exception:
        h1 = False

    # H2: B is a non-empty block of imprimitivity in X
    try:
        G, X, B = witness
        B_set = set(B)
        if not B_set:
            h2 = False
        else:
            elements = list(G.generate()) if hasattr(G, 'generate') else list(G)
            h2 = True
            for g in elements:
                gB = {g(b) for b in B_set}
                if gB != B_set and not gB.isdisjoint(B_set):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: The set of distinct translates {g * B | g in G} does NOT form a partition of X.
    try:
        G, X, B = witness
        X_set = set(X)
        B_set = set(B)
        elements = list(G.generate()) if hasattr(G, 'generate') else list(G)
        
        translates = set()
        for g in elements:
            gB = frozenset(g(b) for b in B_set)
            translates.add(gB)
            
        if frozenset() in translates:
            is_partition = False
        else:
            union_translates = set()
            for t in translates:
                union_translates.update(t)
                
            is_partition = True
            if union_translates != X_set:
                is_partition = False
            else:
                t_list = list(translates)
                for i in range(len(t_list)):
                    for j in range(i + 1, len(t_list)):
                        if not t_list[i].isdisjoint(t_list[j]):
                            is_partition = False
                            break
                    if not is_partition:
                        break
        
        neg_q = not is_partition
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The action of G on X is transitive",
    "H_2: B is a non-empty block of imprimitivity in X",
    "¬Q: The set of distinct translates of B does not form a partition of X"
]

N_HYP = 2
NEG_Q_INDEX = 2