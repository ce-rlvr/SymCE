import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: p is a prime number dividing the order of G
    try:
        G, p = witness
        try:
            order = G.order()
        except TypeError:
            order = G.order
        h1 = isprime(p) and order % p == 0
    except Exception:
        h1 = False

    # neg_Q: The intersection of all Sylow p-subgroups of G is not the trivial subgroup
    try:
        G, p = witness
        P = G.sylow_subgroup(p)
        
        try:
            P_elements = set(P.elements)
        except AttributeError:
            P_elements = set(P.generate())
            
        try:
            G_elements = set(G.elements)
        except AttributeError:
            G_elements = set(G.generate())
            
        core_elements = P_elements.copy()
        for g in G_elements:
            # Conjugate the elements of the Sylow p-subgroup by g
            conj_elements = {g * x * ~g for x in P_elements}
            core_elements = core_elements.intersection(conj_elements)
            # If the intersection drops to just the identity element, we can stop early
            if len(core_elements) == 1:
                break
                
        neg_q = len(core_elements) > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing the order of G",
    "¬Q: The intersection of all Sylow p-subgroups of G is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1