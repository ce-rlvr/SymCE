import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    """
    Checks whether the given witness is a valid counterexample.
    The witness is expected to be a tuple: (G, N, x)
    where G is a group, N is a subgroup, and x is an element.
    """
    try:
        G, N, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: Let N be a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False
        
    # H_2: Let x be an element of G having finite order k
    try:
        h2 = False
        if hasattr(G, 'contains'):
            in_G = G.contains(x)
        else:
            in_G = x in G
            
        if in_G:
            k = x.order()
            if k > 0 and k != float('inf'):
                h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: The order of the coset xN in the quotient group G/N does NOT divide k
    try:
        k = x.order()
        
        # Find the order of the coset xN in G/N.
        # This is the smallest positive integer m such that x^m is in N.
        m = 1
        curr = x
        while True:
            if hasattr(N, 'contains'):
                in_N = N.contains(curr)
            else:
                in_N = curr in N
                
            if in_N:
                break
                
            curr = curr * x
            m += 1
            
            # Safety break to prevent infinite loops in case of invalid objects
            if m > k + 1:
                break
                
        neg_q = bool(k % m != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: x is an element of G having finite order k",
    "¬Q: The order of the coset xN in the quotient group G/N does not divide k"
]

N_HYP = 2
NEG_Q_INDEX = 2