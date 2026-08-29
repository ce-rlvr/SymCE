import sympy
from sympy import Interval, Union, Intersection, Complement, EmptySet, FiniteSet, S
import math
import itertools
import functools

# Top-level setup for standard objects that might be used in witness expressions
Reals = S.Reals
Rationals = S.Rationals
Integers = S.Integers
Naturals = S.Naturals

def conditions(witness) -> list[bool]:
    try:
        witness = tuple(witness)
    except Exception:
        return [False, False, False]

    # 1. Try interpreting the witness as a pair of SymPy sets (X, A)
    # where X is a subspace of the Reals and A is a subset of X.
    try:
        if len(witness) == 2:
            X, A = witness
            if isinstance(X, sympy.Set) and isinstance(A, sympy.Set):
                h1 = (A.is_subset(X) == True) and (A.is_empty == False)
                h2 = (A.is_subset(X) == True) and (X.is_subset(A) == False)
                
                # Compute boundary in the subspace topology of X
                X_minus_A = sympy.Complement(X, A)
                
                # Closure in X is the intersection of the closure in R with X
                closure_A = sympy.Intersection(A.closure, X)
                closure_X_minus_A = sympy.Intersection(X_minus_A.closure, X)
                
                # Boundary in X is the intersection of the two closures in X
                boundary_A = sympy.Intersection(closure_A, closure_X_minus_A)
                
                neg_q = (boundary_A.is_empty == True)
                
                return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # 2. Try interpreting the witness as a finite topological space (X, T, A)
    # where X is the space, T is the topology (list of open sets), and A is a subset.
    try:
        if len(witness) == 3:
            X, T, A = witness
            X_set = frozenset(X)
            T_sets = [frozenset(U) for U in T]
            A_set = frozenset(A)
            
            # Verify that T is a valid topology on X
            is_top = True
            if frozenset() not in T_sets or X_set not in T_sets:
                is_top = False
            if is_top:
                for U in T_sets:
                    for V in T_sets:
                        if U.intersection(V) not in T_sets:
                            is_top = False
                        if U.union(V) not in T_sets:
                            is_top = False
            
            if not is_top:
                return [False, False, False]
                
            h1 = A_set.issubset(X_set) and len(A_set) > 0
            h2 = A_set.issubset(X_set) and A_set != X_set
            
            def get_closure(S_subset):
                closed_sets = [X_set - U for U in T_sets]
                valid_closed = [C for C in closed_sets if S_subset.issubset(C)]
                if not valid_closed:
                    return X_set
                closure = valid_closed[0]
                for C in valid_closed[1:]:
                    closure = closure.intersection(C)
                return closure
                
            closure_A = get_closure(A_set)
            closure_X_minus_A = get_closure(X_set - A_set)
            boundary_A = closure_A.intersection(closure_X_minus_A)
            
            neg_q = len(boundary_A) == 0
            
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: A is a non-empty subset of X",
    "H_2: A is a proper subset of X",
    "¬Q: The topological boundary of A in X is empty"
]

N_HYP = 2
NEG_Q_INDEX = 2