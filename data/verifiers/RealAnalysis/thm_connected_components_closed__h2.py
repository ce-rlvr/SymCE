import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: (X, T, C)
    where:
      - X is an iterable representing the points of the space.
      - T is an iterable of iterables representing the open sets (the topology).
      - C is an iterable representing the subset of X.
    """
    try:
        X, T, C = witness
    except Exception:
        return [False, False]

    # H_1: X is a topological space (T is a valid topology on X)
    try:
        X_set = frozenset(X)
        T_sets = set(frozenset(s) for s in T)
        
        h1 = True
        # 1. Empty set and X must be in T
        if frozenset() not in T_sets:
            h1 = False
        if X_set not in T_sets:
            h1 = False
            
        # 2. All elements of T must be subsets of X
        for s in T_sets:
            if not s.issubset(X_set):
                h1 = False
                break
                
        # 3. Closed under finite intersection and arbitrary union
        # (Since T is finite, pairwise union is sufficient for arbitrary union)
        if h1:
            for a in T_sets:
                for b in T_sets:
                    if a.intersection(b) not in T_sets:
                        h1 = False
                    if a.union(b) not in T_sets:
                        h1 = False
    except Exception:
        h1 = False

    # ¬Q: C is NOT a closed subset of X
    try:
        X_set = frozenset(X)
        T_sets = set(frozenset(s) for s in T)
        C_set = frozenset(C)
        
        if not C_set.issubset(X_set):
            neg_q = False
        else:
            # C is closed iff its complement is open (in T)
            complement = X_set - C_set
            neg_q = complement not in T_sets
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "¬Q: C is not a closed subset of X"
]

N_HYP = 1
NEG_Q_INDEX = 1