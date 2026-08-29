import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import functools
import math
import z3

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
    """
    witness is expected to be a tuple: (X, top, A, B)
    where:
      - X is an iterable of elements (the space)
      - top is an iterable of iterables (the open sets forming the topology)
      - A is an iterable of elements (subset of X)
      - B is an iterable of elements (subset of X)
    """
    try:
        X, top, A, B = witness
    except Exception:
        return [False, False, False]
    
    h1 = False
    try:
        X_set = frozenset(X)
        top_sets = set(frozenset(U) for U in top)
        if frozenset() in top_sets and X_set in top_sets:
            valid = True
            for U in top_sets:
                for V in top_sets:
                    if U.union(V) not in top_sets: 
                        valid = False
                    if U.intersection(V) not in top_sets: 
                        valid = False
            h1 = valid
    except Exception:
        h1 = False
        
    h2 = False
    try:
        if h1:
            A_set = frozenset(A)
            B_set = frozenset(B)
            if A_set.issubset(X_set) and B_set.issubset(X_set):
                if A_set.isdisjoint(B_set):
                    if X_set.difference(A_set) in top_sets and X_set.difference(B_set) in top_sets:
                        h2 = True
    except Exception:
        h2 = False
        
    neg_q = False
    try:
        if h1 and h2:
            # In a space with a finite topology, continuous real-valued functions 
            # are exactly those that are constant on the connected components.
            # Thus, I_A and I_B are comaximal iff no connected component intersects both A and B.
            clopens = [U for U in top_sets if X_set.difference(U) in top_sets]
            components = []
            for C in clopens:
                if not C: 
                    continue
                is_minimal = True
                for D in clopens:
                    if not D: 
                        continue
                    if D < C:
                        is_minimal = False
                        break
                if is_minimal:
                    components.append(C)
            
            for C in components:
                if not C.isdisjoint(A_set) and not C.isdisjoint(B_set):
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: A and B are disjoint closed subsets of X",
    "¬Q: I_A and I_B are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2