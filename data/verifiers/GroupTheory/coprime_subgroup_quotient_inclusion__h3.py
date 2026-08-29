import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings for witness expressions
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

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and int(G.order()) > 0
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h2 = False
        
    # H_3: gcd(|H|, index of N in G) = 1
    try:
        if hasattr(H, 'order'):
            order_H = int(H.order())
        else:
            order_H = int(len(H))
            
        index_N = int(G.order()) // int(N.order())
        h3 = bool(math.gcd(order_H, index_N) == 1)
    except Exception:
        h3 = False
        
    # ¬Q: H is not a subset of N
    try:
        if hasattr(H, 'generators'):
            elements_to_check = H.generators
        else:
            elements_to_check = H
            
        is_subset = all(N.contains(g) for g in elements_to_check)
        neg_q = not is_subset
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: gcd(order(H), index(N)) = 1",
    "not Q: H is not a subset of N"
]

N_HYP = 3
NEG_Q_INDEX = 3