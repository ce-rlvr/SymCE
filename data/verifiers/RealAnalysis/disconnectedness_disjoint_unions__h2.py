import sympy
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_topological_space(X, T):
    try:
        X_set = frozenset(X)
        T_sets = set(frozenset(U) for U in T)
        
        # Check if all elements of T are subsets of X
        for U in T_sets:
            if not U.issubset(X_set):
                return False
                
        # Check if empty set and X are in T
        if frozenset() not in T_sets:
            return False
        if X_set not in T_sets:
            return False
            
        # Check closure under intersection and union
        for A in T_sets:
            for B in T_sets:
                if A.intersection(B) not in T_sets:
                    return False
                if A.union(B) not in T_sets:
                    return False
                    
        return True
    except Exception:
        return False

def count_clopen_sets(X, T):
    try:
        X_set = frozenset(X)
        T_sets = set(frozenset(U) for U in T)
        clopen_count = 0
        for U in T_sets:
            if (X_set - U) in T_sets:
                clopen_count += 1
        return clopen_count
    except Exception:
        return 0

def conditions(witness):
    # H_1: {X_i}_{i \in I} is a family of topological spaces
    h1_ok = False
    try:
        if isinstance(witness, (list, tuple)):
            h1_ok = True
            for space in witness:
                if not isinstance(space, (list, tuple)) or len(space) != 2:
                    h1_ok = False
                    break
                X, T = space
                if not is_topological_space(X, T):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: The index set I has cardinality >= 2
    h2_ok = False
    try:
        if isinstance(witness, (list, tuple)):
            h2_ok = len(witness) >= 2
    except Exception:
        h2_ok = False

    # ¬Q: The disjoint union is connected
    neg_q_ok = False
    try:
        if h1_ok:
            total_clopen = 1
            for space in witness:
                X, T = space
                c = count_clopen_sets(X, T)
                total_clopen *= c
            
            # A space is connected iff it has at most 2 clopen sets
            # (1 if empty, 2 if non-empty and connected)
            neg_q_ok = total_clopen <= 2
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: {X_i}_{i in I} is a family of topological spaces",
    "H_2: The index set I has cardinality >= 2",
    "¬Q: The disjoint union is connected"
]

N_HYP = 2
NEG_Q_INDEX = 2