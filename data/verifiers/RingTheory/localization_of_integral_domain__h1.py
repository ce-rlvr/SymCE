import sympy
from sympy import Integer, ZZ, QQ
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# For this domain, witnesses are typically represented as (n, S) where n is an integer
# representing the ring Z_n, and S is a list of integers representing the subset.
# We also provide ZZ and QQ for convenience if the witness uses SymPy rings.

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: 0 \\notin S",
    "¬Q: The localization S^{-1}R is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
        
    # Check if R is an integer (representing the ring Z_n)
    if isinstance(R, int) or (hasattr(R, 'is_integer') and R.is_integer):
        try:
            n = int(R)
        except Exception:
            return [False, False, False]
            
        if n < 2:
            return [False, False, False]
            
        # H1: S is a multiplicatively closed subset of R
        try:
            h1 = True
            S_list = list(S)
            if len(S_list) == 0:
                h1 = False
            for a in S_list:
                for b in S_list:
                    if (a * b) % n not in S_list:
                        h1 = False
                        break
                if not h1:
                    break
            if not all(isinstance(x, (int, Integer)) and 0 <= x < n for x in S_list):
                h1 = False
        except Exception:
            h1 = False

        # H2: 0 \notin S
        try:
            h2 = (0 not in S_list)
        except Exception:
            h2 = False

        # neg_Q: S^{-1}R is NOT an integral domain
        try:
            # In S^{-1}R, an element r/1 is zero iff there exists t in S such that t*r = 0 in R.
            def is_zero(r):
                return any((t * r) % n == 0 for t in S_list)
                
            if is_zero(1):
                # The zero ring is not an integral domain
                neg_q = True
            else:
                has_zero_divisor = False
                for r1 in range(n):
                    if is_zero(r1): 
                        continue
                    for r2 in range(n):
                        if is_zero(r2): 
                            continue
                        if is_zero((r1 * r2) % n):
                            has_zero_divisor = True
                            break
                    if has_zero_divisor:
                        break
                neg_q = has_zero_divisor
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    else:
        # Fallback for SymPy rings (e.g. ZZ, QQ)
        try:
            h1 = True
            S_list = list(S)
            if len(S_list) == 0:
                h1 = False
            for a in S_list:
                for b in S_list:
                    if (a * b) not in S_list:
                        h1 = False
                        break
                if not h1:
                    break
        except Exception:
            h1 = False
            
        try:
            h2 = (0 not in S_list)
        except Exception:
            h2 = False
            
        # If R is an integral domain like ZZ or QQ, its localization is always an integral domain.
        # Thus, the conclusion holds, meaning the negated conclusion is False.
        return [h1, h2, False]