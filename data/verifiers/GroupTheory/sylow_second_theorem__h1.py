import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (G, p, P, Q)
    """
    try:
        G, p, P, Q = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    # H_2: P and Q are Sylow p-subgroups of G
    try:
        def is_sylow(G, H, p):
            if p <= 1:
                return False
            if not H.is_subgroup(G):
                return False
            order_H = H.order()
            order_G = G.order()
            
            # Check if H is a p-group
            temp = order_H
            while temp % p == 0 and temp > 1:
                temp //= p
            if temp != 1:
                return False
                
            # Check if the index of H in G is coprime to p
            if (order_G // order_H) % p == 0:
                return False
                
            return True
        
        h2 = bool(is_sylow(G, P, p) and is_sylow(G, Q, p))
    except Exception:
        h2 = False
        
    # ¬Q: There does not exist g in G such that Q = g P g^-1
    try:
        def are_conjugate(G, P, Q):
            # If P and Q have different orders, they cannot be conjugate
            if P.order() != Q.order():
                return False
                
            elements = G.generate() if hasattr(G, 'generate') else G.elements
            for g in elements:
                is_conj = True
                for gen in P.generators:
                    cg = g * gen * g**-1
                    if not Q.contains(cg):
                        is_conj = False
                        break
                if is_conj:
                    return True
            return False
        
        neg_q = not are_conjugate(G, P, Q)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P and Q are Sylow p-subgroups of G",
    "¬Q: There does not exist g in G such that Q = g P g^-1"
]

N_HYP = 2
NEG_Q_INDEX = 2