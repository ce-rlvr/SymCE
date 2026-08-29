import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, A, B = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: A is a subset of G
    try:
        h2 = isinstance(A, (set, list, tuple)) and all(a in G for a in A)
    except Exception:
        h2 = False
        
    # H_3: B is a subset of G
    try:
        h3 = isinstance(B, (set, list, tuple)) and all(b in G for b in B)
    except Exception:
        h3 = False
        
    # ¬Q: AB is not a union of conjugacy classes of G
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            AB = set()
            for a in A:
                for b in B:
                    AB.add(a * b)
            
            is_union = True
            for x in AB:
                for g in G.generators:
                    if g * x * ~g not in AB:
                        is_union = False
                        break
                    if ~g * x * g not in AB:
                        is_union = False
                        break
                if not is_union:
                    break
            neg_q = not is_union
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: A is a subset of G",
    "H_3: B is a subset of G",
    "¬Q: AB is not a union of conjugacy classes of G"
]

N_HYP = 3
NEG_Q_INDEX = 3