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
n = sympy.abc.n
x = sympy.abc.x
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        vals = []
        try:
            # Try to treat the witness as an iterable (e.g., generator, list)
            iterator = iter(witness)
            vals = list(itertools.islice(iterator, 2000))
        except TypeError:
            # If not iterable, check if it's callable (e.g., lambda n: ...)
            if callable(witness):
                for i in range(1, 2001):
                    vals.append(witness(i))
            # Otherwise, check if it supports indexing (e.g., sympy Sequence)
            elif hasattr(witness, '__getitem__'):
                for i in range(1, 2001):
                    vals.append(witness[i])
            else:
                return [False, False]
                
        # A valid sequence on N must be infinite; we require at least 2000 terms
        if len(vals) < 2000:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        # H_1: The set {x_n : n in N} is finite.
        # We approximate this by checking if the number of unique values stops growing
        # after the first 1000 terms.
        unique_1000 = set(vals[:1000])
        unique_2000 = set(vals)
        h1 = (len(unique_1000) == len(unique_2000))
    except Exception:
        h1 = False
        
    try:
        # Q: There exists a subsequence of (x_n) that is eventually constant.
        # This is true if at least one value appears infinitely many times.
        # We approximate this by checking if any value from the first 1000 terms 
        # also appears in the next 1000 terms.
        head = set(vals[:1000])
        tail = set(vals[1000:2000])
        q = len(head & tail) > 0
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The set {x_n : n in N} is finite",
    "¬Q: No subsequence of (x_n) is eventually constant"
]

N_HYP = 1
NEG_Q_INDEX = 1