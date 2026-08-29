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

def conditions(witness):
    try:
        n, G, sigma, tau = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    # H_2: sigma and tau are permutations in G
    try:
        h2 = (isinstance(G, PermutationGroup) and 
              isinstance(sigma, Permutation) and 
              isinstance(tau, Permutation) and 
              (sigma in G) and 
              (tau in G))
    except Exception:
        h2 = False
        
    # neg_Q: sigma and tau are conjugate in G iff they have the same cycle type (fails)
    try:
        conjugate_in_G = False
        for g in G.elements:
            if g * sigma * (~g) == tau:
                conjugate_in_G = True
                break
                
        def get_full_cycle_structure(p, degree):
            struct = p.cycle_structure.copy()
            elements_in_cycles = sum(k * v for k, v in struct.items())
            ones = degree - elements_in_cycles
            if ones > 0:
                struct[1] = struct.get(1, 0) + ones
            return {k: v for k, v in struct.items() if v > 0}
            
        degree = max(int(n), getattr(G, 'degree', 0), sigma.size, tau.size)
        struct_sigma = get_full_cycle_structure(sigma, degree)
        struct_tau = get_full_cycle_structure(tau, degree)
        
        same_cycle_type = (struct_sigma == struct_tau)
        
        neg_q = (conjugate_in_G != same_cycle_type)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: sigma and tau are permutations in G",
    "¬Q: sigma and tau are conjugate in G iff they have the same cycle type (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2