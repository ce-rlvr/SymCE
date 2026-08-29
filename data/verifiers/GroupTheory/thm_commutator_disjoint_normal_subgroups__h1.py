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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(H, G):
    try:
        return all(h in G for h in H.generators)
    except Exception:
        return False

def is_normal_subgroup(G, H):
    if not is_subgroup(H, G):
        return False
    try:
        for g in G.generators:
            try:
                g_inv = ~g
            except TypeError:
                g_inv = g**-1
                
            for h in H.generators:
                if (g * h * g_inv) not in H:
                    return False
                if (g_inv * h * g) not in H:
                    return False
        return True
    except Exception:
        return False

def intersection_is_trivial(H, K):
    try:
        if hasattr(H, 'intersection'):
            return H.intersection(K).order() == 1
    except Exception:
        pass
    
    try:
        if H.order() < K.order():
            smaller, larger = H, K
        else:
            smaller, larger = K, H
        
        try:
            gen = smaller.generate()
        except AttributeError:
            gen = smaller.elements
            
        common_count = 0
        for g in gen:
            if g in larger:
                common_count += 1
                if common_count > 1:
                    return False
        return common_count == 1
    except Exception:
        return False

def commutator_is_nontrivial(H, K):
    try:
        for h in H.generators:
            for k in K.generators:
                if h * k != k * h:
                    return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1_ok = bool(is_normal_subgroup(G, H) and is_normal_subgroup(G, K))
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = bool(intersection_is_trivial(H, K))
    except Exception:
        h2_ok = False
        
    try:
        neg_q_ok = bool(commutator_is_nontrivial(H, K))
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: H and K are normal subgroups of G", "H_2: The intersection of H and K is the trivial subgroup", "¬Q: The mutual commutator subgroup is not the trivial subgroup"]

N_HYP = 2
NEG_Q_INDEX = 2