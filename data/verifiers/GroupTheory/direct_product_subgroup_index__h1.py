import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings for the witness expression
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G1, G2, H1, H2 = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = bool(H1.is_subgroup(G1))
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = bool(H2.is_subgroup(G2))
    except Exception:
        h2_ok = False
        
    try:
        def get_index(G, H):
            if hasattr(G, 'index'):
                return G.index(H)
            return G.order() // H.order()
            
        idx1 = get_index(G1, H1)
        idx2 = get_index(G2, H2)
        
        G_prod = G1 * G2
        H_prod = H1 * H2
        idx_prod = get_index(G_prod, H_prod)
        
        neg_q = bool(idx_prod != idx1 * idx2)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H_1 is a subgroup of G_1",
    "H_2: H_2 is a subgroup of G_2",
    "¬Q: The index of H1 x H2 in G1 x G2 is not equal to the product of indices"
]

N_HYP = 2
NEG_Q_INDEX = 2