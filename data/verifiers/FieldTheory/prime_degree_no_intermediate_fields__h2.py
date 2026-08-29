import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    h1 = False
    neg_q = False
    
    try:
        # Witness can be an integer representing the degree of a finite field extension GF(p^n)/GF(p)
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1 = n >= 1
            # A finite field extension of degree n has an intermediate field iff n is composite
            neg_q = n > 1 and not sympy.isprime(n)
            
        # Witness can be a tuple (n, p) representing GF(p^n)/GF(p)
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (int, sympy.Integer)) and isinstance(witness[1], (int, sympy.Integer)):
            n, p = int(witness[0]), int(witness[1])
            h1 = n >= 1 and sympy.isprime(p)
            neg_q = n > 1 and not sympy.isprime(n)
            
        # Witness can be a PermutationGroup representing the Galois group of a Galois extension
        elif hasattr(witness, 'is_group') and witness.is_group:
            h1 = bool(witness.is_finite)
            order = witness.order()
            # By Cauchy's Theorem and Galois correspondence, a Galois extension has a proper 
            # intermediate field if and only if its Galois group has composite order.
            neg_q = order > 1 and not sympy.isprime(order)
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a finite extension field of F",
    "¬Q: There exists an intermediate field E such that F ⊊ E ⊊ K"
]

N_HYP = 1
NEG_Q_INDEX = 1