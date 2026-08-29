import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
# We provide ZZ and QQ as standard examples of prime rings (integral domains).
# A witness should be a tuple: (R, I_gens, J_gens)
# where R is the ring (e.g., ZZ), I_gens is a list of generators for ideal I,
# and J_gens is a list of generators for ideal J.

def conditions(witness):
    try:
        R, I_gens, J_gens = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a prime ring
    # In commutative algebra, a prime ring is an integral domain.
    # We accept SymPy's ZZ, QQ, or any domain marked as a Field or Domain.
    try:
        h1 = False
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'is_Domain') and R.is_Domain:
            h1 = True
    except Exception:
        h1 = False

    # H_2: I is a non-zero ideal of R
    try:
        if not isinstance(I_gens, (list, tuple, set)):
            I_gens = [I_gens]
        
        in_R = all(i in R for i in I_gens)
        is_nonzero = any(i != 0 for i in I_gens)
        h2 = bool(in_R and is_nonzero)
    except Exception:
        h2 = False

    # neg_Q: The product ideal IJ is the zero ideal
    try:
        if not isinstance(I_gens, (list, tuple, set)):
            I_gens = [I_gens]
        if not isinstance(J_gens, (list, tuple, set)):
            J_gens = [J_gens]
            
        neg_q = True
        for i in I_gens:
            for j in J_gens:
                if i * j != 0:
                    neg_q = False
                    break
            if not neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a prime ring",
    "H_2: I is a non-zero ideal of R",
    "¬Q: The product ideal IJ is the zero ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2