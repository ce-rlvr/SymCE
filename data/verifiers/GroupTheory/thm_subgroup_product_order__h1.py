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

def conditions(witness):
    try:
        if len(witness) == 3:
            G, H, K = witness
        elif len(witness) == 2:
            H, K = witness
            G = H
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: H is a finite subgroup of G
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = H.is_subgroup(G) and H.order() < float('inf')
        else:
            H_group = PermutationGroup(*list(H))
            h1 = H_group.is_subgroup(G) and H_group.order() == len(set(H))
            H = H_group
    except Exception:
        h1 = False

    # H2: K is a finite subgroup of G
    try:
        if hasattr(K, 'is_subgroup'):
            h2 = K.is_subgroup(G) and K.order() < float('inf')
        else:
            K_group = PermutationGroup(*list(K))
            h2 = K_group.is_subgroup(G) and K_group.order() == len(set(K))
            K = K_group
    except Exception:
        h2 = False

    # neg_Q: The cardinality of the set HK is NOT equal to (|H| * |K|) / |H \cap K|
    try:
        if hasattr(H, 'generate'):
            H_elements = set(H.generate())
        else:
            H_elements = set(H)
            
        if hasattr(K, 'generate'):
            K_elements = set(K.generate())
        else:
            K_elements = set(K)
            
        HK = set()
        for h in H_elements:
            for k in K_elements:
                HK.add(h * k)
                
        H_cap_K = H_elements.intersection(K_elements)
        
        if len(H_cap_K) == 0:
            neg_q = True
        else:
            expected = (len(H_elements) * len(K_elements)) // len(H_cap_K)
            neg_q = len(HK) != expected
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a finite subgroup of G",
    "H_2: K is a finite subgroup of G",
    "¬Q: The cardinality of HK is not equal to (|H| * |K|) / |H \\cap K|"
]

N_HYP = 2
NEG_Q_INDEX = 2