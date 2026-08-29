import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False]
        
    # H1: G is a finite group
    try:
        h1_ok = hasattr(G, 'order') and hasattr(G, 'generate')
        if h1_ok:
            order = G.order()
            h1_ok = order < float('inf') and order > 0
    except Exception:
        h1_ok = False

    # neg_Q: The number of distinct conjugate subgroups of H in G is NOT equal to [G : N_G(H)]
    try:
        if hasattr(H, 'generate'):
            H_set = frozenset(H.generate())
        else:
            H_set = frozenset(H)
            
        G_elements = list(G.generate())
        
        try:
            identity = G.identity
        except Exception:
            identity = G_elements[0]**0
            
        # Compute N_G(H)
        N_G_H_size = 0
        conjugates = set()
        
        for g in G_elements:
            g_inv = ~g
            # conjugate subset g * H * g^-1
            conj = frozenset(g * h * g_inv for h in H_set)
            conjugates.add(conj)
            if conj == H_set:
                N_G_H_size += 1
                
        index = len(G_elements) // N_G_H_size
        
        # Count how many conjugates are subgroups
        num_conjugate_subgroups = 0
        for conj in conjugates:
            if not conj:
                continue
            if identity not in conj:
                continue
                
            is_closed = True
            for a in conj:
                for b in conj:
                    if a * b not in conj:
                        is_closed = False
                        break
                if not is_closed:
                    break
            if is_closed:
                num_conjugate_subgroups += 1
                
        neg_q_ok = (num_conjugate_subgroups != index)
        
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = ["H_1: G is a finite group", "neg_Q: The number of distinct conjugate subgroups of H in G is not equal to the index of N_G(H) in G"]

N_HYP = 1
NEG_Q_INDEX = 1