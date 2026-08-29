import sympy
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup
# (No specific named objects required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        n = int(witness)
    except Exception:
        return [False]
        
    try:
        lhs = sympy.ntheory.totient(n)
        rhs = n
        for p in sympy.ntheory.primefactors(n):
            rhs *= (1 - sympy.Rational(1, p))
        neg_q = bool(lhs != rhs)
    except Exception:
        # If evaluation fails (e.g., n=0), the formula is invalid, so conclusion fails.
        neg_q = True
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: phi(n) != n * prod_{p|n} (1 - 1/p)"
]

N_HYP = 0
NEG_Q_INDEX = 0