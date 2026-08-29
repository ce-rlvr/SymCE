import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a subgroup of G",
    "¬Q: HK is a subgroup of G if and only if HK = KH is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: K is a subgroup of G
    try:
        h2 = isinstance(K, PermutationGroup) and K.is_subgroup(G)
    except Exception:
        h2 = False
        
    # ¬Q: HK is a subgroup of G iff HK = KH is FALSE
    try:
        if isinstance(H, PermutationGroup):
            H_elems = list(H.generate())
        else:
            H_elems = list(H)
            
        K_elems = list(K.generate())
        
        HK = set()
        for h in H_elems:
            for k in K_elems:
                HK.add(h * k)
                
        KH = set()
        for k in K_elems:
            for h in H_elems:
                KH.add(k * h)
                
        G_elems = set(G.generate())
        
        # Check if HK is a subgroup of G
        is_sub = True
        if not HK:
            is_sub = False
        else:
            # Must be a subset of G
            for x in HK:
                if x not in G_elems:
                    is_sub = False
                    break
            
            if is_sub:
                # Must be closed under multiplication
                for a in HK:
                    for b in HK:
                        if a * b not in HK:
                            is_sub = False
                            break
                    if not is_sub:
                        break
                
                if is_sub:
                    # Must be closed under inverses
                    for a in HK:
                        if ~a not in HK:
                            is_sub = False
                            break
                            
        hk_eq_kh = (HK == KH)
        
        # The conclusion is (is_sub <==> hk_eq_kh).
        # We want the negation of the conclusion, which is XOR.
        neg_q = (is_sub != hk_eq_kh)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]