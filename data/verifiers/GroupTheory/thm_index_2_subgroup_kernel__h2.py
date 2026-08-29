import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H_2: The index of H in G is exactly 2
    try:
        if isinstance(H, PermutationGroup):
            size_H = H.order()
            is_subset = H.is_subgroup(G)
        else:
            H_set = set(H)
            size_H = len(H_set)
            is_subset = all(h in G for h in H_set)
            
        size_G = G.order()
        h2_ok = bool(is_subset and size_G == 2 * size_H)
    except Exception:
        h2_ok = False
        
    # neg_Q: There does NOT exist a surjective group homomorphism from G to Z_2 with kernel H
    # A subset H of index 2 is the kernel of such a homomorphism if and only if it is a subgroup.
    try:
        if isinstance(H, PermutationGroup):
            is_subgroup = True
        else:
            H_set = set(H)
            identity = None
            for h in H_set:
                if h * h == h:
                    identity = h
                    break
            if identity is None:
                is_subgroup = False
            else:
                is_subgroup = True
                for a in H_set:
                    for b in H_set:
                        if (a * b) not in H_set:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
        neg_q_ok = not is_subgroup
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The index of H in G is exactly 2",
    "¬Q: There does not exist a surjective group homomorphism from G to the cyclic group of order 2 with kernel H"
]

N_HYP = 2
NEG_Q_INDEX = 2