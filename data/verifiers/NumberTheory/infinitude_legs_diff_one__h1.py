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

# Top-level setup
# (No specific named bindings needed for this Number Theory conjecture)

def conditions(witness) -> list[bool]:
    N = witness
    try:
        if N == sympy.oo or N == float('inf'):
            return [True]
        
        c_prev = 1
        c = 5
        found = False
        for _ in range(2000):
            if bool(c > N):
                found = True
                break
            c, c_prev = 6 * c - c_prev, c
            
        if not found:
            if isinstance(N, int):
                found = True
            elif isinstance(N, float) and N != float('inf'):
                found = True
            elif hasattr(N, 'is_finite') and N.is_finite:
                found = True
                
        neg_q = not found
    except Exception:
        neg_q = True
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There do not exist strictly positive integers a, b, c such that a^2 + b^2 = c^2, |a - b| = 1, and c > N"
]

N_HYP = 0
NEG_Q_INDEX = 0