import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _get_elements(G):
    if hasattr(G, 'generate') and callable(G.generate):
        return list(G.generate())
    return list(G.elements)

def conditions(witness):
    try:
        G, B = witness
    except Exception:
        return [False, False]
    
    # H_1: B is a block of imprimitivity for the action of G on X
    try:
        B_set = set(B)
        if not B_set:
            h1 = False
        elif not B_set.issubset(set(range(G.degree))):
            h1 = False
        else:
            h1 = True
            for g in _get_elements(G):
                gB = set(g(b) for b in B_set)
                if gB != B_set and not gB.isdisjoint(B_set):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # neg_Q: The setwise stabilizer of B in G does NOT act transitively on the elements of B
    try:
        B_set = set(B)
        if not B_set:
            neg_q = False
        elif not B_set.issubset(set(range(G.degree))):
            neg_q = False
        else:
            stab_elements = []
            for g in _get_elements(G):
                gB = set(g(b) for b in B_set)
                if gB == B_set:
                    stab_elements.append(g)
            
            B_list = list(B_set)
            x = B_list[0]
            orbit = set()
            for g in stab_elements:
                orbit.add(g(x))
            neg_q = orbit != B_set
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: B is a block of imprimitivity for the action of G on X",
    "¬Q: The setwise stabilizer of B in G does not act transitively on the elements of B"
]

N_HYP = 1
NEG_Q_INDEX = 1