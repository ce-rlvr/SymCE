import sympy
import sympy.combinatorics
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness can be represented as a tuple (X, T) where X is a set of points 
    and T is a list of open sets (each a set of points), or as a sympy Set.
    """
    # 1. Try to evaluate as a tuple (X, T) representing a finite topological space
    try:
        X_raw, T_raw = witness
        X = frozenset(X_raw)
        T = set(frozenset(U) for U in T_raw)
        
        # Check if T is a valid topology on X
        is_top = True
        if frozenset() not in T or X not in T:
            is_top = False
        else:
            # Closed under finite intersections
            for U in T:
                for V in T:
                    if U.intersection(V) not in T:
                        is_top = False
                        break
                if not is_top:
                    break
            # Closed under finite unions
            if is_top:
                for U in T:
                    for V in T:
                        if U.union(V) not in T:
                            is_top = False
                            break
                    if not is_top:
                        break
                        
        if is_top:
            # H1: X is connected (the only clopen sets are empty and X)
            clopen_count = sum(1 for U in T if (X - U) in T)
            h1 = (clopen_count == 2)
            
            # H2: X is a T1 space (every singleton is closed)
            h2 = all((X - frozenset([x])) in T for x in X)
            
            # H3: X contains at least two distinct points
            h3 = len(X) >= 2
            
            # neg_Q: X contains at least one isolated point (a singleton that is open)
            neg_q = any(frozenset([x]) in T for x in X)
            
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 2. Try to evaluate as a sympy Set (subspace topology of R)
    try:
        if isinstance(witness, sympy.Set):
            def is_connected_set(s):
                if isinstance(s, sympy.Interval):
                    return True
                if s == sympy.S.Reals:
                    return True
                if isinstance(s, sympy.FiniteSet) and len(s) <= 1:
                    return True
                return False
            
            # H1: X is connected
            h1 = is_connected_set(witness)
            
            # H2: X is a T1 space (all subsets of R are T1)
            h2 = True
            
            def has_at_least_two_points(s):
                if isinstance(s, sympy.FiniteSet):
                    return len(s) >= 2
                if isinstance(s, sympy.Interval):
                    return s.start != s.end
                if s == sympy.S.Reals:
                    return True
                return True 
                
            # H3: X contains at least two distinct points
            h3 = has_at_least_two_points(witness)
            
            def has_isolated_point(s):
                if isinstance(s, sympy.FiniteSet):
                    return len(s) > 0
                if isinstance(s, sympy.Union):
                    for arg in s.args:
                        if isinstance(arg, sympy.FiniteSet) and len(arg) > 0:
                            return True
                return False
                
            # neg_Q: X contains at least one isolated point
            neg_q = has_isolated_point(witness)
            
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: X is connected",
    "H_2: X is a T1 space",
    "H_3: X contains at least two distinct points",
    "¬Q: X contains at least one isolated point"
]

N_HYP = 3
NEG_Q_INDEX = 3