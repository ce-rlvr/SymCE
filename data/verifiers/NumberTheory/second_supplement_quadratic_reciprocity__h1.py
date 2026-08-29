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

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        
        has_sol = False
        if p != 0:
            abs_p = abs(p)
            # Limit to prevent timeout on unreasonably large witnesses
            if abs_p > 1000000:
                return [False]
            for x in range(abs_p):
                if (x * x - 2) % abs_p == 0:
                    has_sol = True
                    break
        else:
            has_sol = False
            
        rhs = (p % 8 == 1) or (p % 8 == 7)
        
        neg_q = (has_sol != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The equivalence (x^2 ≡ 2 (mod p) has a solution iff p ≡ 1 or 7 (mod 8)) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0