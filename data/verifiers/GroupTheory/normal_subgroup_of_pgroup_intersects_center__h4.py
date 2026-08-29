import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
from sympy import abc
from sympy import polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        p, G, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H_2: G is a finite p-group
    try:
        order = G.order()
        if order == 1:
            h2 = True
        else:
            factors = sympy.ntheory.factorint(order)
            h2 = (list(factors.keys()) == [p])
    except Exception:
        h2 = False
        
    # H_3: N is a normal subgroup of G
    try:
        h3 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h3 = False
        
    # ¬Q: The intersection of N and the center Z(G) is the trivial subgroup
    try:
        Z_elems = set(G.center().elements)
        N_elems = set(N.elements)
        # The intersection is trivial if it contains exactly 1 element (the identity)
        neg_q = (len(Z_elems.intersection(N_elems)) == 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is a finite p-group",
    "H_3: N is a normal subgroup of G",
    "¬Q: The intersection of N and the center Z(G) is the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3