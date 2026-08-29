import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference
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

def conditions(witness) -> list[bool]:
    try:
        G, p, Q = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False
        
    # ¬Q: The number of Sylow p-subgroups of G that contain Q is not congruent to 1 (mod p)
    try:
        try:
            P = G.sylow_subgroup(p)
        except Exception:
            try:
                order = G.order()
            except TypeError:
                order = G.order
                
            if order % p != 0:
                if G.generators:
                    id_elem = G.generators[0]**0
                else:
                    id_elem = Permutation()
                P = PermutationGroup([id_elem])
            else:
                raise
                
        if hasattr(P, 'elements'):
            P_elements = set(P.elements)
        else:
            P_elements = set(P.generate())
            
        sylow_sets = set()
        
        if hasattr(G, 'elements'):
            G_elements = G.elements
        else:
            G_elements = list(G.generate())
            
        for g in G_elements:
            conj_set = frozenset(g * x * ~g for x in P_elements)
            sylow_sets.add(conj_set)
            
        count = 0
        try:
            if hasattr(Q, 'elements'):
                Q_elements = set(Q.elements)
            elif hasattr(Q, 'generate'):
                Q_elements = set(Q.generate())
            else:
                Q_elements = set(Q)
        except Exception:
            Q_elements = set(Q)
            
        for S in sylow_sets:
            if Q_elements.issubset(S):
                count += 1
                
        neg_q = (count % p) != 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: The number of Sylow p-subgroups of G that contain Q is not congruent to 1 (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2