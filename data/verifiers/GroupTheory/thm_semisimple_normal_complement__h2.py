import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def intersection_trivial(N, K):
    try:
        if math.gcd(N.order(), K.order()) == 1:
            return True
        if N.order() == K.order() and N.order() > 1:
            if N == K:
                return False
        
        if N.order() > K.order():
            N, K = K, N
            
        for g in N.generate():
            if g.is_Identity:
                continue
            if g in K:
                return False
        return True
    except Exception:
        return False

def is_semisimple(G):
    """
    A finite group is semisimple if it is a direct product of non-abelian simple groups.
    Equivalently:
    1. It has no non-trivial abelian normal subgroups.
    2. Every normal subgroup has a normal complement.
    """
    try:
        if getattr(G, 'order', lambda: 0)() == 0:
            return False
        if G.order() == 1:
            return True
        
        normals = G.normal_subgroups()
        
        # Condition 1: No non-trivial abelian normal subgroups
        for H in normals:
            if H.order() > 1 and H.is_abelian:
                return False
                
        # Condition 2: Every normal subgroup has a normal complement
        for H in normals:
            has_complement = False
            for K in normals:
                if H.order() * K.order() == G.order():
                    if intersection_trivial(H, K):
                        has_complement = True
                        break
            if not has_complement:
                return False
                
        return True
    except Exception:
        return False

def is_normal(G, H):
    try:
        for h in H.generators:
            if h not in G:
                return False
        for g in G.generators:
            for h in H.generators:
                if (g * h * g**-1) not in H:
                    return False
        return True
    except Exception:
        return False

def conclusion_holds(G, N):
    try:
        # For G to be the internal direct product of N and K, N must be normal in G.
        if not is_normal(G, N):
            return False
            
        for K in G.normal_subgroups():
            if N.order() * K.order() == G.order():
                if intersection_trivial(N, K):
                    return True
        return False
    except Exception:
        return False

def conditions(witness):
    """
    witness: A tuple (G, N) where G is a finite semisimple group and N is a subgroup.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False
        
    try:
        neg_q = not conclusion_holds(G, N)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite semisimple group",
    "¬Q: There does not exist a normal subgroup K of G such that G is the internal direct product of N and K"
]

N_HYP = 1
NEG_Q_INDEX = 1