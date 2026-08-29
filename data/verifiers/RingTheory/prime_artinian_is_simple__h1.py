import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.polys.domains import Domain

# Top-level setup for potential witness expressions
Z = sympy.S.Integers
Q = sympy.S.Rationals
R = sympy.S.Reals

def conditions(witness) -> list[bool]:
    # H_1: R is a prime ring
    # In the context of commutative rings (which SymPy domains represent),
    # a prime ring is equivalent to an integral domain.
    try:
        h1 = False
        if witness in (sympy.S.Integers, sympy.S.Naturals, sympy.S.Naturals0):
            h1 = True
        elif witness in (sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            h1 = True
        elif isinstance(witness, Domain):
            # All SymPy domains (ZZ, QQ, poly rings, etc.) are integral domains
            h1 = True
        elif isinstance(witness, int) and witness > 1:
            # An integer n represents the ring Z/nZ, which is prime iff n is prime
            h1 = sympy.isprime(witness)
    except Exception:
        h1 = False

    # ¬Q: R is not a simple ring
    # For commutative rings, a simple ring is equivalent to a field.
    try:
        is_simple = False
        if witness in (sympy.S.Integers, sympy.S.Naturals, sympy.S.Naturals0):
            is_simple = False
        elif witness in (sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            is_simple = True
        elif isinstance(witness, Domain):
            is_simple = bool(witness.is_Field)
        elif isinstance(witness, int) and witness > 1:
            # Z/nZ is a simple ring (a field) iff n is prime
            is_simple = sympy.isprime(witness)
        
        neg_q = not is_simple
    except Exception:
        # If we cannot determine it's a simple ring, we default to neg_q = False 
        # to avoid false positives in counterexample verification.
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a prime ring",
    "¬Q: R is not a simple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1