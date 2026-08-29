import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a nilpotent group
    try:
        h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False
        
    # H_2: H times commutator of G equals G
    try:
        K = G.derived_subgroup()
        K_elems = list(K.generate())
        
        if hasattr(H, 'generate'):
            H_elems = list(H.generate())
        else:
            H_elems = list(H)
            
        products = set()
        for h in H_elems:
            for k in K_elems:
                products.add(h * k)
                
        G_elems = set(G.generate())
        h2 = bool(products == G_elems)
    except Exception:
        h2 = False
        
    # neg_Q: H != G
    try:
        if hasattr(H, 'generate'):
            H_elems = set(H.generate())
        else:
            H_elems = set(H)
            
        G_elems = set(G.generate())
        neg_q = bool(H_elems != G_elems)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: H times commutator of G equals G",
    "neg_Q: H is not G"
]

N_HYP = 2
NEG_Q_INDEX = 2