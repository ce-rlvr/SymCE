import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: K is a subgroup of G",
    "¬Q: The number of orbits of H on G/K is not equal to the number of double cosets H \\ G / K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        h2 = isinstance(H, PermutationGroup) and all(G.contains(g) for g in H.generators)
    except Exception:
        h2 = False
        
    # H_3: K is a subgroup of G
    try:
        h3 = isinstance(K, PermutationGroup) and all(G.contains(g) for g in K.generators)
    except Exception:
        h3 = False
        
    # ¬Q: The bijection fails (number of orbits != number of double cosets)
    try:
        left_cosets = []
        for g in G.elements:
            c = frozenset([g * k for k in K.elements])
            if c not in left_cosets:
                left_cosets.append(c)
                
        orbits = set()
        for c in left_cosets:
            orbit = frozenset([frozenset([h * x for x in c]) for h in H.elements])
            orbits.add(orbit)
            
        double_cosets = set()
        for g in G.elements:
            dc = frozenset([h * g * k for h in H.elements for k in K.elements])
            double_cosets.add(dc)
            
        neg_q = len(orbits) != len(double_cosets)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]