import sympy
from sympy.combinatorics import PermutationGroup
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
        G, H, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is a subgroup of G
    try:
        if not isinstance(H, PermutationGroup):
            h2 = False
        else:
            h2 = True
            for h in H.generators:
                if h not in G:
                    h2 = False
                    break
    except Exception:
        h2 = False
        
    # H_3: N is a normal subgroup of G
    try:
        if not isinstance(N, PermutationGroup):
            h3 = False
        else:
            h3 = True
            for n in N.generators:
                if n not in G:
                    h3 = False
                    break
            if h3:
                for g in G.generators:
                    for n in N.generators:
                        if g * n * ~g not in N:
                            h3 = False
                            break
                        if ~g * n * g not in N:
                            h3 = False
                            break
                    if not h3:
                        break
    except Exception:
        h3 = False
        
    # neg_Q: The index of N in HN does NOT divide the order of H
    try:
        H_elems = list(H.generate())
        N_elems = list(N.generate())
            
        HN_elems = set()
        for h in H_elems:
            for n in N_elems:
                HN_elems.add(h * n)
        
        order_HN = len(HN_elems)
        order_N = len(N_elems)
        order_H = len(H_elems)
        
        if order_N == 0:
            neg_q = False
        else:
            index = order_HN // order_N
            if index == 0:
                neg_q = False
            else:
                divides = (order_H % index == 0)
                neg_q = not divides
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: N is a normal subgroup of G",
    "¬Q: The index of N in HN does not divide the order of H"
]

N_HYP = 3
NEG_Q_INDEX = 3